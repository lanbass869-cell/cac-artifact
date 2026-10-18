# Peer Review: "A Case Study of Evaluation Integrity Violations in Machine Learning Evaluation Frameworks"

**Manuscript:** `paper4_trust_but_verify.tex` (single-authored, anonymous submission)
**Review type:** Full review — three reviewer reports (R1 methodology, R2 evaluation, R3 impact), consolidated concerns with blocking status, consistency audit, and overall recommendation.
**Rating scale:** 1–5 (5 = excellent, 4 = good, 3 = borderline/acceptable with revisions, 2 = poor/major revision, 1 = very poor).

---

## Summary of the Paper

The paper reports five recurring "disclosure failure" patterns observed during operation of a production memory system (MemTether): (P1) active distortion declaration, (P2) dual-metric gap reporting, (P3) holdout independent verification, (P4) evaluator self-check, and (P5) denominator sanity validation. It contributes **evalguard**, a Python metadata checker validating JSON-format evaluation outputs against these patterns; validation on eight benchmarks (five judge-based, three deterministic third-party suites: HELM BoolQ, Open LLM Leaderboard, IFEval); a source-code audit of 33 evaluation files from 15 frameworks reporting 15 findings across 8 files (24.2%), including a "CRITICAL" `nanmean` pattern in LM Eval Harness and fractional exact-match in HELM; a 50-pair NLI feasibility probe (BART-large/MNLI, 84% accuracy); and production case studies, notably a judge-403 error that silently shrank the denominator from 60 to 7 questions, inflating 45.0% to a false 71.4%.

The core thesis — auditing evaluation outputs for *disclosure completeness* the way CI pipelines audit code, as one layer of a three-layer integrity stack (input contamination / process validity / output metadata) — is sensible, timely, and potentially useful. The execution, however, contains numerous internal inconsistencies, an incorrect statistic, a corrupted bibliography, dangling citations, and a validation design with a circularity problem. These are especially damaging because the paper's subject is evaluation integrity itself.

---

## Reviewer 1 (R1): Methodology

**Rating: 2/5**

### Summary assessment
The five patterns are reasonable operationalizations of known failure modes, and the author is commendably explicit that each is individually straightforward and that evalguard is a *metadata* checker, not a semantic correctness checker (L34–35, L110). The three-layer framing is a useful conceptual contribution. However, the methodology suffers from four structural problems: single-system derivation with circular validation, unvalidated thresholds, an incorrect statistical argument, and loose pattern-to-case mappings.

### Strengths
1. Honest scoping: the paper repeatedly and correctly disclaims that evalguard cannot detect computational bugs (L35, L110, L292, L302–304, L353). The output-layer vs source-layer boundary is well drawn.
2. Pattern definitions include explicit detection criteria and thresholds (L64, L72, L87, L95, L103), making them reproducible in principle.
3. The author self-reports anti-patterns in their own evaluation code (5 bare `except` blocks; L306, L332) — genuine disclosure, well aligned with the paper's thesis.
4. The NLI probe is correctly framed as "a feasibility probe, not a benchmark" (L350), with author-constructed pairs disclosed.

### Major methodological concerns
See consolidated MAJOR list (M1–M12 below); from a methodology standpoint the most serious:

- **Circular validation (M5).** Five of eight "benchmarks" are the authors' own outputs or fixtures: LongMemEval/mem0/LoCoMo are their own runs, HotpotQA is "simulated," MemoryQA is a synthetic "bad example" (L142). The abstract describes all five judge-based settings as "our own evaluation outputs" (L22). The only *independent* evidence comes from three deterministic suites — precisely the setting where P3/P4 are declared N/A. Patterns derived from one system are "validated" mostly on that same system: a near self-fulfilling design, since the tool finds metadata gaps in outputs never generated with the metadata schema in mind.
- **Incorrect statistic (M3).** L253: "Under a binomial model with expected violation rate p = 0.05, the probability of observing ≥ 5 violations in 50 frameworks is P(X ≥ 5) = 0.38." For Binomial(50, 0.05), P(X ≥ 5) ≈ 0.104 (exact; Poisson λ = 2.5 gives ≈ 0.109). The claimed 0.38 is wrong by ~3.5×. The test's units also do not match the data: the audit observed 15 findings in 33 *files*, not "≥5 violations in 50 frameworks." The (correct) exploratory-vs-confirmatory instinct therefore rests on an erroneous calculation over mismatched units.
- **Unvalidated thresholds (M8).** The 10-pt holdout gap, 80% self-check agreement, 5% denominator tolerance, and "≥2 metric types" are defaults chosen "to minimize false positives rather than optimized against a labeled error distribution" (L137). No sensitivity analysis; no false-positive rate on any clean corpus (the single MemoryQA "bad example" tests sensitivity to injected failure, not specificity). A disclosure checker whose false-positive behavior is unknown is hard to recommend as a CI gate — a failed gate blocks pipelines.
- **Loose case-to-pattern mapping (M12).** Case 2 (test-set contamination) is mapped to P1 (distortion declaration) and Case 3 (self-referential poisoning) to P3 (holdout verification) (L213–219). In both cases the pattern names the *detection mechanism*, not the *violation class*. P1's detection criterion (metadata fields present) would not have caught Case 2; a holdout did not *cause* Case 3. The mapping inflates apparent coverage of the pattern set.
- **Threshold/example weaknesses.** The holdout example (100% vs 81.8%, L89) implies a holdout of n = 11 (9/11 = 81.8%), never stated; claiming "overfitting" from an 18.2-pt gap on ~11 questions is statistically unsupported.

### Minor methodological points
- The "≥2 distinct metric types" check (L72, L131) is gameable: HELM's four exact-match *variants* (EM, quasi-EM, prefix-EM, quasi-prefix-EM; L185) count as four distinct metrics. These are variants of one metric family; the check should distinguish families from variants.
- The binomial/prevalence discussion sits inside Related Work (L253) rather than validation or limitations — misplaced.
- The intro's hypothetical "94.4% on LongMemEval" (L27) is never reconciled with any number actually reported later (32.5%/71.0% multi-session; 43.2–62.6% strict across runs), leaving the reader unsure whether it is real.
- Single-system derivation is acknowledged (L292, L351), but the mitigations offered do not address validation circularity.

**R1 verdict:** The conceptual framework is publishable in principle; the validation design and statistical argument are not, in current form.

---

## Reviewer 2 (R2): Evaluation and Empirics

**Rating: 2/5**

### Summary assessment
The empirical program has three legs — eight-benchmark output validation, 33-file source audit, 50-pair NLI probe — plus production case studies. Legs 2 and 3 are the most interesting and the most under-verified; leg 1 is largely circular. Arithmetic is mostly internally consistent (see consistency audit), but the source-audit table contradicts its own totals, the framework count is inconsistent (15 vs 47), and the evaluation narrative contradicts the contributions list (5 incidents vs 3 cases).

