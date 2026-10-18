# Peer Review

**Paper:** *Memory Dynamics in Production Multi-Agent Systems: A 30-Day Longitudinal Study of Shared Agent Memory* (`memory-dynamics-paper.tex`)

**Review structure:** Three independent reviewer reports (R1 methodology/technical soundness, R2 evaluation quality, R3 practical impact/generality), followed by a consolidated concern list with severities and fixes, a full consistency check (numbers + citations), and an overall recommendation.

**Paper summary:** The authors present a 30-day observational study of a single-machine production deployment of MemTether, a shared SQLite-backed agent memory system serving 15 AI clients. From 3,000 logged operations they derive five findings: (1) memory type predicts correction rate (procedural 91.5% vs. decisions 8.2%, ~11×); (2) raw cross-agent polarity clashes (81.7%) reduce to 0.044% genuine temporal contradictions after filtering (a claimed 1,857× reduction); (3) corrections cluster — one system-mediated consolidation event accounts for 262/349 (75.1%); (4) injection coverage is 0.48% (209× overscan); (5) cross-agent corrections (14.9% of total) cause disproportionate downstream answer divergence (86% vs. 0.7% for self-corrections). They close with three design principles: type-aware retention, entity resolution before conflict detection, and write-time cross-agent interception.

---

## Reviewer Reports

### R1 — Methodology and Technical Soundness

| Dimension | Score (1–5) |
|---|---|
| Originality | 4 |
| Scientific importance | 4 |
| Technical soundness | 2 |

**Strengths**

1. The measurement target — temporal dynamics of shared memory in a real production deployment — is genuinely absent from the cited literature; static benchmarks (LongMemEval, LoCoMo) indeed cannot capture aging, staleness, or correction dynamics. The niche claim ("no published study...") is credible.
2. Measurement discipline is above average: read-only analysis, hash-chained append-only audit log, bi-temporal schema, and repro commands with expected outputs (§Reproducibility). Honest limitation statements — informative retirement censoring is explicitly flagged in §Survival, and the polarity detector's false-positive direction in §Limitations.
3. Kaplan–Meier framing (correction = event, still-active = right-censored) is an appropriate formalization of memory lifetime, and the informative-censoring caveat shows sophistication.

**Weaknesses**

