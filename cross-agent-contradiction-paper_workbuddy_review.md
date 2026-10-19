# Peer Review: "When Agents Disagree: Measuring and Resolving Cross-Agent Memory Contradictions in Shared Multi-Agent Memory"

**Manuscript:** `cross-agent-contradiction-paper.tex`
**Review date:** 2026-10-19
**Reviewers:** R1 (Systems / NLP, academic), R2 (Applied ML / industry practitioner), R3 (Measurement / causal inference, methods)
**Recommendation target venue:** a systems-conference track (NeurIPS / ACL / ICML systems tracks).

---

## Editor's Summary

The paper makes four headline claims: (i) cross-agent contradiction rate in a real production multi-agent memory store is 0.044% (11/24,907 pairs); (ii) such contradictions cause a 73 percentage-point downstream accuracy loss; (iii) a contradiction-aware post-retrieval filter recovers +53.6pp on a 28-entity A/B test and a unified-condition experiment shows a 36.4pp recovery; (iv) a DistilBERT supersession-prediction model reaches macro F1 = 0.947 on a 2,635-record public benchmark, and MemTether beats mem0 by +15.5pp on LongMemEval and +17.9pp token-F1 on LoCoMo.

All three reviewers agree the topic is timely, the engineering footprint is substantial, and the artifact release is welcome. All three reviewers also identify **serious internal-consistency, statistical, and reproducibility problems** that must be resolved before the work is publishable in current form. The verdict spans major-revision across all three reports.

---

## Reviewer 1 — Systems / NLP (Academic)

**Overall score: 2 / 5 (major revision)**
**Confidence: high**

### Summary of strengths

- The artifact is open-sourced with a Makefile one-command reproduction, which is more than many papers in the area do.
- The four-category taxonomy (temporal flip / entity-polarity FP / self-agent temporal / needs human review) is a useful conceptual contribution and the rule tables are legible.
- The framing of "Memory Supersession Prediction" as a supervised task is interesting and could seed follow-up work.

### MAJOR concerns

1. **Self-contradictory headline number (abstract vs. body vs. tables).** The abstract asserts `F1 = 0.897 on ConflictBank (n=2000, precision 1.000)` and `F1 = 0.813 on a controlled benchmark`. The body (§``sec:specialization``) reports `F1 = 0.889 on temporal conflicts (500-sample subset, seed=42)`. Later (§``sec:learned``) the paper reports `Kimi-k2.6 achieves F1=0.583 ... while our TF-IDF achieves F1=0.986`. The reader cannot reconstruct which number corresponds to which evaluation. Either the abstract conflates two evaluations, or the body contradicts itself. The 0.986 vs. Table ``tab:feature-ablation``'s reported binary F1 of 0.984 for `TF-IDF + handcrafted` is plausible as the binary sub-score, but this is never stated.

2. **`n = 11` is too small to support the central causal claim.** The 73pp loss and the unified three-condition experiment (Condition A 9.1%, B 81.8%, C1 45.5%, C2 81.8%) are computed on **the same 11 rule-classified entities**. The paper acknowledges this in Limitations, but the abstract leads with "**45.5% accuracy (not just 9.1% stale-only)**" as if it were a population estimate. With 11 paired Bernoulli trials, the 95% Wilson CI for the C1-C2 difference spans tens of percentage points. The paper's claim that `Condition C1 represents a previously unquantified failure mode` is an over-strong generalization from `n = 11`.

3. **Asymmetry table (`tab:asymmetry`) is structurally suspect.** A 99.3% stale-only accuracy on 300 self-corrections is suspiciously close to ceiling; if true, it means self-corrections essentially never hurt downstream accuracy. This is a strong empirical claim with no mechanism explanation, and the protocols for the 11 cross-agent runs and the 300 self-correction runs are described in only one paragraph each. Without per-protocol details (how was "stale context" constructed, was the temperature zero, was the prompt the same), the comparison is uninterpretable.

4. **Inconsistent labeling.** Line 34 has two `\label` declarations (`sec:benchmark` and `sec:measure`) on the same scope. §``sec:supersession`` references `tab:supersession`, which is the label that actually points to the *memory-supersession-prediction* results table in §9. The unified-condition table in §8.3 has `\label{tab:unified}`, but the body text says "Table~\ref{tab:unified}" earlier expecting cross-source scan results. Readers relying on `\ref{}` will land on the wrong table.

