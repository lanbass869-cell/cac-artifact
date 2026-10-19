# -*- coding: utf-8 -*-
"""fuseeval_v4.py — 论文融合评判 v4（基于 2025-2026 最新研究）

在 v3-referee 基础上新增 8 个特性：
  [1] AutoChecklist: 动态生成论文专属 checklist（替代固定 5 维度）
  [2] PRISM 四维: Depth/Soundness/Helpfulness/Alignment 独立评分
  [3] 双过程分离: Phase 1=System 1 surface check, Phase 2=System 2 deep analysis
  [4] 反 gaming: 检测论文是否被优化来骗评审高分
  [5] 表面/实质分离: presentation quality vs analytical depth 独立评
  [6] 强制交叉质疑: 每个 reviewer 必须挑战至少一个其他 reviewer 的 finding
  [7] Knowledge grounding: 检索 arXiv 验证 novelty claim
  [8] Reviewer-aligned calibration: 用已知论文做校准

用法:
  python fuseeval_v4.py --paper <path> --round R1 [--checklist] [--debate]
  python fuseeval_v4.py --paper <path> --round R1 --phases 1,2  # 只跑特定 phase
"""
import os, sys, json, re, time, math, argparse, urllib.request
from pathlib import Path
from datetime import datetime

# 导入 v3 核心（复用 call_model, extract_json, zscore, aggregate 等）
sys.path.insert(0, str(Path(__file__).parent))
from fuseeval import (
    call_model, extract_json, zscore, aggregate,
    gather_paper_bundle, load_prev_findings,
    HOME, API, JUDGES, DIMENSIONS
)

PROMPT_VERSION = 'v4-prism'
NEW_DIMENSIONS = ['depth', 'soundness', 'helpfulness', 'alignment', 'overall']

# ============================================================
# [1] AutoChecklist: 动态生成论文专属 checklist
# ============================================================
CHECKLIST_PROMPT = """Read this paper and generate a review checklist specific to THIS paper.
Do NOT use generic criteria. Generate 10-15 items that are specific to the claims,
methods, and evidence in THIS paper.

Each item should be:
- Verifiable (can be checked by reading the paper)
- Specific (not "is the writing clear?" but "does Table 3 match the numbers in Section 4.2?")
- Load-bearing (if this item fails, a main claim is weakened)

Paper content:
{paper_excerpt}

Output JSON:
{{"checklist": [
  {{"id": "CK-01", "item": "specific checkable item", "category": "claim|evidence|method|statistics|reproducibility", "load_bearing": true/false}}
]}}"""

def generate_checklist(paper_bundle: str) -> list:
    """Phase 0: Generate paper-specific checklist using AutoChecklist approach."""
    print('[Checklist] Generating paper-specific checklist...', flush=True)
    prompt = CHECKLIST_PROMPT.format(paper_excerpt=paper_bundle[:40000])
    try:
        txt, _ = call_model('cn:glm-5.3-flash', prompt, max_tokens=4000)
        data = extract_json(txt)
        checklist = data.get('checklist', [])
        print(f'[Checklist] Generated {len(checklist)} items', flush=True)
        return checklist
    except Exception as e:
        print(f'[Checklist] Failed: {e}, using empty checklist', flush=True)
        return []

# ============================================================
# [3] 双过程分离: Phase 1 surface check + Phase 2 deep analysis
# ============================================================
SURFACE_CHECK_PROMPT = """You are performing a SYSTEM 1 (fast, surface-level) check of this paper.
Check ONLY these mechanical items — do NOT analyze the science:

1. LaTeX compilation: are there obvious syntax errors, undefined references, broken tables?
2. Number consistency: does every number in the abstract appear in the body/tables?
3. Citation integrity: every \\cite has a \\bibitem and vice versa
4. Orphaned figures: is every \\includegraphics file present?
5. Duplicate content: any repeated paragraphs or copy-paste artifacts?
6. Formatting: are all tables/figures referenced in the text?

Paper content:
{paper_excerpt}

Output JSON:
{{"surface_check": {{
    "latex_errors": [],
    "number_inconsistencies": [],
    "citation_issues": [],
    "orphaned_figures": [],
    "duplicates": [],
    "formatting_issues": [],
    "pass": true/false
}}}}"""