### Strengths
1. The third-party validation is *real*: HELM BoolQ per-instance stats (1,000 canonical / 4,000 perturbed, 87.4% EM), Open LLM Leaderboard aggregate for a named model (21,606 samples, 7 metric types, 33 subtasks), IFEval 541 samples with 4 accuracy variants (L185–189). Sample sizes and denominators are precise, and IFEval's 541 matches the known benchmark size.
2. The finding that pattern applicability is evaluation-type-dependent (judge-based vs deterministic; P3/P4 N/A for deterministic; L171–179) is a genuine empirical result, honestly reported rather than hidden.
3. Source-audit headline findings are specific enough to be checkable (file names, line numbers, GitHub issues for LM Eval Harness #4319 and HELM #4363; L334), and the admission that evalguard *cannot* see the `nanmean` denominator shrinkage (L302) is an honest and important boundary result.
4. Case 1 (60 → 7 denominator shrinkage, 45.0% → 71.4%) is compelling, arithmetically consistent, and well documented (L211).

### Major evaluation concerns
- **M4 — Source-audit table contradicts itself (BLOCKING).** Table 2 (L308–328): per-row findings sum correctly to 15 (1+3+1+1+5+2+1+1), and 8/33 = 24.2% is correct. But the Total row states severity "**1C/1H/5M**" = 7, which cannot account for 15 findings. L306 claims findings "span three severity levels and **four check categories**," while the table shows only three categories ever triggered (SA1, SA2, SA4; SA3 and SA5 never fire). The caption says "detailed subset of the **47-framework** audit" (L310) while every other mention says **15 frameworks** (L282, L306, L358, L378). These are exactly the class of "silent denominator"-style errors the paper exists to catch.
- **M6 — Dangling analyses (BLOCKING).** The Reproducibility Statement reports LongMemEval strict scores of 43.2% / 62.6% / 43.1% across three runs and promises "cross-run variance analyzed in the Limitations section" (L367). Limitations contains no such analysis. Related Work claims "Our temporal drift finding is a memory-specific manifestation" (L245) — no temporal drift finding is presented anywhere. A 19.4-point cross-run swing in a memory benchmark is arguably the paper's most important self-observation; its promised analysis is missing.
- **M5 — Circularity** (detailed under R1): the abstract's characterization of five judge-based benchmarks as "our own evaluation outputs" (L22) launders two synthetic fixtures (HotpotQA simulated, MemoryQA bad example) into the benchmark count. Table 1 should separate real own-system runs from simulated/synthetic fixtures; as written, "8 benchmarks" overstates independent evidence by 3×.
- **M7 — Five incidents vs three cases (BLOCKING).** Contribution 4 promises "five concrete incidents" (L37); Section 6 presents three (L199–226); Fig. 4's caption says "three integrity violations" (L224). Either deliver five or correct the claim.
- **M9 — Single-author, unverified audit.** Manual source findings (Findings 1–5) have no independent verification; acknowledged (L376). Filed issues partially mitigate, but Finding 4's "potentially misleading" unweighted-averaging claim is a *design trade-off*, not clearly a bug (per-subject vs per-instance averaging is a known reporting choice); soften.

### Minor evaluation points
- "We run evalguard on its own source code… The tool passes all five checks on its own implementation" (L232) is a category error: P1–P5 check evaluation *outputs*, not source code. Presumably the source-audit mode reports no findings on evalguard itself — say that.
- Three different anonymous repositories are referenced: `evalguard` (L22, L259), `evalguard-self-audit` (L232), `evalguard-audit` (L367). Consolidate or explain the split.
- "Both findings have been reported to the respective maintainers" (L334) — "both" of what? Two headline findings or all 15? Ambiguous.
- The NLI probe's 84% is internally consistent (42/50 correct; recall 21/25; specificity 21/25; F1 = 0.84) but the pair set is author-constructed and tiny; the paper says so, to its credit — label it as a probe in the abstract too (currently absent there, featured in the conclusion).
- No false-positive evaluation: evalguard's P1 check (metadata must contain distortion/variant/judge fields) will fail essentially *any* raw output file from a framework that does not emit an evalguard-compatible schema. Report what a fully compliant passing output looks like and how many real-world outputs could ever pass P1. As designed, P1 may be a near-universal fail — making it a compliance checklist, not a detector. Be explicit about this.
- Table 1: explain why the synthetic MemoryQA "bad example" passes P2 (constructed to fail exactly P1/P3/P4/P5?).

**R2 verdict:** The empirical core contains real value (third-party validation, source audit, incident documentation), but tables and claims require a full internal-verification pass before the work can be reviewed on its merits.

---

## Reviewer 3 (R3): Significance, Presentation, and Impact

**Rating: 3/5**

### Summary assessment
If cleaned up, this paper could be genuinely useful: "CI for evaluation outputs" is a memorable, actionable framing, and the three-layer stack (input contamination → transcript/process validity → output metadata disclosure) is a good organizing idea for the subfield. The 60→7 denominator incident is a persuasive motivating artifact. However, presentation defects are severe and — unavoidably — ironic: a paper about disclosure failures and silent inconsistencies contains a corrupted bibliography, dropped citations, contradictory counts, and a dangling promised analysis. Readers will (correctly) weigh the paper's own integrity as evidence for whether its tooling discipline is real.

### Strengths
1. The framing that scores are *perishable knowledge claims* requiring disclosure metadata is compelling and connects to real practitioner pain (silent judge failures, contaminated eval sets).
2. evalguard as a `pip install`-able artifact with sub-second checks is a realistic adoption path; the "run it as a CI step after each evaluation" recommendation (L229) is concrete.
3. The adoption guide and self-audit gesture (running the tool on the authors' own pipeline and reporting 5 bare-`except` findings against themselves, L332) models the behavior the paper advocates.
4. Honest limitations in several places: pattern non-exhaustiveness, NLP-specificity, JSON-only inputs, output-layer blindness (L292–293, L353).

### Major impact/presentation concerns
- **M1 — Bibliography corrupted (BLOCKING).** The paper claims "34 references" twice with *two mutually contradictory breakdowns*: L48 ("14 peer-reviewed, 15 arXiv, 5 documentation") vs L513 ("12 peer-reviewed, 18 arXiv, 4 documentation"). The actual `\thebibliography` contains **24** `\bibitem` entries. Entries are malformed: `benchmark_contamination_1` mashes three different works (watermarking paper + Belz reproducibility title + "Position: Evaluation Scores Are Perishable Knowledge Claims") under one arXiv ID (L394–397); `\bibitem` commands are nested *inside* other bibitems (`silent_medical_2023` nests SilentAgent at L438; `silent_tool_2026` nests EvalPitfalls at L454); two entries float with no keys at all (L442–446: "RewardHackingAgents…", "Scaling Law of Evaluation Failure…"); titles truncated mid-word ("Detection and Remedi", "Confidence Estimates f.", "Hidden Confounds in Local Tool."); and `li2025unreliable`, `ayyagari2026pinned`, `gu2024judgesurvey`, `belz2021reproducibility` each appear twice. For an integrity paper this is close to disqualifying in current form — though entirely fixable.
- **M2 — Dropped citations produce broken prose (BLOCKING).** Related Work L236 contains three subject-less sentences: "**propose** runtime error attribution; we detect disclosure failures post-evaluation. **study** agents that compromise the evaluation pipeline… **analyze** statistical failure of averaging…" — the `\citet` commands were evidently lost. Section 5.3 (L195–197) discusses ELT-Bench-Verified, Automated Transcript Analysis, Maintaining Benchmarks, MemUse, DyadMem, and PRAGMA — none with citation commands, none in the bibliography. The "complementary quality assurance stack" positioning (a core novelty claim) rests on works the reader cannot retrieve.
- **M10 — Contribution identity confusion.** L334 declares "The source-level audit is **the primary contribution** of this work," contradicting the Contributions list (five patterns, evalguard, cross-benchmark validation, case studies — no source audit) and the abstract's emphasis. The paper reads as having drifted mid-writing from "evalguard" paper to "source audit" paper to "three-layer stack" paper. Pick one primary contribution and restructure.
- **M11 — Structure.** Substantive new results (source audit, NLI probe) are presented *inside* "Discussion and Limitations" (§8.1–8.2); the prevalence/binomial discussion is in Related Work; Findings 3–5 appear *after* the table that already summarized them; the final limitations subsection heading is a full broken sentence ("Data Scope Limitation. Our case studies come from… Output-Layer Limitation", L351). A reviewer cannot tell what is a result and what is discussion.

### Minor presentation points
- `\graphicspath{{E:/Temp/paper4_figs_tex/}}` (L8) — absolute local path; figures will not resolve for anyone else.
- Duplicate `\label{sec:repro}` (L257 and L364, the latter stranded after Companion Work).
- Wrong cross-reference: output-layer limitation cites the HELM/LM Eval Harness findings as `Section~\ref{sec:cases}` (L353); they are in §8.1 (`sec:source_audit`).
- natbib in `numbers` mode with author-year-style `\bibitem[...]` labels — dead weight; `\bibliographystyle{unsrtnat}` is inert under a manual `thebibliography`.
- Abstract is ~430 words with hedging that belongs in the body ("We acknowledge that these choices are heuristic…").
- Typos/mechanical: "a incorrectly implemented F1" (L292); "BAAI/BAAI/bge-m3" doubled prefix (L367); unmatched quote style on "loose"/"strict" (L189); "validation., analogous" stray period (L334); spacing artifacts "(SA1)\ NaN" (L304); escaped "agent\'s" (L197).
- Hardware contradiction in one sentence: "no discrete GPU for inference; NVIDIA RTX 4060 8 GB was used for local embedding model inference" (L367) — presumably LLM inference was CPU-only, but as written it contradicts itself.
- Title/scope mismatch: singular "A Case Study" and "Machine Learning Evaluation Frameworks" vs multiple case studies centered on memory-system evaluation.
- Fig. 2 and Fig. 4 captions rely on color alone (green/red) for pass/fail — accessibility and grayscale-printing problem.
- "Production" operation spans September–October 2026 (≈6 weeks; L29, L367); qualify the term.

**R3 verdict:** The idea and artifact have real adoption potential; the manuscript as written would embarrass both author and venue if published — fixable but requiring a rewrite-level pass.

---

## Consolidated MAJOR Concerns (with Blocking Status)

| # | Concern | Blocking? |
|---|---------|-----------|
| M1 | Bibliography corrupted: 24 bibitems vs claimed 34; two contradictory reference breakdowns (14/15/5 at L48 vs 12/18/4 at L513); nested `\bibitem`s (L438, L454); keyless orphan entries (L442–446); mashed-up entry `benchmark_contamination_1` (L394–397); truncated titles; four duplicated entries | **BLOCKING** |
| M2 | Dropped citations: three subject-less sentences in Related Work (L236); six discussed works with no citation keys or bibliography entries (ELT-Bench-Verified, Automated Transcript Analysis, Maintaining Benchmarks, MemUse, DyadMem, PRAGMA; L195–197) | **BLOCKING** |
| M3 | Incorrect binomial statistic: P(X ≥ 5) for Binomial(50, 0.05) ≈ 0.104, not 0.38 (L253); units mismatch (test framed over "50 frameworks" / "≥5 violations" vs observed 15 findings in 33 files) | **BLOCKING** |
| M4 | Source-audit table self-contradictions: severity total "1C/1H/5M" = 7 ≠ 15 findings (L325); "four check categories" vs 3 observed (SA1/SA2/SA4; L306); caption's "47-framework audit" vs "15 frameworks" everywhere else (L310 vs L282/L306/L358/L378) | **BLOCKING** |
| M5 | Validation circularity: 5/8 "benchmarks" are the authors' own outputs or synthetic fixtures; abstract labels all five judge-based settings "our own evaluation outputs" (L22, L142); independent evidence limited to three deterministic suites where P3/P4 are N/A; no specificity/false-positive evaluation anywhere | **BLOCKING** |
| M6 | Dangling analyses: promised "cross-run variance analyzed in the Limitations section" absent (L367); "Our temporal drift finding" (L245) never presented; intro's "94.4%" (L27) never reconciled with reported numbers | **BLOCKING** |
| M7 | Contribution 4 claims "five concrete incidents" (L37); Section 6 presents three; Fig. 4 caption says "three integrity violations" (L224) | **BLOCKING** |
| M8 | Thresholds (10-pt holdout gap, 80% self-check, 5% denominator, ≥2 metrics) unvalidated; no sensitivity analysis or false-positive rate on clean outputs; CI-gate recommendation (L229) unjustified without FP data | **BLOCKING** |
| M9 | Single-author source audit without independent verification of Findings 1–5 (acknowledged at L376); Finding 4 (MMLU averaging) is a design trade-off, not clearly a defect — soften | No |
| M10 | Contribution identity conflict: "source-level audit is the primary contribution" (L334) vs contributions list and abstract | No |
| M11 | Structure: results embedded in Discussion (§8.1–8.2); prevalence analysis in Related Work (L253); broken subsection heading (L351); Findings 3–5 after their summarizing table | No |
| M12 | Pattern-to-case mapping loose: Case 2→P1 and Case 3→P3 map detection mechanisms to violation classes (L213–219), overstating pattern coverage | No |

---

## MINOR Concerns

1. Broken subsection heading containing two full sentences ("Data Scope Limitation. Our case studies come from… Output-Layer Limitation", L351).
2. Duplicate `\label{sec:repro}` (L257, L364); second instance stranded after Companion Work.
3. Wrong cross-reference: `\ref{sec:cases}` used for source-audit findings (L353); should be `sec:source_audit`.
4. Hard-coded absolute `\graphicspath{E:/Temp/paper4_figs_tex/}` (L8) — non-portable submission.
5. Three distinct anonymous repo URLs (`evalguard`, `evalguard-self-audit`, `evalguard-audit`; L22, L232, L259, L367) — consolidate or explain.
6. Category error: "passes all five checks on its own implementation" (L232) — P1–P5 check outputs, not source code.
7. "Both findings have been reported to the respective maintainers" (L334) — ambiguous antecedent (2 vs 15 findings).
8. P2 check counts EM *variants* as distinct metric types (HELM's 4 EM variants, L185) — metric family vs variant distinction needed.
9. Holdout example implies n = 11 (9/11 = 81.8%, L89) — report n; "overfitting" claim unsupported at that sample size.
10. Hardware self-contradiction: "no discrete GPU for inference; RTX 4060 used for embedding inference" (L367).
11. "BAAI/BAAI/bge-m3" doubled prefix (L367).
12. Typos: "a incorrectly implemented F1" (L292); "validation., analogous" (L334); "agent\'s" (L197); unmatched quote style on "loose"/"strict" (L189); spacing artifacts "(SA1)\ NaN" (L304).
13. Abstract ~430 words, over-length, with body-appropriate hedging; NLI probe absent from abstract but featured in conclusion.
14. natbib `numbers` mode with author-year bibitem labels; `\bibliographystyle{unsrtnat}` inert under manual `thebibliography`.
15. Title/scope mismatch: singular "A Case Study" + "Machine Learning Evaluation Frameworks" vs memory-system multi-case content.
16. Fig. 2 and Fig. 4 pass/fail encoded by color alone — add symbols/patterns for grayscale and color-vision accessibility.
17. "Production" = ~6 weeks of operation (Sept–Oct 2026); qualify the term.
18. MemoryQA "bad example" passes P2 — explain fixture construction so Table 1 is interpretable.
19. Prevalence/binomial discussion misplaced in Related Work (L253).
20. Companion Work note cites an anonymous manuscript — citation to unpublished, unverifiable work; consider folding into future work.

---

## Consistency Check

### Citation-key integrity (verified programmatically)
- All 24 `\citep`/`\citet` keys used in the body resolve to `\bibitem` entries; no undefined citation keys and no orphaned keyed bibitems at the key level.
- **However:** the bibliography contains keyless orphan entries (L386–392 duplicating `li2025unreliable` and `ayyagari2026pinned`; L442–446 "RewardHackingAgents" and "Scaling Law of Evaluation Failure" with no keys), nested `\bibitem`s inside `silent_medical_2023` (L438) and `silent_tool_2026` (L454), and six prose-discussed works (§5.3) with no keys at all. Reference-count claims (34) do not match the 24 actual entries. Verdict: **key-level consistency OK; entry-level integrity FAIL.**

### Numerical consistency (verified by recomputation)

**Internally consistent (PASS):**

| Claim | Locations | Check |
|---|---|---|
| 60→7 questions; 45.0% → 71.4%; 26.4-pt distortion | L22, L105, L207, L211 | 5/7 = 71.43% ✓; 27/60 = 45.0% ✓; Δ = 26.4 ✓; 53 + 7 = 60 ✓ |
| Strict 32.5% vs judge 71.0%; 38.5-pt gap | L74, L80 | 71.0 − 32.5 = 38.5 ✓ |
| Main 100% vs holdout 81.8%; 18.2-pt gap | L89 | 100 − 81.8 = 18.2 ✓ (n implied 11, unstated — see MINOR 9) |
| Source audit: 15 findings, 8/33 files, 24.2% | L253, L284, L306, L358 | 1+3+1+1+5+2+1+1 = 15 ✓; 8/33 = 24.24% ✓ |
| NLI probe: 84% accuracy, F1 = 0.84 | L348, L358 | 42/50 = 84% ✓; recall 21/25, specificity 21/25, precision 21/25 → F1 = 0.84 ✓ |
| IFEval 541 samples; HELM 1,000 canonical / 4,000 perturbed | L185, L189 | Matches known benchmark sizes ✓ |
| Open LLM Leaderboard 21,606 samples, 7 metrics, 33 subtasks | L187 | Internally plausible, no external check possible ✓ |

**Inconsistent (FAIL):**

| Discrepancy | Locations | Detail |
|---|---|---|
| Reference count & breakdown | L48 vs L513 vs actual | "34 refs (14/15/5)" vs "34 refs (12/18/4)" vs 24 actual bibitems — three mutually incompatible statements |
| Severity total | L325 vs L316–323 | "1C/1H/5M" = 7 ≠ 15 findings; MEDIUM count alone is ≥9 (1+1+5+2+1) |
| Framework count | L310 vs L282/L306/L358/L378 | "47-framework audit" vs "15 frameworks" |
| Check categories | L306 vs Table 2 | "four check categories" vs 3 observed (SA1, SA2, SA4) |
| Incident count | L37 vs L199–226, L224 | "five concrete incidents" vs three cases presented |
| Promise vs delivery | L367 vs §8 | Cross-run variance analysis promised in Limitations; absent |
| Temporal drift claim | L245 | Cites a "finding" that is never presented |
| Primary contribution | L334 vs L31–38, abstract | Source audit as "primary contribution" vs evalguard-centric contributions |
| 8 "benchmarks" vs evidence base | L22, L142 | 3 of 8 are simulated/synthetic fixtures counted as validation benchmarks |

### Citation–claim spot checks
- `wu2024longmemeval`, `zheng2023judge`, `liang2023helm`, `gao2024lmeval`, `openllm2024`, `locomo2024`, `gu2024judgesurvey`, `belz2021reproducibility`: plausible, correctly attributed. ✓
- `benchmark_contamination_1`: entry is a chimera of three works under arXiv:2607.26191 — attribution unreliable. ✗
- Entries with 2026 arXiv IDs (e.g., 2609.33044, 2609.34262, 2610.05732) cannot be verified by this reviewer; several have truncated titles and should be double-checked by the author. ⚠
- Six works discussed in §5.3 (ELT-Bench-Verified, Automated Transcript Analysis, Maintaining Benchmarks, MemUse, DyadMem, PRAGMA) have **no citations and no bibliography entries**. ✗

---

## Overall Recommendation

**Reject (major revision / resubmission encouraged).**

**Weighted ratings:** R1 Methodology 2/5 · R2 Evaluation 2/5 · R3 Impact 3/5.

### Rationale

This paper is a victim of its own thesis. It argues that evaluation artifacts must be internally consistent, complete in disclosure, and free of silent inconsistencies — and then ships a manuscript with a corrupted bibliography (24 entries claiming to be 34, with two contradictory breakdowns), three sentences whose citations were dropped mid-word, a source-audit table whose severity total (7) contradicts its finding count (15), a "47-framework audit" that is elsewhere a 15-framework audit, a promise of five case studies that delivers three, a promised cross-run variance analysis that is absent, and an incorrect binomial probability (0.38 vs the correct ≈ 0.104). Any one of these is a fixable slip; jointly, in a paper whose entire contribution is automated integrity checking, they undermine confidence that the artifact was run on the paper itself with the rigor the paper demands of others. The author has, to their credit, created the perfect rebuttal to this paragraph: run evalguard's own checks and the source-audit mode on this manuscript before resubmission.

Underneath the presentation damage is a paper worth writing:

1. The 60→7 denominator incident is a genuinely valuable, fully consistent documented failure (5/7 = 71.4% vs 27/60 = 45.0%).
2. The three-layer integrity stack (input contamination / transcript validity / output disclosure) is a useful organizing contribution, and the placement of evalguard at the output layer is clearly argued.
3. The evaluation-type-dependence finding (P3/P4 N/A for deterministic evals; deterministic suites fail P1 but pass P2/P5) is an honest, real result.
4. The source audit's headline findings (nanmean NaN-shrinkage in LM Eval Harness, fractional EM in HELM) are specific, checkable, and reported upstream with issue numbers — and the honest admission that evalguard itself cannot see them is a better contribution than the paper seems to realize.
5. The self-audit disclosure (5 bare `except` blocks in the authors' own pipeline) models exactly the behavior the paper advocates.

### Conditions for a strong resubmission

1. **Fix every internal contradiction** (M1, M2, M4, M6, M7): rebuild the bibliography from BibTeX, restore the dropped `\citet` commands, reconcile 15 vs 47 frameworks and the severity totals, deliver the promised cross-run variance analysis (a 19.4-point swing deserves its own subsection, not a dangling promise), and make the case-study count true.
2. **Correct the binomial analysis** (M3) and align its units with the reported data, or remove it.
3. **Break the validation circularity** (M5): run evalguard on judge-based outputs the authors did not produce (e.g., published LongMemEval/LoCoMo results from other teams, RAGAS/TruLens outputs), report a false-positive rate on compliant outputs, and stop counting synthetic fixtures as benchmarks.
4. **Validate the thresholds** (M8) with at least a coarse sensitivity analysis, and either justify the CI-gate recommendation with false-positive data or soften it.
5. **Pick one primary contribution** (M10) and restructure so results live in results sections, not Discussion and Limitations.

The reviewer notes the deep irony that this paper's flaws are themselves a strong empirical demonstration of its thesis: silent inconsistencies survive writing, reading, and submission without automated checking. The most compelling possible revision of this paper is one where its own artifacts demonstrably pass its own checks.

*Review saved to `E:\RUANJIAN\workdocs\memtether\cac-artifact\paper4_trust_but_verify_review.md`.*