5. **Citation claims that don't match the cited work.** `Letta` is cited via `[Packer et al., 2023, MemGPT, arXiv:2310.08560]`. While the MemGPT authors founded Letta, the paper should cite Letta's own documentation or release paper rather than its predecessor. Similarly the bibliography entry `[TOKI (2026)]` is attributed to "Anonymous," which is not a citation.

### MINOR concerns

- "Outperforming LLM detection ($F_1 = 0.113$)" — unclear on which dataset/task.
- "11,714× speedup" — compute units (CPU time, dollars, wall-clock) are never stated in the abstract or the relevant body section.
- `bibitem[Rasmussen et~al.(2025)]{zep}` is correct (MemGPT/Zep lineage), but the in-text "Letta~\cite{letta}" mapped to the `MemGPT` paper is a footnote trap.

### Recommendation

**Major revision.** Resolve numerical inconsistencies between abstract and body, expand `n = 11` analyses with confidence intervals and per-protocol description, distinguish the 0.986 single-task F1 from the 0.811 macro F1, and either enlarge the cross-agent contradiction corpus or downgrade the central causal claim from "**45.5%**" headline language to "case-study evidence."

---

## Reviewer 2 — Applied ML / Industry Practitioner

**Overall score: 2 / 5 (major revision)**
**Confidence: medium-high**

### Summary of strengths

- The engineering artifact (MemTether itself, the scan/classify pipeline, the synthetic DB with `Makefile`) is genuinely usable. I would download and try it.
- The headline numbers — 0.044% pair contradiction rate, 53.6pp retrieval A/B lift, 73pp downstream loss — are concrete and operationally meaningful.
- The supersession-discipline framing is good practitioner intuition: most production memory issues are not "every fact conflicts" but "specific high-churn entities."

### MAJOR concerns