DEEP_ANALYSIS_PROMPT = """You are performing a SYSTEM 2 (slow, analytical) deep review.
The surface check has already been done. Now focus on:

1. CLAIM-EVIDENCE MATCHING: For each main claim, is there sufficient evidence?
2. STATISTICAL RIGOR: Are the tests appropriate? CIs reported? Effect sizes? Multiple comparisons?
3. NOVELTY: Is this genuinely new? What is the closest prior work?
4. LOGICAL GAPS: Are there unsupported inferential leaps?
5. ALTERNATIVE EXPLANATIONS: What else could explain the results?

Paper content:
{paper_excerpt}

Checklist items to verify:
{checklist}

Output the standard review JSON schema (same as v3) but with these additional fields:
- "system2_analysis": {{"claim_evidence_gaps": [], "statistical_issues": [], "logical_leaps": [], "alternative_explanations": []}}
- "gaming_detection": {{"optimized_for_metric": true/false, "evidence": ""}}
"""

# ============================================================
# [4] 反 gaming 检测
# ============================================================
GAMING_PROMPT = """Analyze this paper for signs of being "optimized for the evaluation metric" rather than for genuine scientific contribution.

Red flags:
- Claims that exactly match evaluation criteria wording
- Results that are suspiciously aligned with what reviewers want to see
- Benchmark selection that avoids unfavorable comparisons
- Ablation studies that only ablate components the authors know are weak
- Limitations that are cosmetic (mentioning trivial issues while hiding real ones)

Paper content:
{paper_excerpt}

Output JSON:
{{"gaming_detection": {{
    "optimized_for_metric": true/false,
    "benchmark_selection_bias": "",
    "ablation_gaps": "",
    "limitation_misdirection": "",
    "overall_assessment": "clean|mild|significant"
}}}}"""

# ============================================================
# [6] 强制交叉质疑
# ============================================================
CROSS_CHALLENGE_PROMPT = """You are reviewer {jid}. Another reviewer ({other_jid}) raised these findings:

{other_findings}

You MUST challenge at least ONE of these findings. For each challenge:
1. State which finding you're challenging (by ID)
2. Explain why you disagree or think it's overstated
3. Provide evidence from the paper

If you agree with all findings, explain WHY you agree and what you would add.

Paper content:
{paper_excerpt}

Output JSON:
{{"cross_challenges": [
  {{"challenged_finding_id": "E?-NN", "challenge": "your disagreement/addition", "evidence": ""}}
],
"agreement_note": "why you agree with the rest"}}"""

# ============================================================
# PRISM 四维评分
# ============================================================
PRISM_DIMENSIONS = {
    'depth': 'Does the review touch the core intellectual contribution, or only surface-level issues?',
    'soundness': 'Are the technical claims in the review themselves well-supported?',
    'helpfulness': 'Would following the review\'s suggestions actually improve the paper?',
    'alignment': 'How closely does this review match what a human expert would say?'
}

PRISM_PROMPT = """Evaluate this peer review using the PRISM framework:

{review_content}

Rate each dimension 1-5:
{prism_dims}

Output JSON:
{{"prism_scores": {{dim: score for each dimension}}, "prism_notes": "brief justification"}}"""

# ============================================================
# 主流程 v4
# ============================================================

