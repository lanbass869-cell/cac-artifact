# Peer Review — JSS Submission: MemTether (JSS-MemTether-20261018)

**Manuscript:** MemTether: A Local-First Agent Memory System with Bi-Temporal Supersession and Hash-Chained Audit
**Review scope:** Sections from line 280 onward — Specialization (Table 3), Memory Court, Findings 1–5, Expanded Downstream Validation, Memory Supersession Prediction, Evaluation Summary (Table 1), Lessons Learned, Threats to Validity, Ethics Statement, Conclusion, Declarations, Data Availability, Reproducibility, and Bibliography.
**Review date:** 2026-10-19

**Summary of the manuscript (reviewed sections):** The paper reports five empirical findings from a 30-day single-user production deployment of a multi-agent memory system (type-dependent correction rates, an entity-resolution gap, correction clustering, injection coverage <1%, cross-agent harm asymmetry), a new supersession-prediction task (DistilBERT, macro F1 ≈ 0.946/0.947), benchmark results (LongMemEval, LoCoMo, ConflictBank), tamper-detection and reproducibility artifacts, and an unusually candid Threats-to-Validity section.

---

## Reviewer 1 (R1) — Methodology

**Rating: 3 / 5**

### Assessment

The methodological core of the reviewed sections is a mix of observational production analytics (correction rates, Kaplan–Meier survival analysis, day-level clustering), a controlled downstream experiment (stale vs. correct context), a supervised prediction task, and standard benchmark evaluation. The multi-method design is appropriate for a systems paper, the data-scope note (three overlapping datasets: 2,590 / 2,309 / 2,635 records) is a model of transparency, and the survival analysis is a sensible tool for the retention-policy question. However, several methodological choices weaken the inferential claims:

1. **Causal language outruns the design.** Finding 1 asserts a "clear explanation" for the 11× procedural/decision correction gap (procedures change, rationales do not) — plausible, but this is an uncontrolled observational pattern; confounds (e.g., procedural memories are also more frequently *touched* by tooling, which mechanically increases correction opportunities) are not examined. Finding 5 says cross-agent corrections "cause" disproportionate harm; only the downstream experiment supports causality, and it is small and has selection issues (see R2).
2. **The r^N "mathematical upper bound" is an overclaim** (Lessons 1). The bound holds only under an independence assumption: each of N facts retrieved independently with probability r. Joint retrieval, query decomposition, reranking, or multi-turn aggregation can beat it. Worse, the paper's own fitted base rate r = 0.736 implies r^10 ≈ 4.7%, which is implausibly below observed multi-session accuracy — evidence the fitted exponential model is misspecified, yet the text presents r^N as "a mathematical upper bound that no embedding-based retrieval system can overcome." Also, the symbol *r* is used for two unrelated quantities in the same paragraph (per-fact retrieval probability and the Pearson correlation −0.135); this must be fixed.
3. **Attribution of benchmark gains is unestablished.** The Threats section states the schema-grounded retrieval (SGM) path produces **zero** (entity, attribute) pairs on English benchmark data. It is therefore unclear which components (ECO/SSI/AFN/SGM) actually produce the LongMemEval 68.8% and LoCoMo 0.523 results. No component ablation appears in the reviewed sections. Without it, the +8.6pp claim over mem0 cannot be attributed to any mechanism.
4. **B1-gate evaluation circularity** (Reproducibility §B1). The synthetic benchmark generator and the verdict-replay assertion share the same detection logic and seed; "50/50 recall and 50/50 precision" on self-generated ground truth is weak evidence. The full benchmark (50 conflicting + 80 near-miss + 20 dev entities, §3.10) is the meaningful test and should be the one reproducible from this section.
5. **Downstream experiment design (Expanded Validation):** 100 entities sampled, only 43 gradeable because of API content filtering — a 57% attrition whose direction of bias is unknown (are filtered entities more or less likely to diverge?). Grading of "divergence" is done by a third LLM call whose model identity is not named; same-family self-grading bias is possible and no human validation of the judge is reported.