1. **The contradiction detection pipeline is a moving target.** The scan script applies an `nf ≤ 30` filter that excludes 57 hub entities where "**contradictions concentrate**" (the paper's own words). The reported 0.044% is therefore explicitly described as a lower bound. The headline number in the abstract does not say this. A practitioner wanting to *use* this method on their own memory store must run both filtered and unfiltered scans and reconcile — there is no guidance.

2. **The "downstream loss" demonstration uses contexts that none of the 11 detected contradictions come from.** §``sec:methods`` explicitly states: "none of the 11 rule-classified contradictions from our systematic scan involve *packy*, making this a complementary case study rather than a direct validation of the scan results." That's fine for a case study, but the *Retrieval A/B test* (§``sec:retrieval``, +53.6pp) **also** uses 28 entities from the controlled benchmark, not the production-detected contradictions. So the two strongest "this filter helps in production" claims (the 73pp loss and the +53.6pp lift) both run on benchmark artifacts rather than on the 11 production-detected pairs. The pipeline is never closed on the very entities it was designed to detect.

3. **The contradiction-aware filter has a hidden oracle dependency.** The filter assumes that when two facts disagree, the newer `valid_from` is the correct one. In a real multi-agent setting this is not always true — agent B may have stale data and agent A may be the one writing the current truth. The paper never discusses this scenario, never measures accuracy of the recency heuristic, and presents the 53.6pp result as if it generalizes.

4. **Third-party benchmarks lack methodological symmetry.** §``sec:thirdparty`` reports `75.7% vs 60.2%` on LongMemEval but states the comparison is under "identical conditions (same hardware, same LLM judge, same 500-question benchmark)" without naming the hardware, the judge model version, or how "EAF" was configured. The 6.3pp gap between "judge (82.0%) and strict (75.7%)" is acknowledged in metric-bias §``sec:metric_bias`` but is folded into the headline 75.7% number. A more conservative reader would prefer the `68.8%` rerun number (October 18, 2026) be the headline.

5. **Free-tier API as production.** The LLM judge is `GLM-5.3-flash via local API (temperature=0)` accessed on a free tier. The paper acknowledges this as a limitation, but the downstream numbers (45.5% / 81.8% / etc.) come from this judge. If the free tier is non-deterministic, these numbers are not reproducible — yet they drive the paper's central empirical claim. A deterministic open-weight model (e.g., Qwen2.5-3B via vLLM) would remove this objection entirely.

### MINOR concerns

- `packy`-entity grading rubric (0 / 0.5 / 1) doesn't separate "wrong group recommended" from "refused to answer"; both are graded 0. Combined with n=3 runs per judge per condition, score variability is order ~17pp.
- Comparison with `Zep`, `Letta`, `LangMem` for "predicted accuracy" in Table ``tab:mapping`` is presented without any actual experiment; it's a thought-experiment mapping. Add a footnote clarifying this.
- `synthetic_memory.db` with 102 facts and 13 known contradiction pairs is small enough that 5-fold CV would be more robust than a single split.

### Recommendation

**Major revision.** Close the loop by running the post-retrieval filter on the 11 production-detected pairs (not just on a 28-entity controlled benchmark). Either match the third-party benchmark setup with named hardware/judge versions or report a conservative number. Replace free-tier API calls with reproducible open-weight or paid-tier settings, or explicitly annotate downstream numbers as "non-reproducible under paid-tier conditions."

---

## Reviewer 3 — Measurement / Causal Inference (Methods)

**Overall score: 2 / 5 (major revision)**
**Confidence: high**

### Summary of strengths

- The counterfactual analysis (Table ``tab:counterfactual``: with-vs-without supersession, both production and synthetic) is a clean design. Replaying supersession events in two modes (supersession / overwrite) lets the authors identify a causal effect, not just correlation.
- The synthetic DB plus production DB dual-track reporting is a strength — synthetic numbers are reproducible via `counterfactual.py` even when production numbers are not.
- The Wilson 95% CI for the 0.044% rate is appropriate to the sample size.

### MAJOR concerns

1. **The headline number (`F1 = 0.897`) is from a benchmark where the proposed method is structurally advantaged.** §``sec:specialization`` honestly reports F1 = 0.000 on semantic and misinformation conflicts. The detector is a *temporal-numeric overlap* detector, not a general contradiction detector. The abstract does not make this specialization clear. A reader who hears "F1 = 0.897 on ConflictBank" without reading §``sec:specialization`` will assume this is a general-purpose claim. This is selection-of-results bias in the abstract framing.

2. **Counterfactual numbers are not on the same scale.** Table ``tab:counterfactual`` juxtaposes production (1,768 facts, 11 → 23 contradictions) against synthetic (102 facts, 13 → 33 contradictions). The percentage prevented (52% vs 61%) is presented as if the two systems are comparable, but they are not — production entities average ~0.24 facts each, synthetic ~6.4 facts each. Supersession discipline is more impactful on dense synthetic data simply because there are more pairs to begin with. Reporting a single number ("52–61%") collapses these two effects.

3. **The "supersession vs. overwrite" comparison is not apples-to-apples.** §``sec:overwrite`` reports overwrite yields `0/24,907` contradictions because it deletes the conflicting fact. But it also reports `0 chains` because it deletes the old fact. The conclusion "supersession retains provenance at the cost of a nonzero contradiction rate" is correct as a trade-off statement, but the row labels in Table ``tab:overwrite`` give the reader the false impression that overwrite is dominant on contradictions: `Overwrite (prod) 1,420 11 348 chains` should read `Overwrite (prod) 1,420 0 0 chains`. The current cell actually does show `0` contradictions and `0` provenance for overwrite — but the column header "Provenance" only shows the chain count, not the percentage. Clarify or add columns.

4. **Expanded downstream validation lacks interpretation.** §``sec:expanded``: "Of 100 entities, 43 produced gradeable answer pairs. Stale context caused downstream answer divergence in 86% of gradeable entities (37/43, 95% CI [76%, 96%], binomial test $p < 0.001$)." This is the strongest empirical claim in the paper and is reported almost parenthetically. What were the other 57 entities, why weren't they gradeable, and what was the rubric for "divergence"? This deserves a subsection.

5. **Effect size estimate `Cliff's δ = 0.86` lacks a confidence interval.** For a paired-binary outcome with n=11, Cliff's δ can be computed exactly and a 95% CI is straightforward. Reporting a point estimate without CI is methodologically weak.

### MINOR concerns

- §``sec:disc`` ("Why the Rate Is Low") ism largely a re-statement of Section 4 and the Limitations bullet list. Could be tightened.
- The numerical CI `[28%, 95%]` for the 73pp difference (Limitations bullet 2) has unclear endpoint derivation — a binomial CI on the difference of two proportions with n=11 should span ~67pp wide; please publish the formula (e.g., Newcombe, Agresti-Caffo).
- `distilbert-base-uncased` is a 2019-era checkpoint. State whether any newer encoder was tried.
- Footnote: the DistilBERT fine-tune achieves `macro F1 = 0.947` on supersession but only `0.690` on ConflictBank — same model, same training pipeline, very different scores. The paper attributes the gap to "lexical-beats-semantic" but doesn't show ablations isolating encoder capacity from training-corpus leakage.

### Recommendation

**Major revision.** Rework the abstract to advertise the temporal specialization; expand §``sec:expanded`` into a full subsection with the rubric, CI method, and per-condition breakdown; report confidence intervals on all effect-size estimates; and reconcile the DistilBERT 0.947 vs 0.690 gap with a controlled ablation.

---

## Number / Citation Check

### Citation lookup (authoritative refs)

| Cite key | Claimed citation | Authoritative check | Status |
|---|---|---|---|
| `mem0` | Chhikara et al. 2025, arXiv:2504.19413 | Mem0 paper, April 2025 | ✅ Real |
| `zep` | Rasmussen et al. 2025, arXiv:2501.13956 | Zep paper, January 2025 | ✅ Real |
| `letta` | Packer et al. 2023, arXiv:2310.08560 — labeled "MemGPT" but cited as Letta | arXiv ID valid, but **content mismatch** | ⚠️ Mislabeled |
| `toki` | Anonymous, arXiv:2606.06240 | Bib entry authored as "Anonymous" — not a citable claim | ⚠️ Unattributed |
| `memstrata` | Yadav, arXiv:2606.26511 | June 2026 ID format plausible | ✅ Plausible (cannot verify w/o Web) |
| `sleeper` | Abdelnabi et al. arXiv:2605.15338 | May 2026 ID format plausible | ✅ Plausible |
| `agentpoison` | Chen et al. NeurIPS 2024 | Real paper exists | ✅ Real |
| `conflictbank` | Su et al. arXiv:2408.12076 | August 2024, real | ✅ Real |
| `fever` | Thorne et al. arXiv:1803.05355 | 2018, real | ✅ Real |
| `immutablepast` | HaddadPajouh et al. arXiv:2609.16073 | Sept 2026 ID | ⚠️ Future-month arXiv (plausible given Oct 2026 date) |
| `statefuse` | Volkov et al. arXiv:2607.05844 | July 2026 ID | ⚠️ Same as above |
| `pacmi` | Wang et al. arXiv:2610.05732 | Oct 2026 ID | ⚠️ Same |
| `revoked` | Shen et al. arXiv:2609.08258 | Sept 2026 ID | ⚠️ Same |
| `scopeaware` | Gu et al. arXiv:2610.09008 | Oct 2026 ID | ⚠️ Same |
| (LangMem) | cited in body w/o `\bibitem` | A full citation is missing in the bibliography | ❌ Missing |

### Numerical cross-checks

| Statistic | Where cited | Cross-check | Verdict |
|---|---|---|---|
| 73pp loss | Abstract, §6, §10 | 82% − 9% = 73 ✅ | ✅ |
| 53.6pp retrieval lift | §7, abstract | 96% − 43% = 53 (rounds to 53.6?) — recompute from raw cells | ⚠️ 96 − 43 = 53, not 53.6 — possible rounding, verify |
| 36.4pp recovery | §8.3 | 81.8% − 45.5% = 36.3 ≈ 36.4 ✅ | ✅ |
| +17.9pp token-F1 vs mem0 (LoCoMo) | abstract, §9 | 0.523 − 0.344 = 0.179 ✅ | ✅ |
| +15.5pp EAF on LongMemEval | abstract, §9 | 75.7 − 60.2 = 15.5 ✅ | ✅ |
| 87pp recovery | abstract, Intro | 81.8 − (−5.2)? Not present. Claimed abstract "recovers 87pp" — backing computation not visible in any table | ❌ Cannot verify |
| F1 = 0.897, P = 1.000 (n=2000) | abstract, §8.1 | Implied R = 0.897/(2−0.897) ≈ 0.813 ✅ | ✅ |
| F1 = 0.889 (500-subset) | §8.1 | P=1.000, R=0.800 → F1 = 0.889 ✅ | ✅ |
| F1 = 0.986 (TF-IDF binary, 100 subset) | §8.4 | Consistent with Table 8.4 binary F1 of 0.984 within rounding | ✅ Apparent |
| "0% (0/24,907)" after simulated `correct()` | §5.2 | Plausible (11/24,907 − 11/24,907 = 0) | ✅ |
| Counterfactual `11 → 23` (prod) | Table | `348 events replayed` — but the increase is 12, not 348. Many events must not reverse into the scanner's polarity-clash definition. ✓ but under-justified in text | ⚠️ |
| Counterfactual `13 → 33` (synth) | Table | 20 extra contradictions from 20 supersessions — i.e., every reverted supersession becomes a contradiction. Coincidence or filter artifact? | ⚠️ Needs explanation |
| Supersession prevented `52% / 61%` | Table | 12/23 = 52% ✓; 20/33 = 61% ✓ | ✅ |
| Cross-agent entropy Wilson CI `[28%, 95%]` | Limitations bullet 2 | Width seems plausible for a difference of two proportions with n=11 | ⚠️ State the CI method |
| `distilbert-base-uncased` macro F1 = 0.947 supersession, 0.690 ConflictBank | §9, §8.4 | Inconsistent same-model scores without an isolation ablation | ❌ Reconciliation required |

### Structural / LaTeX issues

- `\begin{thebibliography}{10}` sets label-width allowance for 10 entries but 14 are present. Entries with author prefixes longer than 10-character width will overflow the label column. **Minor.**
- Two `\label` keys (`sec:benchmark`, `sec:measure`) declared on line 34–35 — second is silently ignored by `\ref`. **Minor.**
- `\label{tab:unified}` is on the **Unified three-condition table** but is referenced in §``sec:measure`` ("Table~\ref{tab:unified}") where the cross-source scan results are expected. **Moderate** (figure-routing confusion).
- `\bibitem[Anonymous]{toki}` — this violates standard bibliography expectations. Replace with author list or use the venue's anonymous-track handling. **Minor.**
- Missing `\bibitem` for `LangMem` (cited in body text, §2, §10). **Minor.**
- Duplicate `\label{sec:production}` placed at line 229 outside any section header. **Minor.**

### Reproducibility audit

| Component | Claim | Verified against artifact |
|---|---|---|
| `Makefile` one-command reproduction | §3 (Reproducibility) | README exists; **not personally re-run by reviewers** |
| Synthetic DB contradiction counts | Table 5 | `counterfactual.py` claimed reproducible |
| ConflictBank n=2000 / n=1020 splits | §8 | Hashes in Table ``tab:hashes`` — cannot verify w/o artifact |
| Wilson 95% CI formula | Limitations bullet | Not specified |
| DistilBERT hyperparameters | §9 | α=0.25, γ=2.0, 3 epochs reported; seed not specified |
| Free-tier non-determinism | Limitations | Acknowledged but not mitigated |

---

## Aggregate Recommendation

**Major revision across all three reviewers (R1: 2/5, R2: 2/5, R3: 2/5).**

The paper is in a topic that the community needs and ships an artifact that is more rigorous than the median submission. However, before the work is publishable the authors must:

1. **Reconcile numerical inconsistencies** between abstract / body / tables (especially the 0.897 / 0.889 / 0.986 family and the unbacked "recovers 87pp" claim).
2. **Close the loop** between the 11 production-detected contradictions and the post-retrieval filter / downstream experiments (currently these run on different entities).
3. **Specialize the abstract** to make clear that `F1 = 0.897` is on temporal-only ConflictBank conflicts, not on general contradiction detection.
4. **Replace the free-tier API judge** with a deterministic open-weight alternative, or annotate downstream numbers as non-reproducible.
5. **Add confidence intervals** to all effect-size estimates (Cliff's δ, 73pp loss, 53.6pp lift), with the CI formula named.
6. **Expand §``sec:expanded``** from a paragraph into a full subsection with grading rubric and a per-condition breakdown.
7. **Fix citation hygiene**: replace `Letta` with `MemGPT` or cite Letta directly; add a `\bibitem` for `LangMem`; resolve `toki` anonymity; verify the 2026-dated arXiv IDs are real before final submission.
8. **Fix LaTeX label hygiene**: resolve duplicate `\label{sec:benchmark}/sec:measure}`, retarget `\ref{tab:unified}` to the correct table.

With these changes, the paper would make a useful contribution to the multi-agent memory literature. As written, it would mislead readers applying its claimed numbers outside the temporal-conflict scope.