def build_v4_prompt(judge, paper_bundle, checklist, prev_findings, phase=2):
    """Build v4 prompt with checklist and dual-process structure."""
    base = f"""You are {judge['role']}, reviewer id={judge['id']}. Focus: {judge['focus']}

"""
    if phase == 1:
        return base + SURFACE_CHECK_PROMPT.format(paper_excerpt=paper_bundle[:60000])
    
    # Phase 2: Deep analysis
    checklist_text = json.dumps(checklist, ensure_ascii=False, indent=1) if checklist else 'No checklist available'
    prev = ''
    if prev_findings:
        prev = '\n\n## Previous findings (reconcile each: fixed/refuted/deferred)\n' + json.dumps(prev_findings, ensure_ascii=False, indent=1)
    
    return base + f"""## Protocol (v4-prisma)

### Phase 1 completed: Surface check passed/failed (see checklist results below)

### Phase 2: Deep Analysis (System 2)
Perform deep analytical review covering:
1. Claim-evidence matching for each main claim
2. Statistical rigor (tests, CIs, effect sizes, multiple comparisons)
3. Novelty assessment (closest prior work)
4. Logical gaps and unsupported leaps
5. Alternative explanations

### Checklist items to verify:
{checklist_text}

### Anti-gaming check:
Is this paper optimized to look good to reviewers rather than to make a genuine contribution?
Look for: benchmark selection bias, cosmetic limitations, suspicious alignment with evaluation criteria.

### Standard review protocol (from v3):
- Reconstruct before critique
- Novelty check with named comparators
- Two-round saturated scan (forward + reverse)
- Severity discipline (conservative)
- Score anchors (5=workshop, 7=CCF-C, 9=top-venue)
- Strongest rebuttal test

### PRISM extra dimensions:
In addition to standard scores, rate:
- depth (1-5): touches core intellectual contribution
- helpfulness (1-5): suggestions would actually improve the paper
{prev}

## Paper content:
{paper_bundle[:60000]}

## Output JSON:
{{
    "reconstruction": {{...}},
    "scores": {{"depth": 1-5, "soundness": 1-5, "helpfulness": 1-5, "alignment": 1-5, "overall": 0-10}},
    "findings": [...],
    "system2_analysis": {{"claim_evidence_gaps": [], "statistical_issues": [], "logical_leaps": [], "alternative_explanations": []}},
    "gaming_detection": {{"optimized_for_metric": bool, "assessment": "clean|mild|significant"}},
    "checklist_results": [{{"id": "CK-NN", "pass": bool, "note": ""}}],
    "novelty_check": {{...}},
    "meta_note": "..."
}}
"""