### Strengths
- Kaplan–Meier framing of memory lifetime with right-censoring is methodologically sound and directly motivates the TTL recommendation (median survival 2.5 days for procedures).
- The metric-note paragraph distinguishing 73pp (accuracy drop, n=11) from 86% (divergence rate, n=43) is exactly the kind of clarification papers usually omit.
- Pre-registered-feeling detail: fixed seeds (42), pinned version (v0.1.0a80.post2, commit d1c0f99), exact pytest counts.

---

## Reviewer 2 (R2) — Evaluation Quality

**Rating: 2 / 5**

### Assessment

The evaluation is extensive in *coverage* (four benchmark families, a production deployment, an integration-test inventory, a new prediction task with seven baselines) and commendably transparent about limitations. But *numeric hygiene* is inadequate: multiple headline and supporting numbers are internally inconsistent, unsupported, or methodologically fragile. I verified all arithmetic; results are in the Number Consistency Check below. The issues that drive my rating:

1. **Headline supersession F1 is inconsistent:** Table 7 reports **0.946** with "+14.2pp" (consistent: 0.946 − 0.804 = 0.142), but the Finding box and Table 1 report **0.947** while still claiming "+14.2pp" (0.947 − 0.804 = 14.3pp). One of the two values is wrong; the abstract-level Table 1 inherits the error.
2. **Gradeability rate is stated backwards:** the Expanded Downstream Validation section says 43 of 100 entities were gradeable (43%). The Threats section says "57% gradeable from 100 sampled" — this reverses the actual figure (57% is the *non*-gradeable rate).
3. **The 25.3pp claim in Lessons 2 is not derivable from any reported number.** The strict-vs-judge gap in Table 1 is 68.8 − 62.4 = **6.4pp**. The oracle diagnostic ("semantically correct in 15 of 31 strict-matched failures") cannot produce 25.3pp under any reading I can construct. If 25.3pp comes from an earlier section, it must be cross-referenced; otherwise it must be corrected.
4. **Confidence interval method:** the reported 95% CI [76%, 96%] for 37/43 is the Wald (normal-approximation) interval. For n=43 with p≈0.86, Wald undercover; Wilson gives [72.7%, 93.4%] and Clopper–Pearson is similar. The interval should be recomputed with an exact/Wilson method and the method named.
5. **Entity-resolution funnel mixes sampling units** (Finding 2). The 81.7% raw clash rate comes from 2,000 sampled *fact pairs*; the 0.044% (11/24,907) rate is over *cross-source pairs*; the "1,857× reduction" divides rates defined on different units and is also arithmetically off (81.7 / 0.0442 ≈ **1,849×**; 1,857× results from dividing by the rounded 0.044). The paragraph is also garbled ("after applying the full classification pipeline" appears twice with a broken clause).
6. **ConflictBank sample accounting:** the specialization table uses 3 categories × 500 = **1,500** samples, but the text and Table 1 reference a "full n=2000 evaluation" (F1 = 0.897). The relationship between the 1,500-sample subset and the 2,000-sample evaluation is never explained.
7. **Baseline provenance mixing in Table 1:** mem0 overall judge 60.2% is from the published paper; mem0 multi-session 52.4% is the authors' own run; LangMem is the authors' own run with 79.2% NOT_FOUND. The caption claims "identical judge configuration," but a published number produced under a different harness cannot satisfy that claim. All comparative numbers should come from a single harness, or the table must visibly separate provenance.
8. **Table 1 row "Cross-agent harm: 73pp vs self-corr 0.7pp"** commensurates two different metrics (percentage-point accuracy drop from an n=11 experiment vs. a divergence *rate* from an n=300 experiment). The text acknowledges the distinction; the table erases it.
9. **"86% of downstream answer divergence" (Figure 5 caption, Lessons 4)** conflates a divergence *rate among cross-agent entities* (86% of 43) with a *share of total harm*. Whether cross-agent corrections cause "the overwhelming majority of measurable downstream harm" depends on exposure base rates, which are not provided.
10. **Reproducibility gap on the headline benchmark:** the released script reproduces LongMemEval at **58.3%**, not the headline 68.8% (a 10.5pp gap; the +8.6pp advantage over mem0 exists only on the EAF pipeline path, which is not the released reproduction path). The discrepancy is honestly disclosed, but as it stands the paper's most important comparison is not independently reproducible.

