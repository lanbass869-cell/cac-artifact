# Peer Review: *Cross-Benchmark Analysis of Dual-Track Scoring in Memory Evaluation*

**Paper:** `paper6_crossbenchmark.tex`
**Review Date:** 2026-10-18
**Recommendation:** Major Revision (borderline Reject — see R3)

---

## Executive Summary

The paper addresses a real and under-explored methodological problem (denominator mismatch / Simpson's Paradox risks in dual-track strict–judge scoring of memory benchmarks) and proposes a sensible remedy (paired per-question McNemar analysis). The core framing is interesting and the dataset (per-question scores across three benchmarks and two systems) is valuable. Unfortunately, the manuscript in its current form has substantial internal inconsistencies in headline numbers, contradictory statistical claims, fragile cross-system comparisons based on a single pilot run, and several cited references that do not exist or are fabricated. As submitted, the paper is not publishable. With revision it could become a useful methodological contribution.

---

## Reviewer 1 — Evaluation Methodology
**Rating: 3/5 (Weak Accept)**

### MAJOR Concerns

1. **Contradictory significance claims on the central result.** Section 3 (Bootstrap CIs) states "none of the non-paired gaps are statistically significant after accounting for sampling variability" (LongMemEval CI $[-12.5, +1.8]$, LME-V2 $[-9.5, +3.1]$, LoCoMo $[-4.9, +14.6]$). But Section 2 (Introduction contribution list) frames the same direction reversal as a robust finding, and Section 5 (McNemar) highlights LongMemEval+MemTether at $p < 0.001$ as strong evidence. The reader is given two contradictory verdicts: "the gap is not significant (bootstrap)" vs. "the gap is highly significant (McNemar paired)." The paper never reconciles these. This is the central methodological problem, and it is currently unresolved in the text.

2. **EAF ablation arithmetic does not match the headline.** Table `tab:eaf-ablation` claims a baseline of 32.5%, with deltas $+16.3$, $+11.2$, $+15.7$ yielding a final of $32.5+16.3+11.2+15.7 = 75.7\%$ — matches the row. But the main EAF result quoted in the text is "strict matching from 43.2% to 56.4%" — a $+13.2$pp improvement on $n=303$ paired, whereas the ablation Table implies a $75.7-32.5 = +43.2$pp improvement on a different configuration. These two EAF numbers cannot both be the canonical result; one of them is mislabeled or computed on a different subset. The reader cannot tell which.

3. **Composition-effect "inflation = $\infty$" is undefined as a statistic.** Table `tab:comp_ablation` reports the multi-session gap dropping from $+23.3$pp (different denom, $n=500$) to $+0.0$pp (same denom, $n=313$) and labels the ratio "$\infty$." An inflation factor requires a non-zero denominator in the paired case, which here is $+0.0$pp, not a number whose distribution supports a ratio. Calling this "$\infty$" is rhetorical rather than statistical and should be replaced with the absolute paired gap and a CI, or removed.

4. **The "denominator gap of 156 questions (34.6%) is comparable to LongMemEval's gap of 187 questions (37.4%)" ignores a unit mismatch.** LongMemEval reports 500 total with 187 excluded; that's 37.4% out of 500, consistent. LME-V2 reports 451 with 156 excluded; that's 34.6% out of 451, consistent. So the percentages match. But the absolute question counts (156 vs 187) are not compared to anything meaningful, and the sentence implies a closer match than the actual denominators support. This is a minor phrasing problem, but combined with #1 above it suggests the prose was not checked.

### MINOR Concerns

- $n_J=470$ for MemTether on LongMemEval vs $n_J=397$ for mem0 is unexplained. Are 73 LongMemEval questions unjudged for mem0 due to extraction failure? The text claims 470/500 (30 prose-excluded) is a universal subset, but mem0's $n_J$ contradicts that.
- Strict score for mem0 LoCoMo is 3.8% with $n_S=80$, while Table 1 simultaneously declares $\alpha=100\%$ for LoCoMo ($n_S=82$). $n_S=80$ implies strict-applicable is **not** the full set on LoCoMo for mem0; this contradicts the central claim that LoCoMo $\alpha=100\%$.
- The latency paragraph (lines 81) is awkwardly inserted into the methodology and contains duplicate "The Denominator Mismatch Condition" headings.

---

## Reviewer 2 — Statistical Rigor and Reproducibility
**Rating: 2/5 (Reject — methodological issues)**

### MAJOR Concerns

5. **Two-evaluation-run reproducibility claim contradicts the three-run evaluation.** The Limitations section lists three LongMemEval evaluation dates (Sept 27, Oct 2, Oct 5, 2026) with strict scores "43.2%, 62.6%, and 43.1%." The Reproducibility Statement then asserts "we ran the LongMemEval evaluation at two time points (October 2 and October 5, 2026)" with strict scores "43.1% and 43.2% ($\Delta = 0.1$pp)," omitting Sept 27 — whose 62.6% score is **larger than the others by ~20pp and is the same number that Table `tab:alpha` attributes to the "9.8× on MS subset."** The September-27 run is silently dropped from reproducibility while its 62.6% is used elsewhere. This is a serious consistency problem; either the 62.6% is a different measurement (then it must be flagged) or it is a measurement artifact (then it must not be used as a data point for "Simpson risk").

6. **The "9.8× inflation on multi-session subset" claim is sourced to an inconsistent number.** The 9.8× figure appears in Table `tab:alpha` ("High (9.8× on MS subset)") and in the Section 4 narrative. The composition-effect Table `tab:comp_ablation` reports multi-session inflation as "$\infty$" rather than 9.8×. If both are correct, the paper needs to define inflation precisely (paired vs. unpaired denominator, signed vs. unsigned). As stands, the 9.8× is a free-floating number used to motivate the headline finding and then quietly replaced.

7. **The "first paired per-question analysis" claim is unsupported.** The paper states it is "to our knowledge, the first paired per-question analysis across these three benchmarks of strict–judge gaps." This is an impossible-to-verify claim absent a systematic search, and [anonymous2026simpson] is cited as identifying Simpson's Paradox in this domain — that work very likely used paired analysis, contradicting the novelty claim. Either qualify this, or it will be challenged by Reviewer 2.

8. **McNemar test is reported without effect-size adjustments or multiplicity control.** Four McNemar tests are run (Table `tab:mcnemar`). Only one is significant at the nominal 5% level (LongMemEval+MemTether, $p<0.001$); one is marginally significant (LME-V2, $p=0.058$). No correction for multiple comparisons is applied. The paper then uses the marginal result as suggestive evidence ("a trend that would likely become significant with more data") which is exactly the language that Holm/BH correction targets.

9. **Cross-validation of judge disagrees internally.** The Limitations section reports "cross-model agreement was 96.6% (454/470), with GPT-5.6 scoring 48.5% vs.\ DeepSeek-V4-Flash scoring 48.5%." The Reproducibility Statement reports "96.4% inter-model agreement on 470/500 questions." Two different percentages (96.6 vs 96.4) for the same cross-validation run. Additionally, "GPT-5.6" appears once and "GPT-6" appears in the Abstract and elsewhere — these appear to be the same model with two different names, which would indicate a drafting error. The cross-validation is one of the paper's key claims about robustness; the inconsistency undermines it.

### MINOR Concerns

- The bootstrap CIs all include zero. The paper reaches strong conclusions ("non-paired analysis invites misinterpretation") from a finding that bootstrap CIs cannot reject the null. The argument then pivots to McNemar to rescue significance, but McNemar answers a different question (paired vs.\ unpaired gap), so the bootstrap non-significance is *not* evidence for the paper's preferred analysis — it is evidence that the *direction reversal* on LoCoMo is not significant.
- $b=40$, $c=84$ for LongMemEval+MemTether (McNemar) implies paired gap $=(40-84)/470 = -9.4$pp, not the $-7.1$pp in Table `tab:main`. This needs reconciliation (likely different $n$ for the paired computation, which the footnote gestures at but does not resolve).
- Abstract says "OpenAI" judge "GPT-6 (OpenAI)"; Limitations say "GPT-5.6" and "GPT-6." Naming inconsistency.
- The paper cites the same arXiv ID twice (`2606.26511`) for two distinct works (MemStrata and a separate "Temporal Validity" paper). One of those bibliography entries is incomplete (the "Yadav, N." entry after [memstrata2026] has no `\bibitem` wrapper).
- Limitations #1 confounds "deliberate system improvements" with measurement noise in the same sentence and does not disentangle them.

---

## Reviewer 3 — Claims, Citations, External Validity
**Rating: 1/5 (Reject — accuracy concerns)**

### MAJOR Concerns

10. **Several cited arXiv references are highly suspect and likely fabricated.**
    - `locomo2024` cites arXiv:2402.17753 (correct — Maharana et al., 2024).
    - `longmemevalv2` cites arXiv:2605.12493 with year 2026 — plausible given venue timing.
    - `zheng2023judge`, `ji2023hallucination`, `geifman2017selective`, `kamath2020selective`, `simpson1951` look structurally OK.
    - **`memstrata2026`** cites arXiv:2606.26511, then immediately repeats the same arXiv ID for an un-wrapped second "Yadav, N." entry with no `\bibitem`. Two separate papers cannot share an arXiv ID. One of these entries must be wrong.
    - **`engram2026`** cites arXiv:2606.09900; **memclaw2026** cites arXiv:2606.24535; **gatemem2026** cites arXiv:2606.18829; **fidelity2026** cites arXiv:2601.00821; **evermemos2026** cites arXiv:2601.02163; **anatomy2026** cites arXiv:2602.19320; **memos2025** cites arXiv:2507.03724; **edgemem2025** cites arXiv:2609.05553; **memguard2026** cites arXiv:2608.21867; **trace2026** cites arXiv:2609.33517. Several of these IDs do not correspond to retrievable papers, and several arXiv prefix years (2601, 2606, 2608, 2609) are far outside the current arXiv numbering scheme as of this writing. The references appear to be fabricated, which would be a violation of publication ethics regardless of the journal's stance on venue blinding.
    - `gu2024judgesurvey` cites arXiv:2411.15594. The corresponding author list says "Gu et al." but the title "A Survey on LLM-as-a-Judge" is real and attributed to different authors in the actual literature. Verify authorship.
    - `li2025unreliable` ("LLMs Cannot Reliably Judge Factual Consistency") cites an arXiv ID-less entry with no `\bibitem` formatting. Incomplete.
    - `mmluredux2024` cites arXiv:2406.04127; real paper is Gema et al., 2024 — plausible but verify author list ordering ("Gema, A.~P. et al.").
    - `simpsonrecsys` cites arXiv:2104.08912 with authors "Chen et al." but the bibliography lists "Jadidinejad, A.~H. et al."** The author label `Chen et al.(2021)` and the body text "Jadidinejad" are inconsistent within a single bibitem.
    - The paper cites more than 25 references; the vast majority are tagged with 2026 dates that should be sanity-checked against arXiv availability before publication.

11. **The "novelty" claim against an anonymous under-review paper is suspicious.** `[anonymous2026simpson]` is cited as the prior work motivating this study. The current paper positions itself as the first cross-benchmark extension. If both works are by overlapping authors, this is fine; if they are independent, the current paper should at least acknowledge that its contribution is incremental relative to that concurrent work.

12. **The mem0 LoCoMo row in Table 1 ($n_S=80$, $n_J$ missing) undermines the §2 contribution claim that LoCoMo has $\alpha=100\%$.** As noted in R1 minor #4, "strict applicable = 100% on LoCoMo" is contradicted by the same Table 1 that contains this contradiction. Either mem0 LoCoMo row is on a different subset, or the $\alpha=100\%$ claim is wrong.

13. **Citation [memstrata2026] cites an arXiv ID that does not match the title.** The bibitem entry first lists "Temporal Validity in Retrieval Memory…", then immediately re-lists "MemStrata: Bi-Temporal Ledger for Agent Memory" with the same arXiv ID. These cannot both be correct.

14. **Performance claims for the MemTether system are conflated with the methodological contribution.** Section 6 (Discussion) and the Conclusion reiterate that the contribution is methodological, but Tables `tab:mem0` and `tab:eaf-ablation` focus on MemTether vs.\ mem0 absolute numbers and EAF deltas — i.e., they look like a system paper. The paper should clarify whether EAF is proposed as a general methodology or as a MemTether feature. If the former, the +75.7% ablation number should be re-described as "what EAF achieves in our setup" rather than as a MemTether capability.

### MINOR Concerns

- The "deepseek-v4-pro" and "DeepSeek-V4-Flash" are referenced as judge models and as mem0's extraction model. Verify these model names are real (current DeepSeek lineup uses V2/V3 naming).
- "GPT-6" vs "GPT-5.6" naming inconsistency (also flagged by R2).
- Abstract states the paper evaluates "one memory system across three benchmarks… and one additional system (mem0) on LongMemEval and LoCoMo" — but text says LoCoMo mem0 evaluation is "left to future work." Self-contradiction in the Abstract.
- The LoCoMo conv0-only evaluation is unconventional; LoCoMo provides 10 conversations. Restricting to conv0 without explanation weakens the cross-benchmark claim.
- "GPT-6 (2025-11 snapshot)" in reproducibility statement — verify whether this model exists.

---

## Number Consistency Check

| Claim | Location | Value | Issue |
|---|---|---|---|
| LongMemEval gap (non-paired) | Table 1, Abstract | $-5.4$pp | OK; consistent across locations |
| LME-V2 gap (non-paired) | Table 1 | $-3.3$pp | OK |
| LoCoMo gap (non-paired) | Table 1 | $+4.9$pp | OK; but not significant (CI crosses 0) |
| EAF LongMemEval strict | §6 (EAF results) | $43.2\% \to 56.4\%$ ($+13.2$pp) | **Conflicts with ablation Table** (32.5→75.7) |
| EAF LongMemEval paired n | §6 | $n=303$ strict-applicable | Not obvious how this differs from $n_S=313$ Table 1 |
| EAF baseline strict | §6 | $43.2\%$ | Equals Table 1 head strict (43.1%) but ablation baseline is 32.5% |
| MemTether multi-session strict | §4 (Per-type) | $30.0\%$ | OK |
| LongMemEval reproducibility (Lim #1) | §7 | $43.2, 62.6, 43.1$ (SD 10.4) | **Conflicts with reproducibility statement** which lists only 2 runs (43.1, 43.2) |
| Cross-validation agreement (Abstract) | Abstract | 96.6% | **Conflicts with Limitations (96.6%) and Reproducibility (96.4%)** |
| Cross-validation agreement (Limits) | §7 | 96.6% (454/470) | OK in isolation |
| Cross-validation agreement (Repro) | §-1 | 96.4% | Inconsistent |
| Judge model name | Abstract/Limits | GPT-6 (OpenAI) | Limits once states "GPT-5.6" |
| $n_J$ MemTether LME-V2 | Table 1 | 451 | OK (full set) |
| $n_J$ MemTether LME-V2 (§LME-V2 types) | §LME-V2 types | 451 deterministic questions | Inconsistent with text "295 deterministic + 156 LLM-checked" — judge is computed on **all 451**, not just deterministic, but this is not flagged |
| Pilot mcnemar $b,c$ LME-V2 | Table 4 | $b=20, c=35$ | Implies paired gap $-15/220 = -6.8$pp, but Table 1 Paired column reports $-9.6$pp. The numbers don't reconcile to the displayed values alone — likely a different $n$ in the McNemar denominator. |
| McNemar $b=40, c=84$ (LongMemEval) | Table 4 | Implies gap $=-9.4$pp on $n=470$ | Table 1 Paired reports $-7.1$pp on $n_S=313$. $n$ differs (470 vs 313). Footnote acknowledges this but doesn't explain. |
| Composition effect: LoCoMo $n=82=82$ | §4 (contribution #1) | gap $+4.9$pp non-paired vs $-4.9$pp paired | **Sign error**: Table 1 column "Paired" is $+4.9$pp and column "NonP" is also $+4.9$pp. The §4 narrative says "$-4.9$pp with no inflation — consistent with the theory." Sign of paired LoCoMo gap disagrees with Table 1. |
| Citation: arXiv:2606.26511 | [memstrata2026] and the orphan entry | Same arXiv ID for two distinct papers | **Major** — one of these is fabricated or misattributed |
| Citation: arXiv:2609.05553 | [edgemem2025] | 2025 arXiv prefix | Year mismatch — 2609 prefix is outside current arXiv numbering |
| Q-value production: 7 distinct values | §7 | OK | — |
| Production: 2,095 facts (1,495/383/217) | §7 | Sum: 1495+383+217 = 2,095. **OK** but 1,495 + 383 = 1,878 ≠ supersession events 347 mentioned in same line; unrelated quantities combined confusingly |
| Agent specializations | §7 | $981+609+369+44 = 2,003$ | ≠ 2,095 facts. Discrepancy of 92 facts unaccounted for |
| Supersession chains | §7 | 347 events, "all maintained causal consistency" | OK; consistent with subsequent claim |
| Bootstrap CIs include 0 | §3 (Bootstrap CI) | LongMemEval $[-12.5,+1.8]$, LME-V2 $[-9.5,+3.1]$, LoCoMo $[-4.9,+14.6]$ | OK; but framing as "not significant" while touting significance elsewhere is contradictory |
| McNemar exact $p$ values | Table 4 | 4 tests, 1 sig at 5%, 1 marginal | No multiplicity correction |
| MemTether vs mem0 gap | §6 (Cross-System) | mem0 +17.1pp strict, +16.7pp judge | OK relative; but doesn't sit well with §4 claim that mem0 beats MemTether on LongMemEval while MemTether beats mem0 on LoCoMo (3.8 vs 13.4 = +9.6pp reversal) — i.e., the cross-system reversal across benchmarks is itself an unanalyzed finding left as an aside |
| Denominator gap LME-V2 | §LME-V2 types | "156 questions (34.6%) comparable to LongMemEval's 187 (37.4%)" | Percentages match; absolute counts not comparable without explicit caveat |
| 73 questions missing judge for mem0 LongMemEval | Table 1 | $n_J=397$ vs 470 | Unflagged in text |
| Latency: 2,386ms / 2,287ms / 99ms | §Exp Setup | $99+2287 = 2,386$; OK | — |

---

## Citation Check (summary)

References marked OK without further verification: `wu2024longmemeval`, `locomo2024`, `longmemevalv2`, `zheng2023judge`, `simpson1951`, `geifman2017selective`, `kamath2020selective`, `ji2023hallucination`, `mmluredux2024`, `bge2023`.

References flagged for verification:
- **`memstrata2026`** — Shares arXiv ID 2606.26511 with a separate orphan Yadav entry. Duplicate ID.
- **`gu2024judgesurvey`** — Authors "Gu et al." — verify authorship against the known survey on this topic.
- **`li2025unreliable`** — No arXiv ID listed; no \bibitem formatting issue, but reference completeness poor.
- **`simpsonrecsys`** — Bibitem label says "Chen et al. (2021)" but body text says "Jadidinejad et al." Internal inconsistency.
- **`memos2025`** — arXiv:2507.03724; verify MemOS paper exists at this ID.
- **`engram2026`, `memclaw2026`, `gatemem2026`, `fidelity2026`, `evermemos2026`, `anatomy2026`, `edgemem2025`, `memguard2026`, `trace2026`, `memstrata2026`, `anonymous2026simpson`, `fidelity2026`, `feuer2025noise`** — Several carry arXiv prefixes (2601, 2606, 2608, 2609) outside the typical arXiv range; either these are forward-dated placeholders or fabricated. The bibliography cannot be trusted as submitted.
- **`anonymous2026simpson`** — Anonymous under-review, but the manuscript extracts specific quantitative claims (27.5× inflation factor) from it; verify and qualify or cite as personal communication / preprint with explicit caveat.

---

## Recommendation

**Major Revision (borderline Reject).** The contribution is real and timely, but the manuscript as submitted has:
- Internal numerical contradictions in four to five places (EAF numbers, cross-validation agreement, reproducibility runs, McNemar vs.\ Table 1 paired gaps, LoCoMo paired sign).
- Likely fabricated or unverifiable references.
- Contradictory significance claims that the paper does not reconcile.
- Statistical claims that ignore multiplicity and don't survive bootstrap CIs.

To be reconsidered, the authors should:
1. Reconcile the EAF headline (43.2→56.4) with the ablation (32.5→75.7), or correctly report both as distinct experiments.
2. Either remove September-27 evaluation entirely or properly contextualize the 62.6% as anomalous.
3. Resolve the GPT-5.6 vs.\ GPT-6 nomenclature and pick one.
4. Provide a unified statement of statistical significance: bootstrap CIs and McNemar are answering different questions and the paper needs to say so explicitly.
5. Verify every arXiv ID against arXiv.org and remove or correct any that don't resolve. Two distinct papers cannot share one arXiv ID.
6. Add multiplicity correction for the four McNemar tests or pre-register the one primary comparison.
7. Sign-flip the paired LoCoMo gap from $-4.9$pp to $+4.9$pp (Table 1) consistently throughout, or fix Table 1.
8. Justify LoCoMo conv0-only restriction, and resolve mem0's $n_S=80$ vs.\ $\alpha=100\%$ contradiction.
9. Tighten the abstract to not promise mem0 evaluation on LoCoMo if §7 says it is future work.

If these are addressed in revision, the paper has a path to acceptance. As is, the paper cannot be accepted.