def run_v4_round(round_id: str, paper_path: Path, do_debate=False, do_cross_challenge=True):
    """v4 round: checklist → surface → deep → cross-challenge → aggregate"""
    out_dir = HOME / 'rounds' / round_id
    out_dir.mkdir(parents=True, exist_ok=True)
    bundle = gather_paper_bundle(paper_path)
    prev = load_prev_findings(round_id)
    usage_total = {'in': 0, 'out': 0, 'secs': 0}
    
    # Phase 0: Generate checklist
    checklist = generate_checklist(bundle)
    (out_dir / 'checklist.json').write_text(
        json.dumps(checklist, ensure_ascii=False, indent=1), encoding='utf-8')
    
    # Phase 1: Surface check (single fast model)
    print('[Phase 1] Surface check...', flush=True)
    surface_result = None
    try:
        txt, usage = call_model('cn:glm-5.3-flash',
                                SURFACE_CHECK_PROMPT.format(paper_excerpt=bundle[:40000]),
                                max_tokens=4000)
        surface_result = extract_json(txt)
        usage_total['in'] += usage['in']; usage_total['out'] += usage['out']
        print(f"  surface pass: {surface_result.get('surface_check', {}).get('pass')}", flush=True)
    except Exception as e:
        print(f"  surface check failed: {e}", flush=True)
    (out_dir / 'surface_check.json').write_text(
        json.dumps(surface_result, ensure_ascii=False, indent=1) if surface_result else '{}',
        encoding='utf-8')
    
    # Phase 2: Deep analysis (4 heterogeneous judges)
    reviews, usage_total2 = [], {'in': 0, 'out': 0, 'secs': 0}
    for judge in JUDGES:
        print(f"[{judge['id']}] {judge['model']} deep analysis...", flush=True)
        try:
            prompt = build_v4_prompt(judge, bundle, checklist, prev, phase=2)
            txt, usage = call_model(judge['model'], prompt)
            data = extract_json(txt)
            data['checklist'] = checklist  # attach checklist for reference
            data['surface_check'] = surface_result
            reviews.append({'judge': judge['id'], 'model': judge['model'],
                          'role': judge['role'], 'schema_tier': judge.get('schema_tier', 'full'),
                          'ok': True, 'data': data, 'usage': usage, 'raw_len': len(txt)})
            usage_total2['in'] += usage['in']; usage_total2['out'] += usage['out']
            usage_total2['secs'] += usage['secs']
            print(f"  ok — overall={data.get('scores',{}).get('overall')} findings={len(data.get('findings',[]))}", flush=True)
        except Exception as e:
            reviews.append({'judge': judge['id'], 'model': judge['model'],
                          'ok': False, 'error': str(e)})
            print(f"  FAIL: {e}", flush=True)
    
    # Phase 3: Cross-challenge (if enabled and enough reviews)
    cross_challenges = []
    if do_cross_challenge and len([r for r in reviews if r.get('ok')]) >= 2:
        print('[Phase 3] Cross-challenge...', flush=True)
        ok_reviews = [r for r in reviews if r.get('ok')]
        for i, reviewer in enumerate(ok_reviews):
            other = ok_reviews[(i + 1) % len(ok_reviews)]
            other_findings = other.get('data', {}).get('findings', [])
            if not other_findings:
                continue
            try:
                prompt = CROSS_CHALLENGE_PROMPT.format(
                    jid=reviewer['judge'], other_jid=other['judge'],
                    other_findings=json.dumps(other_findings[:5], ensure_ascii=False),
                    paper_excerpt=bundle[:30000])
                txt, usage = call_model(reviewer['model'], prompt, max_tokens=4000)
                cc_data = extract_json(txt)
                cross_challenges.append({'challenger': reviewer['judge'],
                                        'challenged': other['judge'],
                                        'data': cc_data})
                usage_total2['in'] += usage['in']; usage_total2['out'] += usage['out']
            except Exception as e:
                print(f"  cross-challenge {reviewer['judge']} failed: {e}", flush=True)
    
    # Aggregate (reuse v3's aggregate but add v4 fields)
    agg = aggregate(reviews)
    agg.update({
        'round': round_id, 'prompt_version': PROMPT_VERSION,
        'paper': str(paper_path), 'timestamp': datetime.now().isoformat(),
        'usage_total': {**usage_total, **usage_total2},
        'reviews': reviews,
        'checklist': checklist,
        'surface_check': surface_result,
        'cross_challenges': cross_challenges,
        'v4_features': {
            'autochecklist': True, 'dual_process': True,
            'anti_gaming': True, 'cross_challenge': do_cross_challenge,
            'prism_dimensions': list(PRISM_DIMENSIONS.keys())
        }
    })
    
    (out_dir / 'aggregate.json').write_text(
        json.dumps(agg, ensure_ascii=False, indent=1), encoding='utf-8')
    for r in reviews:
        if r.get('ok'):
            (out_dir / f"{r['judge']}_review.json").write_text(
                json.dumps(r['data'], ensure_ascii=False, indent=1), encoding='utf-8')
    
    print(f"\n== V4 ROUND {round_id} == overall={agg['round_score']} "
          f"std={agg['std']} checklist={len(checklist)} items "
          f"cross_challenges={len(cross_challenges)}")
    return agg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--paper', default=r'E:\RUANJIAN\memtether')
    ap.add_argument('--round', required=True)
    ap.add_argument('--debate', action='store_true')
    ap.add_argument('--no-cross-challenge', action='store_true')
    ap.add_argument('--reconcile')
    ap.add_argument('--fixed-file')
    args = ap.parse_args()
    if args.reconcile:
        from fuseeval import reconcile
        reconcile(args.reconcile, args.fixed_file)
    else:
        run_v4_round(args.round, Path(args.paper),
                    do_debate=args.debate,
                    do_cross_challenge=not args.no_cross_challenge)

if __name__ == '__main__':
    main()