### Strengths
- Majority-class macro F1 = 0.461 for the supersession task is *correct* (verified: 0.4605) — the baselines are honestly constructed.
- Per-class precision/recall (0.91/0.89) is reported to preempt the "predicts majority" objection.
- 5/5 anchored tamper scenarios detected with the 1/1 unanchored miss reported as expected — honest negative reporting.
- The specialization table (F1 = 0.000 on semantic/misinformation conflicts) is an unusually honest scope-limiting result.

---

## Reviewer 3 (R3) — Practical Impact

**Rating: 3 / 5**

### Assessment

For the JSS audience, the actionable yield of the reviewed sections is real:

1. **Type-aware retention (Finding 1 + survival analysis)** is the most deployable recommendation in the paper: procedural memories with median survival 2.5 days vs. no other type reaching 50% correction in 30 days directly supports a default ~3-day TTL with re-validation for procedures and indefinite persistence for decisions. The evidence chain (91.5% vs. 8.2% correction rates; KM curves; explicit window-artifact check) is the strongest in the paper.
2. **Cross-agent conflict interception as the priority mechanism (Finding 5)** is well-motivated: 14.9% of corrections are cross-agent but stale cross-agent context diverges 86% of the time vs. 0.7% for self-corrections. The mapping to the B1 write-time gate gives the finding an engineering consequence.
3. **Monitoring guidance (Finding 3)** — distinguishing organic corrections (2.7/day) from bulk consolidation spikes (269 on 2026-09-27) to avoid false alarms — is practical and rarely stated.
4. **The supersession-prediction task** enables proactive governance (risk-flagging at write time, TTL assignment). DistilBERT at macro F1 ≈ 0.946/0.947 vs. a 0.804 metadata baseline suggests the signal is real and cheap features go far.

However, practical impact is capped by deployment scope:

- **Single user, zero external users, one machine.** All five findings derive from one operator's data. The recommendations are phrased generically ("memory systems should…") but are supported by n=1 deployments. The Threats section admits this; the abstract/conclusion phrasing should be softened to match.
- **Chinese-only SGM.** A core retrieval advantage (84% vs 64%) is demonstrated only in Chinese, and the component produces zero pairs on English data — so practitioners deploying on English workloads cannot expect the headline results.
- **The supersession model is not deployed closed-loop**; its practical value is currently asserted, not measured (the Finding box says so honestly).
- **Alpha software:** v0.1.0a80.post2, SECURITY.md alpha notice. Production-adoption claims should be read accordingly.
- The **file-level pointer sharing lessons** (WAL contention, single-machine scope) are useful but thin; the "client-server for larger deployments" pointer is stated without data.

The Ethics Statement is adequate: desensitization described concretely (paths replaced, identifiers removed, keys stripped), EU AI Act Article 12 mentioned with an appropriate non-legal-advice disclaimer. The single-author CRediT statement and the "no inter-annotator agreement" admission are consistent with the Threats section.

---

## Consolidated MAJOR Concerns

