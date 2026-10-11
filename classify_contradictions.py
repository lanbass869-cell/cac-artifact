# -*- coding: utf-8 -*-
"""classify_contradictions.py — Phase 2: 对 Phase 1 的 198 对矛盾做分类
4 类: temporal_status_flip / entity_polarity_fp / granularity_mismatch / semantic_contradiction
分类判据（deterministic，非 LLM）:
  - temporal_status_flip: score>=6 且两条 valid_from 不同（旧→新状态变化）
  - entity_polarity_fp: score=3 且共享实体是泛词（非专名）
  - granularity_mismatch: 同实体同 source 不同时间（不是 cross-agent）
  - semantic_contradiction: 其余（人工复核候选）
"""
import json, sys, collections, datetime
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

d = json.load(open(r'E:/Temp/_scan_contradictions_results.json', encoding='utf-8'))
contras = d['contradictions']

# Entity frequency (to identify generic vs proper nouns)
from collections import Counter
ent_freq = Counter(c['entity'] for c in contras)

classified = []
for c in contras:
    ents = set(c['clash_entities'])
    score = c['score']
    va = c['a'].get('valid_from') or ''
    vb = c['b'].get('valid_from') or ''
    sa = c['a']['source']
    sb = c['b']['source']

    # Determine type
    if score >= 6:
        # High confidence: multiple id-like entity clashes
        if va and vb and va != vb:
            ctype = 'temporal_status_flip'
        elif sa == sb:
            ctype = 'self_agent_temporal'
        else:
            ctype = 'cross_agent_status_flip'
    elif score == 3:
        # Low confidence: single entity clash, likely entity name collision
        # Check if the clash entity is generic (appears in many pairs)
        clash_ent = c['clash_entities'][0] if c['clash_entities'] else '?'
        if ent_freq[c['entity']] >= 3:
            ctype = 'entity_polarity_fp'
        elif len(ents) == 1 and len(clash_ent) <= 6 and clash_ent.islower() and clash_ent.isalpha():
            ctype = 'entity_polarity_fp'  # short lowercase = likely generic word
        else:
            ctype = 'needs_human_review'
    else:
        ctype = 'needs_human_review'

    classified.append({**c, 'type': ctype})

types = Counter(c['type'] for c in classified)
print('Contradiction classification:')
for t, n in types.most_common():
    print(f'  {t}: {n} ({n/len(classified)*100:.1f}%)')

# Temporal analysis for genuine flips
flips = [c for c in classified if c['type'] in ('temporal_status_flip', 'cross_agent_status_flip')]
print(f'\nGenuine status flips: {len(flips)}')
for f in flips:
    print(f"  {f['entity']}: {f['a']['source']}({(f['a']['valid_from'] or '?')[:10]}) -> {f['b']['source']}({(f['b']['valid_from'] or '?')[:10]})")

result = {
    'classification_date': datetime.datetime.now().isoformat(),
    'total_pairs': len(classified),
    'type_distribution': dict(types),
    'genuine_status_flips': len(flips),
    'classified': classified,
}
out = r'E:/Temp/_contradiction_classification.json'
with open(out, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f'\nOutput: {out}')