1. **The consolidation confound is unaddressed (most serious).** Finding 3 establishes that 262/349 (75.1%) of corrections came from a single bulk `nrem_consolidation` event on 2026-09-27. Yet Finding 1's per-type correction rates and the KM curves (§Survival) are computed over *all* corrections, including this event. If the bulk process preferentially targeted stale procedures — plausible, since bulk cleanup targets stale content and the paper itself argues procedures go stale fastest — then the 91.5% rate and the 2.5-day median survival are partially artifacts of one batch job. No sensitivity analysis excluding the 262 event corrections is reported. This is the single most important missing analysis: it could either confirm or materially weaken the headline finding.
2. **The superseded-rows vs. edges footnote is mathematically impossible as stated.** Footnote 2 of Table 1 says the 386-superseded-rows vs. 349-edges gap "arises from multi-step chains where one edge supersedes a fact that was itself already superseded." Under the stated DAG semantics each edge marks exactly one old row, so distinct superseded rows ≤ edges always (a chain A→B→C contributes two edges and two rows). 386 > 349 therefore cannot arise from chains; it implies ~37 rows marked `superseded` without a corresponding edge (or a different mechanism). The explanation is backwards and must be replaced with the real one.
3. **The survival risk set n=2,309 is not reconstructable.** 349 events + 1,960 censored = 2,309, but no combination of Table 1 quantities yields this: active 1,957 + superseded 386 = 2,343; + retired 200 = 2,543; typed total (Table 2) = 2,590. The risk-set definition (created-within-window? retired excluded? type IS NULL excluded?) must be stated precisely.
4. **"Correction" denotes two different quantities.** Table 2 / Finding 1 count status-based corrections (column sums to 386), while Findings 3 and 5 (and the abstract's "349 corrections") count supersession *edges*. The per-type rates are therefore not the same quantity as the corrections discussed elsewhere. One harmonized definition — or both, clearly labeled with a 386-vs-349 reconciliation — is required.
5. **The 1,857× reduction is an apples-to-oranges ratio.** The numerator (81.7%) comes from a 2,000-pair *sample* of one agent pair (codex–workbuddy) at fact-pair level; the denominator (11/24,907 = 0.044%) covers a different, larger population at entity-pair level. The ratio is also computed from rounded figures (0.817/0.00044 ≈ 1,857; unrounded ≈ 1,850). Neither the population mismatch nor the rounding is disclosed. Contribution 3 further mislabels it a "false-positive rate" — it is a reduction factor.
6. **Downstream experiment statistics.** The 95% CI [76%, 96%] for 37/43 matches a Wald interval; the exact (Clopper–Pearson) interval is ≈[72%, 95%]; the method is unstated. The binomial null of 50% divergence is arbitrary — 50% is not a meaningful baseline for "does stale context change the answer"; the meaningful baselines are the self-correction condition or zero. Most importantly, the self-correction arm (0.7%, n=300) has **no methods description anywhere**: how were 300 entities selected when only 284 self-correction events exist? As written, this number is unverifiable.
7. **Grader validity.** The third-LLM-call grader (GLM-5.3-flash, temperature 0) that decides "divergence" is unvalidated: no human-labeled subsample, no agreement statistic. Since divergence is the paper's harm measure for Finding 5, grader validity is load-bearing.
8. **Broken text in §4.3 (Finding 2).** A duplicated editing artifact: "At the cross-source pair level (24,907 pairs), after applying the full classification pipeline on the shared entity (e.g., one agent writes...). However, after applying the full classification pipeline (...)" — the sentence is fragmented and the parenthetical example is stranded mid-sentence. Must be rewritten.

**R1 verdict:** A novel and worthwhile measurement study, but the central finding is confounded by the paper's own Finding 3, several bookkeeping numbers are inconsistent or unreconstructable, and one experimental condition is undocumented. Not technically sound as submitted.

---

### R2 — Evaluation Quality

| Dimension | Score (1–5) |
|---|---|
| Originality | 4 |
| Scientific importance | 3 |
| Technical soundness | 2 |

**Strengths**

1. Evaluating on production data rather than static benchmarks is exactly the right move, and each finding is operationalized into a concrete, checkable metric. The repro commands with expected outputs (§Reproducibility) are exemplary.
2. Finding 2's funnel design (raw clash rate → filtered contradiction rate) is a clever quantification of how misleading naive entity matching is, and the paper appropriately resists over-claiming (the 3-day TTL is explicitly labeled a hypothesis, not a validated recommendation).

**Weaknesses**

1. **No baseline or comparison point.** All rates (91.5%, 0.48%, 86%) are properties of one system. The paper could situate them against published dynamics from mem0/Zep/Letta, or against itself with the consolidation event excluded. Without any comparison, there is no way to judge whether any number is typical or idiosyncratic to this deployment.
2. **A single agent pair drives the headline clash rate.** The 81.7% raw clash rate is measured only between codex and workbuddy (the repro command confirms `--source1 codex --source2 workbuddy`), yet the abstract states it as a property of "cross-agent fact pairs" generally. With 15 sources available (105 pairs), the pairwise matrix should be reported, or the claim narrowed to "the codex–workbuddy pair."
3. **Metric consistency.** "Corrections" = 386 (Table 2 sum) vs. 349 (events) in different sections. "Divergence" — a symmetric difference in answers — is repeatedly glossed as "harm." Divergence is necessary but not sufficient for harm: two divergent answers can both be acceptable paraphrases. No human judgment of which answer was *wrong* is reported, so "86% downstream harm" overstates what was measured (86% answer divergence).
4. **Attrition bias in the downstream experiment.** 57% of the 100 entities (57/100) returned empty responses due to API content filtering and were dropped. If filter-triggering entities differ systematically (e.g., more sensitive/ambiguous content), the 86% estimate is biased in an unknown direction. At minimum, compare dropped vs. retained entities on available covariates; better, report divergence on all 100 with empty responses handled explicitly.
5. **Statistical reporting gaps.** No CI for the 81.7% clash rate (n=2,000 → ±1.7pp at 95%); no log-rank test for the KM curves (only one pairwise chi-squared is reported); the "209×" and "1,857×" factors are computed from rounded inputs; no multiple-comparison discussion even though at least five headline tests are run.
6. **Finding 4's equivalence claim is unsupported.** "Improving retrieval by 1% is equivalent to storing 2× more memories" is asserted with no experiment, no model, and no citation. It does not follow from the coverage ratio alone. Either derive it formally or delete it.
7. **Finding 4 is also close to tautological as presented.** 0.48% coverage is largely determined by the designer's chosen injection cap (3,980 chars) relative to accumulated corpus size — the finding is real but its interpretation ("retrieval quality is the binding constraint") needs the retrieval-quality evidence that is deferred to future work.

**R2 verdict:** Right evaluation target, honest reproducibility, but no baselines, single-pair generalization of the clash rate, undocumented experimental arm, and attrition bias undermine confidence in the headline numbers.

---

### R3 — Practical Impact and Generality

| Dimension | Score (1–5) |
|---|---|
| Originality | 4 |
| Scientific importance | 3 |
| Technical soundness | 3 |

**Strengths**

1. The three design principles (type-aware retention, entity resolution before conflict detection, write-time cross-agent interception) are actionable and directly traceable to measured quantities. The buffer-pool analogy for Finding 4 is apt and communicates the retrieval-quality argument well.
2. The deployment description is unusually candid for this genre: named hardware, WAL mode, junction/symlink sharing mechanism, MCP client interface, PyPI version pin, and an artifact repository with a synthetic data generator. This is more deployment validity than most agent-memory papers provide.
3. Limitations are honestly stated: single deployment, single operator, irreproducible private data, short window, rule-based polarity detector, single machine.

**Weaknesses**

1. **n-of-one operator.** All 15 "clients" are AI clients operated by one person on one machine, in one usage style. The paper concedes this, but the abstract's framing ("production multi-agent systems") invites over-general reading. The claim "no published study has characterized how shared agent memory evolves in production" is fair, but "production" here means a single-user hobby/prosumer deployment; the title and abstract should calibrate (e.g., "a single-operator production deployment").
2. **Zero workload characterization.** No data on what the 15 clients actually were, what domains the memories covered, write frequency per client, or how usage evolved. Without this, readers cannot judge whether 91.5% procedure correction is a property of memory systems or of this operator's workflow (e.g., heavy tool-configuration churn).
3. **The 2026-09-27 consolidation event limits generality of Findings 1, 2(?), and 5.** Organic corrections number only 87 over 30 days (~2.9/day). Every per-type and per-source statistic built on 349 events is dominated by one batch process. Generality claims should be restated on the organic subset — which is small enough that most findings would become hypotheses rather than results.
4. **Design recommendations outrun the evidence in places.** "Cross-agent interception at write time" is justified by the harm asymmetry, but the paper never measures the false-positive cost of write-time interception (which, per Finding 2's own funnel, would be severe: ~99.96% of raw polarity clashes are not genuine contradictions). The recommended design principle therefore conflicts with the paper's own Finding 2 unless interception uses the full semantic pipeline — this tension is never discussed.
5. **Companion-paper dependence.** Findings 2 and 5 are "reported in full detail in our companion paper" — for a self-contained paper, key methods (classification pipeline stages, downstream protocol) live outside the artifact under review. Reviewers of this paper cannot fully verify two of five findings.
6. **Citation-integrity risks.** Two references are "Anonymous (2026)" including one arXiv-style entry (2606.24535) that cannot be verified; the MemTether citation is also self-referential/anonymous. These should be replaced with real, verifiable citations or the claims attributed to the companion paper by title.
7. **Timeline oddity.** The study window is 2026-09-13 to 2026-10-14, and several citations are dated 2026 — internally consistent, but reviewers should note the field is fast-moving and the related-work section is thin (eight references, one paragraph).

**R3 verdict:** Genuinely useful practitioner signals with above-average transparency, but generalizability is limited to single-operator deployments, and the write-time-interception recommendation is in unexamined tension with the paper's own entity-resolution finding.

---

## Concerns

### Major concerns

| # | Concern | Section(s) | Blocking | Suggested fix |
|---|---|---|---|---|
| M1 | Consolidation confound: Finding 1 rates and KM curves include the 262 system-mediated corrections from the 2026-09-27 bulk event | §4.1, §4.2, Finding 3 | **Yes** | Recompute Table 2 and KM curves excluding `nrem_consolidation`-originated corrections; report both versions; revise claims if the effect shrinks |
| M2 | Footnote 2's chain explanation for 386 rows > 349 edges is mathematically impossible under DAG semantics | Table 1 | **Yes** | Audit the database; state the real mechanism (e.g., rows superseded without recorded edge, or corrections applied via retire path) |
| M3 | "Correction" = 386 (status-based, Table 2) vs. 349 (events) used interchangeably; abstract and Findings 3/5 use 349 while Finding 1's rates use 386 | Abstract, §3, Table 2, Findings 3/5 | **Yes** | Harmonize definitions; label each statistic as status-based or event-based; reconcile |
| M4 | Survival risk set n=2,309 (349 events + 1,960 censored) is not reconstructable from any combination of Table 1 numbers | §4.2 | **Yes** | State exact inclusion criteria for the risk set and make it reconstructable |
| M5 | Self-correction downstream arm (0.7%, n=300) has no methods description; 300 exceeds the 284 self-correction events available | §4.6, §4.7 | **Yes** | Describe entity selection, stimulus construction, and grading for the self-correction condition, or remove the 0.7% claim |
| M6 | 57% API-content-filtering attrition in the downstream experiment introduces unknown bias; CI method unstated (Wald reported; exact differs); 50% null arbitrary | §4.7 | **Yes** | Report exact binomial CI; analyze dropped vs. retained entities; justify or replace the 50% null with the self-condition comparison |
| M7 | 1,857× reduction mixes a sampled single-pair numerator with a full-population entity-pair denominator and is computed from rounded values; also mislabeled "false-positive rate" in Contribution 3 | Abstract, Contribution 3, §4.3 | **Yes** | Compute ratio within one population at one level; report unrounded; rename to "reduction factor" |
| M8 | 81.7% clash rate measured on one agent pair (codex–workbuddy) but generalized to all cross-agent pairs | Abstract, Contribution 3, §4.3 | No | Report the full 15×15 pairwise matrix or narrow the claim |
| M9 | Grader (LLM third call) unvalidated — no human-labeled agreement subsample | §4.7 | No | Add a human-labeled subsample (e.g., 50 pairs) with agreement statistics (κ) |
| M10 | Divergence ≠ harm: symmetric answer difference is interpreted as "harm" without any wrongness judgment | Finding 5, §5, Fig. 5 caption | No | Add human/LLM judgment of which answer is correct; rename "divergence" consistently or justify "harm" |
| M11 | Write-time interception recommendation conflicts with the paper's own Finding 2 (99.96% of raw clashes are false positives); interception false-positive cost never measured | §5, Finding 5 | No | Discuss explicitly; condition the recommendation on semantic-level (not entity-string) interception; ideally measure interception precision |
| M12 | "Improving retrieval by 1% is equivalent to storing 2× more memories" is unsupported by any experiment or derivation | §4.5 | No | Derive formally or delete |
| M13 | Findings 2 and 5 depend on a companion paper for full methods; this paper is not self-contained | §4.7 | No | Inline the essential pipeline/protocol descriptions; cite the companion only for extended detail |
| M14 | No sensitivity analysis or uncertainty for Finding 4 (coverage ratio depends on the chosen 3,980-char injection cap) | §4.5 | No | Report coverage as a function of injection cap; contextualize with token budgets |

### Minor concerns

1. Broken duplicated sentence in §4.3 (Finding 2): "At the cross-source pair level (24,907 pairs), after applying the full classification pipeline on the shared entity (e.g., ...). However, after applying the full classification pipeline ..." — editing artifact; rewrite.
2. Finding 3's text says "262 of 269 corrections" were system-mediated, leaving 7 same-day corrections unexplained; the abstract's "262 of 349 (75.1%)" and the table's "77.1%" (269/349) describe different numerators — clarify the 269 vs. 262 vs. 7 relationship.
3. Table 3 caption says "a single consolidation event accounts for 77%" but the abstract and Finding 3 text say 75.1% (262/349) — pick one and make caption/text/abstract agree.
4. Abstract says "a single system-mediated consolidation event accounts for 262 of 349 corrections (75.1%)" while §3 says "87 organic corrections (the remaining 262 were system-mediated)" — 87 + 262 = 349 ✓, but then Table 3 shows 2026-09-27 with 269 corrections, implying 7 organic corrections occurred that day; state this.
5. Contribution 2 says "over 11×"; 91.5/8.2 = 11.16 ✓ — but consider reporting the CI for the ratio (or odds ratio with CI) rather than a point ratio.
6. Finding 5 says "This asymmetry follows a power-law distribution" — a two-point contrast (86% vs. 0.7%) is not evidence of a power law; rephrase (e.g., "disproportionate concentration").
7. Abstract's finding (5) says "86% answer divergence" while §5/Fig. 5 say "86% of downstream harm" — unify terminology (see M10).
8. §Reproducibility lists "Python 3.13" and "the 8813 API pool" — undocumented jargon; define the API pool or remove.
9. The repro section's expected output "81.7% contradictory, 18.4% same polarity" sums to 100.1% — presumably a residual category is omitted; list all categories.
10. Table 1 footnote 1 references "the unified system paper" — not in the bibliography; cite it properly or remove the cross-reference.
11. Bibliography formatting: `letta` cites "MemGPT" paper but the key/text say Letta; `caura` and `cac` are Anonymous/non-verifiable entries (see R3 W6).
12. The paper says "32 days, truncated to 30 for analysis" — state the truncation rule (which days dropped, why).
13. Figure 3 caption says "(269 corrections)" while the text emphasizes 262 — consistent with item 4 but worth a clarifying phrase in the caption.
14. `\label{sec:repro}` appears after text in the Reproducibility section — fragile placement; move before the subsection content.
15. The abstract calls 0.044% a rate of "cross-source entity pairs" while §4.3 computes it from "cross-source pairs" (24,907) — specify whether pairs are entity-pairs or fact-pairs at each stage.
16. No ethics/privacy statement beyond "private operational data" — a brief statement on what categories of personal data the DB contained and why release was impermissible would strengthen the paper.
17. The deployment table lacks client identities/types (even anonymized categories), limiting workload interpretation (see R3 W2).

---

## Consistency Check

### A. Numbers: abstract vs. body vs. tables vs. conclusion

| Quantity | Abstract | Body | Tables | Conclusion/Other | Verdict |
|---|---|---|---|---|---|
| Study length | "30-day" | "2026-09-13 to 2026-10-14 (32 days, truncated to 30)" | Table 1: "30 days" | Conclusion: "30 days" | Consistent, but truncation rule unstated (Minor 12) |
| Operations | 3,000 | §1: "3,000 operations (2,273 writes, 87 organic corrections..., 200 retirements)" | Table 1: 3,000 | Conclusion: "3,000 operations" | **Inconsistent internal sum**: 2,273 + 87 + 200 = 2,560 ≠ 3,000; 440 operations unaccounted (searches? reads?). Footnote 1 hints audit includes reads but no read count is given for the 3,000. Needs breakdown |
| Clients | 15 | §1, §4.1: 15 | Table 1: 15 | Conclusion: 15 | Consistent |
| Active memories | 1,957 | §1, §4.5: 1,957 | Table 1: 1,957 | — | Consistent |
| Entities | 7,375 | §1 | Table 1: 7,375 | — | Consistent |
| Supersession events | — | 349 (§1, §4.3, §4.6) | Table 1: 349 | — | Consistent |
| Superseded memories | — | — | Table 1: 386 (footnote) | — | 386 vs. 349 unexplained/inverse explanation (M2) |
| Procedure correction | 91.5%, "over 11×" | §4.1: 118/129 = 91.47% ✓; 91.5/8.2 = 11.16 ✓ | Table 2: 129/118/91.5% ✓; repro expects 129/118 ✓ | — | Consistent |
| Decision correction | 8.2% | §4.1: 34/413 = 8.23% ✓ | Table 2: 413/34/8.2% ✓ | — | Consistent |
| Other types | — | — | Incident 49/289 = 16.96% ✓ (17.0); Experience 46/426 = 10.80% ✓ (10.8); Fact 139/1,333 = 10.43% ✓ (10.4) | — | Table internally consistent |
| Table 2 sums | — | — | Total = 2,590; corrected = 386 | — | 2,590 ≠ any Table 1 population; 386 ≠ 349 (M3) |
| KM | — | n=2,309 (349 events, 1,960 censored); median 2.5 days procedural | — | — | n unreconstructable (M4); 349+1,960 = 2,309 internally consistent |
| Raw clash rate | 81.7% | §4.3: 81.7%; repro: 81.7% (+18.4% same → 100.1%) | Table 3: 81.7% | — | Consistent except repro percentage sum (Minor 9) |
| Genuine contradiction rate | 0.044% | §4.3: 11/24,907 = 0.04418% ✓ | Table 3: 0.044% | — | Consistent |
| Reduction factor | 1,857× | §4.3: 1,857×; Contribution 3: "1,857× false-positive rate" | Table 3: 1,857× | — | 0.817/0.00044 = 1,857 (rounded inputs); unrounded = 1,850; mislabeled in Contribution 3 (M7) |
| Consolidation | "262 of 349 (75.1%)" | §4.3: "269 corrections on 2026-09-27... (262 of 269)"; §1: 87 organic + 262 system = 349 ✓ | Table 3: 269 = 77.1% of 349 ✓; 19+12+49+269 = 349 ✓ | Fig. 3 caption: 269 | **Three figures in play: 262 (event-attributed), 269 (same-day), 77.1% vs 75.1%** — abstract vs. caption mismatch (Minor 3/4) |
| Organic rate | — | §4.3: "2.7 corrections per day" excluding event | — | — | 87/30 = 2.9/day; (349−262)/30 = 2.9; (349−269)/30 = 2.67 ≈ 2.7 — so "excluding this event" here means excluding the whole day; inconsistent with the 262-based narrative. Clarify |
| Coverage | 0.48%, 209× | §4.5: 833,488 chars; 3,980 cap; 833,488/3,980 = 209.4 ✓; 3,980/833,488 = 0.4775% ≈ 0.48 ✓ | — | Fig. 4 caption: 833K, 3,980, 209× ✓; repro: 833488, 0.48% ✓ | Consistent; mean 426 × 1,957 = 833,682 ≈ 833,488 (rounding of mean; acceptable but note) |
| Cross-agent share | 14.9% | §4.6: 52/349 = 14.90% ✓; 284/349 = 81.37% ✓ (81.4); 52+284 = 336; 349−336 = 13 = 3.72% ✓ (3.7) | Repro: cross=52, self=284 ✓ | — | Consistent |
| Divergence | 86% vs. 0.7% | §4.6/§4.7: 37/43 = 86.05% ✓; CI [76,96]; p<0.001; 0.7% (n=300) | — | Fig. 5 caption: "86% of downstream answer divergence" vs. text "99% of the measurable downstream harm" | **86% vs. 99% tension**: text says cross-agent corrections are "responsible for approximately 99% of the measurable downstream harm" — 86% divergence rate per-entity is not 99% of total harm; the 99% claim is unexplained/unsupported (add derivation or remove) |
| n=100 → 43 gradeable | — | §4.7: 100 entities, 43 gradeable | — | — | 57 dropped = 57% attrition (M6) |
| "73pp finding" | — | §4.7: "confirms the 73pp finding from our companion paper" | — | — | 86% − ~13%? Unclear; 73pp presumably 86−13 or similar from companion; unexplained in this paper — define |
| Conclusion's five findings | — | — | — | Conclusion lists all five qualitatively | Consistent with body at qualitative level |

**Summary of numeric issues:** operation-count breakdown short by 440; 386 vs. 349; n=2,309; 262/269/75.1%/77.1% cluster; 86% vs. 99% harm claim; 1,857× rounding; repro percentage sum 100.1%; 2.7 vs. 2.9 organic rate.

### B. Citations: `\cite{key}` vs. `\bibitem{key}`

`\cite` keys used in body:
1. `wu2024longmemeval` (§1) → `\bibitem{wu2024longmemeval}` ✓
2. `locomo2024` (§1) → `\bibitem{locomo2024}` ✓
3. `memtether` (§1) → `\bibitem{memtether}` ✓
4. `cac` (§4.7) → `\bibitem{cac}` ✓
5. `mem0` (§Related) → `\bibitem{mem0}` ✓
6. `zep` (§Related) → `\bibitem{zep}` ✓
7. `letta` (§Related) → `\bibitem{letta}` ✓
8. `mab` (§Related) → `\bibitem{mab}` ✓
9. `caura` (§Related) → `\bibitem{caura}` ✓

`\bibitem` entries defined: `wu2024longmemeval`, `locomo2024`, `memtether`, `mem0`, `zep`, `letta`, `mab`, `caura`, `cac` — 9 entries, 9 cited keys.

**Result: perfect 1:1 match — no uncited bibitems, no undefined cites.**

Citation-quality caveats (not match failures):
- `cac` and `caura`: "Anonymous (2026)" — non-verifiable; `caura` gives arXiv:2606.24535 (a 2026 arXiv ID whose format should be checked — 2606 would mean June 2026, plausible only if the paper is submitted after that date).
- `memtether`: self-citation to a GitHub repo, "Anonymous."
- Table 1 footnote 1 mentions "the unified system paper" with no citation.
- `letta` key vs. MemGPT title — minor key/title mismatch, acceptable but worth renaming for clarity.

### C. Cross-reference integrity

- `\ref{tab:deployment}`, `tab:type-correction`, `tab:clash-rate`, `tab:clustering` — all defined ✓
- `\ref{fig:type-correction}`, `fig:km`, `fig:entity-resolution`, `fig:daily-corrections`, `fig:coverage`, `fig:asymmetry` — all defined ✓; all six figure PDFs are `\includegraphics`-referenced (figs 1–6 present in `\graphicspath{{figs_dynamics/}}`; existence on disk not verifiable from the .tex alone)
- `\ref{sec:expanded-dyn}` used in §4.6 → `\label{sec:expanded-dyn}` defined ✓
- Section numbering oddity: "Expanded Downstream Validation" is subsection 4.7 but is visually formatted as a peer of Findings; Finding 5 references it forward ✓
- Finding numbering: only `\newtheorem{finding}` is defined but findings are unnumbered prose headers ("Finding 1..." in subsection titles) — fine, but the `finding` theorem environment is unused; remove or use.

---

## Recommendation

**Overall: Major Revision**

**Rationale.** The study targets a real gap — longitudinal dynamics of shared agent memory in production — and the deployment transparency and reproducibility artifacts are commendable. But in its current form the paper's central empirical claim (Finding 1) is confounded by the paper's own Finding 3: 75% of all corrections come from one bulk consolidation event, and no analysis excludes them. Compounding this, several bookkeeping numbers do not reconcile (2,560 ≠ 3,000 operations; 386 vs. 349 corrections; n=2,309 risk set; 262 vs. 269; 86% vs. 99% harm), one experimental arm (self-correction, n=300) is entirely undocumented, the downstream experiment has 57% unexamined attrition, and the headline 1,857× ratio mixes populations and rounding. None of these problems appears fatal to the underlying contribution — the raw data seem capable of supporting (or refuting) the claims once re-analyzed — which is why this is Major Revision rather than Reject.

**Required for acceptance (blocking):**
1. Re-analysis of Findings 1 and KM with consolidation-event corrections excluded (M1).
2. Corrected, database-audited explanation for 386 vs. 349 (M2) and a harmonized correction definition (M3).
3. Reconstructable survival risk set (M4).
4. Full methods for the self-correction downstream arm (M5).
5. Exact CIs, attrition analysis for the 100-entity experiment, and a defensible null (M6).
6. Single-population, unrounded computation of the clash-to-contradiction ratio with correct terminology (M7).
7. Reconciliation of the operation-count breakdown (Consistency A) and the 262/269/75.1/77.1 cluster (Minor 2–4).

**Strongly encouraged (non-blocking):** pairwise clash matrix across all 15 sources (M8), grader validation with human labels (M9), divergence-vs-harm terminology and a wrongness judgment (M10), explicit treatment of the interception-vs-false-positive tension (M11), removal or derivation of the "1% retrieval ≈ 2× storage" claim (M12), and calibration of "production" framing to a single-operator deployment (R3).

---

*Review completed. Confidence: high on internal consistency and statistics; medium on domain generality (single-deployment literature context is thin, so "no published study" claims are assessed against the paper's own related-work section only).*