| # | Concern | Blocking? |
|---|---------|-----------|
| M1 | Internal numeric inconsistencies in reported results: supersession F1 0.946 (Table 7, "+14.2pp" consistent) vs. 0.947 (Finding box & Table 1, where "+14.2pp" is arithmetically wrong — should be +14.3pp); Threats section states "57% gradeable" where the experiment reports 43/100 = 43% gradeable; Lessons 2 claims strict matching undercounts "by 25.3pp," derivable from no reported number (strict–judge gap is 6.4pp). These are errors of fact in a quantitative paper. | **Yes** |
| M2 | Headline LongMemEval result (68.8% judge; +8.6pp over mem0) is not reproducible via the released artifact: the reproduction script yields 58.3% via a different (non-EAF) path. Disclosure is appreciated, but the primary configuration's evaluation path must be released, or the headline must be demoted to the reproducible configuration. | No |
| M3 | Comparative baselines mix provenance (mem0 60.2% published vs. 52.4% self-run vs. LangMem self-run with 79.2% NOT_FOUND) under a caption claiming "identical judge configuration." Require a single-harness comparison, or explicit provenance split within Table 1. | No |
| M4 | No component attribution for English-benchmark results: SGM contributes zero (entity, attribute) pairs on English data (per Threats), so the source of the LongMemEval/LoCoMo gains is unidentified. Require an ECO/SSI/AFN/SGM ablation on the English benchmarks. | No |
| M5 | Metric conflation around cross-agent harm: 73pp (n=11 accuracy drop), 86% (37/43 divergence rate), 0.7% (n=300 divergence rate) are used interchangeably; Figure 5 caption and Lessons 4 state cross-agent corrections "cause 86% of downstream answer divergence," conflating a rate with a share of harm; "power-law asymmetry" is unsupported by two point estimates. Require one canonical metric, corrected captions, and removal or justification of the power-law framing. | No |
| M6 | Downstream experiment validity: 57% of sampled entities ungradeable due to API content filtering (unknown selection bias); divergence judged by an unnamed LLM (potential same-family self-grading bias) with no human validation; binomial test and CI method unspecified (reported CI [76%, 96%] matches Wald, which undercover at this n; Wilson gives [72.7%, 93.4%]). | No |
| M7 | Generalizability ceiling: all findings from a single-user, zero-external-user deployment operated by the author. Acknowledged in Threats, but recommendation-level claims ("memory systems should…") throughout Findings and Lessons must be softened or explicitly conditioned on this scope. | No |
| M8 | The r^N result is presented as "a mathematical upper bound that no embedding-based retrieval system can overcome," but it assumes independent per-fact retrieval; the paper's own fitted r = 0.736 implies r^10 ≈ 4.7%, suggesting model misspecification; the symbol r is reused for the Pearson correlation (−0.135) in the same passage. Require reframing as a heuristic independence model and disambiguation of notation. | No |
| M9 | B1-gate synthetic evaluation is circular (generator and verdict assertions share detection logic and seed); 50/50 precision/recall on self-generated ground truth carries little evidential weight. Make the §3.10 full benchmark (50 conflicting + 80 near-miss + 20 dev entities) the reproduced evaluation. | No |

## Consolidated MINOR Concerns

| # | Concern |
|---|---------|
| m1 | Entity-resolution reduction factor: exact ratio is 81.7 / 0.04416 ≈ **1,849×**, not 1,857× (1,857× comes from dividing by the rounded 0.044%). Recompute from raw counts. |
| m2 | ConflictBank accounting: specialization table = 3 categories × 500 = 1,500 samples, but text/Table 1 cite a "full n=2000 evaluation" (F1 = 0.897). Explain the sampling relationship or reconcile the counts. |
| m3 | Finding 3: "262 of 269" corrections on 2026-09-27 were consolidation, implying 7 organic corrections that day; excluding only the consolidation process gives 87/30 ≈ 2.9 organic/day, not the reported 2.7 (= 80/30, which excludes all 269). Clarify the exclusion rule. |
| m4 | Memory Court case study: "2 asserted available while 3 asserted banned/403, yielding a 60% contradiction rate" — the derivation of 60% is unstated and inconsistent with any denominator involving 15 or 24. Define the metric. |
| m5 | Finding 2 paragraph is garbled: "after applying the full classification pipeline" appears twice with a broken sentence in between. Rewrite. |
| m6 | Table 1 row "Cross-agent harm: 73pp / self-corr: 0.7pp" mixes an accuracy drop (pp) with a divergence rate (%) as if commensurable; relabel or split into two rows with n's. |
| m7 | "Four public benchmarks" (Conclusion) counts the authors' own newly released supersession dataset; state "three public benchmarks and one newly released dataset." |
| m8 | Temporal accuracy ("MT 100% vs mem0 27.2%") appears only in a Reproducibility code comment; it is absent from the main text and Table 1. Document it or remove it. |
| m9 | Memory Court: "Five engineering-level gaps… none affect the correctness of the core mechanism" sits awkwardly beside the 1/1 unanchored tamper scenario going undetected (anchor tail coverage). Rephrase the correctness claim. |
| m10 | Audit-log scale: 2,346 audit entries vs. "31K+ operations" — clarify what subset of operations is audited. |
| m11 | Finding 4's 1,957 active memories is a fourth dataset size not covered by the three-dataset scope note; add it. |
| m12 | Lessons 2: define the oracle-ceiling diagnostic's denominator ("15 of 31 strict-matched failures" — 31 of what population, how sampled?). |
| m13 | "Improving retrieval by 1% is equivalent to storing 2× more memories" (Finding 4) has no derivation; the 209× overscan factor alone does not imply this equivalence. Derive or delete. |
| m14 | Name the grading model in the downstream experiment and state the binomial test variant (exact vs. normal) and CI method; switch the CI to Wilson/Clopper–Pearson. |
| m15 | LoCoMo comparison (0.523 vs. 0.344 token-F1) lacks run details in the reviewed sections (which model generated answers, how many conversations, judge configuration); add or cross-reference. |
| m16 | LongMemEval multi-session row: "79.7% (106/133)" — verify the subset size matches LongMemEval's official multi-session split definition and state which of the five question types are included. |
| m17 | Bibliography items dated 2026 with arXiv IDs in the 26xx range cannot be verified by reviewers; ensure all citations resolve and are correct at submission time. |
| m18 | The artifact repo URL (github.com/lanbass869-cell/cac-artifact) and the system repo (github.com/MemTether/MemTether) differ in naming; confirm both are permanent and mirrored, since the reproducibility section depends on them. |
| m19 | Data Availability says production data "is not publicly released" while the Reproducibility §Production Data Note says "SQL queries for all reported counts are included in the Reproducibility section above" — no SQL queries are visible in the reviewed text. Include them or fix the cross-reference. |
| m20 | Court export claims the HTML verifier works "in any browser without installing software"; state whether it was tested in more than one browser (the engineering gaps list mentions browser CI verification as a gap). |

---

## Number Consistency Check (independently verified)

**Verified consistent:**

| Claim | Check | Result |
|---|---|---|
| Procedural correction rate 91.5% | 118/129 = 0.9147 | ✔ |
| 11× procedural vs. decision rate | 91.5/8.2 = 11.16 | ✔ |
| Table 4 totals: 2,590 typed records | 129+289+426+1333+413 = 2,590 | ✔ |
| Table 4 corrected total = 386 | 118+49+46+139+34 = 386 | ✔ |
| Survival cohort n=2,309 (349 events + 1,960 censored) | 349+1960 = 2,309 | ✔ |
| Benchmark 2,635 = 386 pos + 2,249 neg | ✔; pos rate 14.65% ≈ "14.6%" | ✔ |
| 2026-09-27 = 77.1% of corrections | 269/349 = 0.7708 | ✔ |
| Other daily percentages (5.4%, 3.4%, 14.1%) | 19/349, 12/349, 49/349 | ✔ |
| Organic rate 2.7/day | (349−269)/30 = 2.67 | ✔ (but see m3) |
| Mean 426 chars/memory | 833,488/1,957 = 425.9 | ✔ |
| Coverage 0.48% | 3,980/833,488 = 0.478% | ✔ |
| 209× overscan | 833,488/3,980 = 209.4 | ✔ |
| Cross-agent 14.9% / self 81.4% / 3.7% unattributed | 52/349, 284/349, 13/349 | ✔ |
| 86% divergence = 37/43 | 0.8605 | ✔ |
| Multi-session 79.7% = 106/133 | 0.7970; gap to 52.4% = 27.3pp | ✔ |
| Court tests 14 | 6+2+1+2+1+2 = 14 | ✔ |
| 534 passed + 4 skipped = 538 collected | ✔ | ✔ |
| Temporal F1 0.889 from P=1.000, R=0.800 | 2PR/(P+R) = 0.8889 | ✔ |
| Majority-class macro F1 0.461 | 0.4605 | ✔ |
| Table 7 "+14.2pp over best baseline" | 0.946 − 0.804 = 0.142 | ✔ |
| r^10 at r=0.9 ≈ 0.35 | 0.3487 | ✔ |

**Inconsistencies found:**

| # | Location | Issue | Severity |
|---|---|---|---|
| N1 | Table 7 vs. Finding box & Table 1 | Supersession macro F1: **0.946** vs. **0.947**. With 0.947, "+14.2pp" is wrong (0.947−0.804 = 14.3pp). Also "all text-based baselines by 19+" is 19.3pp with 0.947 (0.947−0.754) — fine — but should be stated precisely. | High |
| N2 | Expanded Validation vs. Threats | Gradeable rate: **43/100 = 43%** (text) vs. "**57% gradeable**" (Threats). Reversed. | High |
| N3 | Lessons 2 vs. Table 1 | Strict-matching undercount "**25.3pp**" vs. derivable strict–judge gap **6.4pp** (68.8−62.4). 25.3pp is not derivable from any reviewed number. | High |
| N4 | Finding 2 / Fig. 2 / Table 5 | Reduction factor **1,857×** vs. exact 81.7/0.04416 ≈ **1,849×** (11/24,907 = 0.04416%). Rounding artifact. | Medium |
| N5 | Specialization table vs. text/Table 1 | 3 × 500 = **1,500** samples vs. "full **n=2000** evaluation." Unexplained 500-sample difference. | Medium |
| N6 | Finding 5 / Fig. 5 | "Cross-agent corrections … cause **86% of downstream answer divergence**" — 86% is the divergence rate *within* 43 cross-agent entities, not a share of total harm. | Medium |
| N7 | Table 1 row "Cross-agent harm" | 73pp vs. 0.7pp presented as commensurable; different metrics, different n (11 vs. 300). | Medium |
| N8 | Finding 5 CI | 95% CI [76%, 96%] matches Wald; Wilson for 37/43 is **[72.7%, 93.4%]**. Understated uncertainty. | Medium |
| N9 | Reproducibility vs. Evaluation Summary | Reproduction script yields LongMemEval **58.3%**, headline is **68.8%** (10.5pp gap, different pipeline). | High (disclosed) |
| N10 | Reproducibility code comment | Temporal accuracy "MT 100% vs mem0 27.2%" appears nowhere else. | Low |

---

## Overall Recommendation

**Major Revision.**

The paper has genuine strengths: a transparent multi-dataset production analysis, a methodologically sound survival-analysis framing of memory lifetime, honest negative results (specialization F1 = 0.000, unanchored tamper miss, 58.3% standalone path), a fixed-seed pinned-version artifact, and findings (type-aware retention, cross-agent interception priority, consolidation-spike monitoring) that are actionable for JSS's practitioner audience. The Threats to Validity section is more candid than the genre average.

However, the paper cannot be accepted in its current state because:

1. **(Blocking, M1)** Headline numbers are internally inconsistent in ways reviewers can detect without access to the artifact (0.946/0.947, 43%/57% gradeable, unexplained 25.3pp). In a paper whose central contribution is empirical measurement, numeric self-consistency is a floor requirement.
2. **(M2, M3)** The most important comparative claim (+8.6pp over mem0 on LongMemEval) is neither independently reproducible (58.3% released path) nor measured under a single harness (mixed provenance in Table 1).
3. **(M4–M6)** The downstream-harm experiment and benchmark gains lack component attribution, judge validation, and appropriate CI methodology.
4. **(M7)** All findings derive from a single-user deployment; recommendation-level language must be conditioned accordingly.

Required for resubmission: fix all M1 items and all Number Check inconsistencies (N1–N10); release the EAF-pipeline evaluation path or demote the headline; present a single-harness comparison table; add a component ablation for English benchmarks; recompute CIs with exact methods; rewrite the r^N passage as a heuristic model with disambiguated notation; soften generalization claims. The MINOR items (m1–m20) should be addressed in a revision pass but are not independently blocking.

I thank the authors for the unusually complete artifact and disclosure posture; a carefully revised version of this work would be a solid contribution to the software-engineering-for-AI-agents literature.

---

*Review prepared for JSS (Journal of Systems and Software) editorial assessment. Ratings: 5 = accept, 4 = minor revision, 3 = major revision, 2 = reject with resubmission encouragement, 1 = reject.*
