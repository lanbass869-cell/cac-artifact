# Peer Review: "About or Contains? Entity-Aware Retrieval for Agent Memory"

Reviewed manuscript: `about-or-contains-paper.tex` (Anonymous, article class, 10 sections, 5 references)
Review date: 2026-10-18

---

## Reviewer Reports

### R1 — Methodology and Technical Soundness

**Summary.** The paper identifies an "about vs. contains" failure mode in agent-memory retrieval (facts that merely contain the query string outrank facts that are about the query entity), attributes it to two root causes (popularity-based ranking via `use_count`, and regex-based entity extraction with 58.1% coverage), and proposes a subject-proximity score with a coverage gate that falls back to the baseline hybrid retriever. Evaluation: precision@10 improves from 28% to 73% on a small hand-labeled benchmark.

**Strengths.**
1. The problem articulation is crisp and genuinely under-discussed in the agent-memory literature; the packy walkthrough (top-1 = file-path match with embedding score 1.00) is a convincing, concrete motivating example.
2. The gating design (entity-first when coverage is sufficient, fallback otherwise) is a sensible precision/recall trade-off and is honest about low recall.
3. The method requires no model, no embedding, and is deployable as post-processing — technically simple and reproducible.

**Weaknesses.**
1. **Ground truth is not independent of the method (circularity).** §2.3 defines ABOUT as "the query string appears as a substring of the fact's primary entity (the first entity extracted by the predicate extractor)". The "predicate extractor" is the same regex extractor whose failures are Root Cause 2. The proposed method ranks facts in which the query entity is the subject/primary entity. Ground truth and method objective are thus nearly the same predicate, so precision@10 for the proposed method is inflated by construction. The paragraph simultaneously claims the labels are "determined by manual inspection" and "does not rely on character position" — three mutually inconsistent criteria in one sentence. Also: under the stated rule, for "temporal accuracy" (0 entity links, Table 2) *no* fact can be labeled ABOUT, so baseline About@10 must be 0 — yet Table 1 reports 1/10. The labeling protocol as written cannot produce Table 1.
2. **The "no regression guarantee" is a false claim, refuted by the paper itself.** §4.2: "This guarantees no regression." The Finding reports a regression: temporal accuracy 1→0. With 0% entity coverage, the gate must fail and the method must return baseline results identically (1/10). Either the gate triggered (contradicting 0% coverage) or the fallback is not the baseline (contradicting §4.2). As stated, the guarantee has a counterexample inside the paper. No theorem or proof is offered; the informal "guarantee" is simply false.
3. **Baseline scoring mechanism is never specified.** The baseline is described as "embedding + FTS5 + RRF fusion", yet Root Cause 1 says ranking uses `use_count`, and §3.1 states "the baseline ranks them by use_count". Where does `use_count` enter RRF? Meanwhile §2.2 attributes the packy top-1 to the *embedding* score (1.00), not popularity. The two causal stories conflict; the reader cannot determine what the baseline actually computes.
4. **Undefined components.** The Q-value ("learned quality", weight 0.2) is never defined — range, learning procedure, or source. The "predicate extractor" is never specified. The piecewise subject-proximity function (Eq. 1) has overlapping conditions (e.g., idx=50 with count≥2 matches both the 0.7 and 0.5 branches) with no stated precedence.
5. **No statistical treatment.** No significance test, no confidence interval, no effect-size discipline beyond +45pp. Wilson 95% CIs on 28/100 and 73/100 would be roughly [20%, 37%] and [64%, 81%] (non-overlapping), but the 100 pairs are not independent (queries duplicated; see R2), so even this would overstate certainty. A McNemar test on paired outcomes is the right instrument, but the paired per-item outcomes are not reported and cannot be reconstructed.

**Ratings.**
| Dimension | Score (1–5) |
|---|---|
| Originality | 3 |
| Scientific importance | 2 |
| Technical soundness | 2 |

---

### R2 — Evaluation Quality

**Strengths.**
1. Precision@10 is used consistently as the metric throughout abstract, tables, and conclusion; the arithmetic of Table 3 (28/100, 73/100, +45pp; remaining 27% errors) is internally correct.
2. The paper is candid that "statistical significance cannot be reliably assessed" at this scale and reports raw counts.
3. The reproducibility section gives runnable commands with expected outputs that match the text (packy 1/10 baseline, 10/10 hybrid; 827 unlinked facts = 41.9% of 1,975).

**Weaknesses.**
1. **Benchmark composition is self-contradictory.** Table 1 caption: 10 runs over **8 distinct queries** (supersession and fuseeval run twice). Abstract, §1, and Table 3 caption: "**10-query** benchmark", "100 query–result pairs across **10 queries**". These cannot both be true.
2. **Table 1 does not sum to the headline number.** Per-run About@10 counts sum to **19/100** (1+0+0+2+2+1+1+2+2+8). Table 3 reports baseline **28/100**. The caption's explanation ("they represent 10 runs over 8 distinct queries") does not explain an 8-count discrepancy — if Table 1 is the benchmark, the total must be 28; if it is not, the paper never presents the actual benchmark runs.
3. **Per-query results for the proposed method are missing.** Only 4 of 10 per-query outcomes appear in prose (packy 1→10, memory_hub 2→10, fuseeval 2→10, Memory Court 1→10) plus one regression (temporal accuracy 1→0). The claims "73/100" and "improvement direction consistent across 7 of 10 queries" are unverifiable. Memory Court does not appear in Table 1 at all, so even its baseline (1) has no table support.
4. **Pseudo-replication.** Duplicate runs of supersession and fuseeval are counted as independent benchmark items, inflating n from 8 to 10. Worse, the two supersession runs disagree (0/10 vs 2/10) while the caption claims they were run "to verify stability" — the data show instability, which is never discussed. (Possible cause: the underlying DB drifts during the 30-day window; run dates and DB snapshots are not given.)
5. **Query selection bias.** The queries (packy, hubguard, supersession, Memory Court, ...) appear to be ad-hoc terms the authors noticed failing, plus CAC (baseline 80%). No sampling procedure, no query taxonomy, no held-out queries. External validity of 28% baseline precision is unknown.
6. **No ablations.** The weights (0.7/0.2/0.1), position thresholds (30/80/200 chars), and gate parameters (≥3 facts, ss ≥ 0.7) are magic numbers with no sensitivity analysis; with 8–10 queries they are likely overfit to the benchmark.
7. **No inter-annotator agreement.** Ground truth is manual labeling with no second annotator, no kappa, no labeling guidelines, and a definition (primary-entity substring) that conflicts with manual inspection (see R1).
8. **Coverage table (Table 2) covers only 4 of the 8–10 queries**; coverage for packy, hubguard, memory_hub, MEMORY.md, supersession, CAC is not reported.
9. **Precision only.** Recall, MRR, or nDCG are never measured; "Correct@10" conflates "labeled ABOUT" with correctness.

**Ratings.**
| Dimension | Score (1–5) |
|---|---|
| Originality | 2 |
| Scientific importance | 2 |
| Technical soundness | 2 |

---

### R3 — Practical Impact and Generality

**Strengths.**
1. The failure mode is real, frequently encountered in production agent memory (string containment in file paths, tags, lists), and the fix is cheap, deterministic, and local-first — aligned with the system's constraints. The discussion of why LLM-based extraction was rejected (cost, non-determinism) is pragmatic and credible.
2. The subject-proximity score is retriever-agnostic and language-agnostic in principle (character position only); the claim that it can be applied as post-processing to any retriever is plausible.
3. The Limitations paragraph is unusually honest (single deployment, subjective labels, extractor coverage gaps).

**Weaknesses.**
1. **Single deployment, n=1 system, effectively single user.** "Production" is the authors' own local memory store serving 15 clients that are never described. Nothing is shown about query distribution, traffic, or multi-tenant behavior. Generalization to other memory systems (mem0, Zep, Letta) is asserted, not demonstrated — none of them is evaluated.
2. **Deployment validity of the numbers is undermined by the inconsistencies in R1/R2** (19 vs 28; Memory Court contradictions; the false no-regression guarantee). A practitioner cannot currently tell which numbers are real.
3. **The "no regression" property — the main deployment argument — is the one property the paper fails to establish** (temporal accuracy 1→0 with no explanation of how a fallback path produced a different result than the baseline).
4. **Novelty overclaim.** "No prior work quantifies or addresses the about-vs-mention distinction" ignores classic entity-centric IR, positional/field-weighting evidence (e.g., BM25F-style proximity features), and entity-ranking work; Related Work is 5 citations, all to agent-memory benchmarks.
5. **Privacy/anonymity.** Table 3 excerpts appear to contain sensitive personal memory content (plaintext-key mentions, account bans); no anonymization or consent statement. The public GitHub URL (`github.com/lanbass869-cell/cac-artifact`) deanonymizes an otherwise "Anonymous" submission and ties the artifact to the CAC project.

**Ratings.**
| Dimension | Score (1–5) |
|---|---|
| Originality | 3 |
| Scientific importance | 3 |
| Technical soundness | 3 |

---

## Concerns

### Major concerns

| # | Concern | Blocking | Suggested fix |
|---|---|---|---|
| M1 | **Ground-truth circularity and incoherent labeling protocol.** ABOUT is defined via the "primary entity" produced by the same regex extractor the paper criticizes; this near-duplicates the proposed method's ranking objective and inflates precision. The paragraph also asserts manual inspection AND non-reliance on character position simultaneously, and the stated rule cannot reproduce Table 1 (temporal accuracy: 0 entity links ⇒ 0 possible ABOUT labels, yet 1/10 reported). | **Yes** | Define ABOUT purely by written human-annotation guidelines on fact content, blind to retrieval output; use ≥2 independent annotators; report Cohen's κ; remove the "primary entity substring" rule or show it agrees with human labels. |
| M2 | **Benchmark composition contradiction and 19≠28.** Table 1 = 10 runs over 8 distinct queries summing to 19/100; abstract/Table 3 claim a 10-query benchmark summing to 28/100. The caption's reconciliation is a non-explanation, and Memory Court (cited in the Finding) is absent from Table 1. | **Yes** | Fix the benchmark to N distinct queries; present one table with baseline and entity-aware side-by-side per query; make all totals reconcile; correct "10-query" vs "8 distinct" everywhere. |
| M3 | **Memory Court results are mutually inconsistent.** Table 2 shows only 2 entity-linked facts (4.7%) ⇒ the gate (≥3 facts with ss ≥ 0.7) must fail ⇒ fallback ⇒ result must equal baseline. Yet the Finding claims Memory Court 1→10, and the Analysis claims enhanced-index Memory Court 5→9 (implying plain entity-aware gave 5, not 10). Three incompatible numbers for the same query. | **Yes** | Recompute and report one consistent set of per-query numbers; explain how a 2-link entity supports 10/10, or correct the Finding. |
| M4 | **"Guarantees no regression" is false as stated.** The paper's own Finding reports temporal accuracy 1→0 while coverage is 0% — under §4.2 the gate must fall back to the identical baseline. Either the algorithm differs from its description or the number is wrong. | **Yes** | Either prove the fallback path is exactly the baseline and fix the temporal-accuracy number, or drop the guarantee and explain the regression mechanism. |
| M5 | **Incoherent headline sentence:** "The enhanced index improves the hybrid from 73% to 73% precision@10". With Memory Court +4 and supersession +2, the likely intended value is 79% — but then it contradicts the Finding (Memory Court 10). A central claim is currently meaningless. | **Yes** | Recompute the enhanced-index total; state clearly which system (baseline / entity-aware / enhanced) each number belongs to; update Table 3. |
| M6 | **Baseline mechanism unspecified; Cause 1 attribution conflicts.** Baseline = "embedding + FTS5 + RRF", yet §3.1 says the baseline ranks by `use_count`, and §2.2 attributes the packy top-1 to embedding score 1.00. Root Cause 1 is not established against a precisely described baseline. | No | Specify the exact baseline scoring function (all RRF inputs and weights); show an ablation isolating the popularity component. |
| M7 | **Aggregates unverifiable: no per-query table for the proposed method.** 73/100 and "7 of 10 queries improved" cannot be checked from the paper. | No | Add a per-query table: baseline / entity-aware / enhanced About@10 for all queries; derive all totals from it. |
| M8 | **Pseudo-replication and no inferential statistics.** Duplicate runs inflate n; supersession reruns differ (0 vs 2) while the caption claims a stability check; no CI, no McNemar, no clustering by query. | No | Deduplicate queries (n=8) or justify reruns; report Wilson CIs and an exact McNemar test on paired items; acknowledge dependence. |
| M9 | **Query selection bias.** Queries appear hand-picked from noticed failures; no sampling protocol; CAC (80% baseline) shows the tail exists but is unexplored. | No | Describe query provenance; add randomly sampled or system-log-derived queries; stratify by query type (entity name / multi-word term / file name). |
| M10 | **No ablation of method hyperparameters.** Weights 0.7/0.2/0.1, thresholds 30/80/200, gate ≥3 and ss ≥ 0.7 are unjustified. | No | Sensitivity analysis over weights and thresholds; report how results change. |
| M11 | **LLM-extraction alternative barely evaluated.** "82% success on unlinked facts" is asserted with no table, no precision of extracted entities, no end-to-end precision@10 of an LLM-extraction variant. | No | Add the LLM-extraction arm to the benchmark, or soften the claim. |

### Minor concerns

| # | Concern |
|---|---|
| m1 | "30-day" period is 2026-09-13 to 2026-10-14, which is 31–32 days. |
| m2 | Abstract says "≥3 facts with the query entity in subject position"; the algorithm gates on ss ≥ 0.7, which includes idx ≤ 80 ("prominent"), not just subject position. Abstract also says "return those first" while the algorithm returns entity results exclusively. |
| m3 | Q-value ("learned quality") is never defined anywhere in the paper despite carrying weight 0.2 in the score. |
| m4 | Eq. (1): condition branches overlap (e.g., idx ≤ 80 also satisfies idx ≤ 200; count ≥ 2 is orthogonal to position) — evaluation order/precedence must be stated. |
| m5 | §2.2 has a redundant repeated clause: "shows the top-3 results ... under the baseline hybrid retriever" appears twice in one sentence; "top-3" is also never actually shown (no listing of the 3 results). |
| m6 | §2.3 says labeling "does not rely on character position", yet the proposed method's key signal IS character position — the paper never explains why position is legitimate for ranking but (allegedly) not for labeling. |
| m7 | The "+45pp" improvement appears in Table 3's row only under Correct@10; the Precision@10 cell of that row is empty — table formatting should be fixed. |
| m8 | Table 1 lists 10 rows but claims "8 distinct query terms"; the column header "About@10" vs text "precision@10" — for k=10 they coincide, but state it once. |
| m9 | "7 of 10 queries improved" (§5) is inconsistent with the per-query narrative: only 4 improvements are named; with a temporal-accuracy regression and 3 no-change fallback queries, the arithmetic of "7 improved" cannot be verified. |
| m10 | The 4 English regex patterns and the resulting "4,136 new entity links" appear only in §5.1 Analysis, not in the Method section; if the enhanced extractor is part of the contribution, it belongs in §4. |
| m11 | "supersession (0→2) are recovered" — grammar ("is recovered"); also inconsistent with Table 1 where supersession baseline is 0 and 2 across its two runs (which run is the reference?). |
| m12 | Reproducibility section: `entity_aware_retrieval.py` is said to be at a GitHub URL, but the repo is anonymous-hostile (username `lanbass869-cell`); no artifact DOI, no pinned commit, no DB schema dump or snapshot hash. |
| m13 | Bibliography: `\bibitem[Packer et~al.(2023)]{letta}` cites MemGPT (2023) but Related Work text attributes "Letta" — Letta is the product rename; the citation is to the MemGPT paper. Minor, but authors should be consistent. |
| m14 | Zep paper first author is Rasmussen (correct), but "Rasmussen, R. et al." omits the actual arXiv author list details; mem0 "Chhikara, P. et al." likewise — use full author lists or consistent et-al style. |
| m15 | Figure/table quality: Table 3's caption says "100 query–result pairs across 10 queries" — the same contradiction as M2. |
| m16 | The paper claims "1,975 active memories" and "2,378 writes" — 403 writes missing/unaccounted (deleted? superseded?); the lifecycle of memories is never explained, though supersession is a key concept. |
| m17 | No ethics/consent statement despite the memory store containing personal data (API keys, account bans, paywall notes). |
| m18 | hyperref loaded but no \url formatting issues; fine. algorithmic environment used without the algorithm float wrapper — cosmetic. |

---

## Consistency Check

### A. Numeric cross-check (abstract vs body vs tables vs conclusion)

| Number | Abstract | Body | Tables | Conclusion | Verdict |
|---|---|---|---|---|---|
| 30-day deployment | "30-day" | "2026-09-13 to 2026-10-14" | — | — | **Inconsistent**: that span is 31–32 days (m1). |
| 1,975 active memories | ✓ | §2.1 ✓; repro section ✓ (827 = 41.9% of 1,975 ✓ arithmetically) | — | — | Consistent. |
| 15 AI clients | ✓ | §2.1 ✓ | — | — | Consistent (but clients never described). |
| Baseline precision@10 = 28% | ✓ | §1 contribution 1 ✓; §5 Table 3: 28/100 ✓ | Table 3: 28/100 ✓ | ✓ | Consistent across mentions — **but** Table 1's own rows sum to 19/100, not 28 (M2). |
| Entity-aware precision@10 = 73% (+45pp) | ✓ | §1 ✓; Table 3: 73/100, +45pp ✓ | Table 3 ✓ | ✓ | Consistent across mentions; unverifiable from per-query data (M7). |
| 58.1% extraction coverage | ✓ | §1 ✓; §3.2: "misses 41.9% (827/1,975)" ✓ | — | — | Consistent (100−41.9=58.1 ✓). |
| "Memory Court" coverage 4.7% | ✓ | Table 2: 2/43 = 4.65% ≈ 4.7% ✓ | Table 2 ✓ | — | Consistent. |
| "temporal accuracy" coverage 0% | ✓ | Table 2: 0/7 ✓ | Table 2 ✓ | — | Consistent. |
| packy: 10 results, 1 about, top = GUI tool | ✓ | §2.2: 1 of 10 ✓; Table 1: packy 1/10 ✓; Table 4 (popularity): 0/5 top-5 about ✓ | ✓ | — | Consistent. |
| ≥3 facts gate | "≥3 facts ... in subject position" | §4.2 algorithm: ≥3 facts with ss ≥ 0.7 | — | — | **Inconsistent** (m2): ss ≥ 0.7 ≠ subject position; also "return those first" vs algorithm returns them exclusively. |
| Regression: temporal accuracy 1→0 | not mentioned | §1 contribution 3 ✓; Finding ✓; §5 Analysis ✓; Conclusion ✓ | — | ✓ | Consistent as reported, but **contradicts the no-regression guarantee** (M4) and Table 1 baseline (1/10) vs 0-coverage fallback logic. |
| packy 1→10, memory_hub 2→10, fuseeval 2→10, Memory Court 1→10 | not mentioned | Finding ✓; §5 Analysis ✓ (duplicated text) | Table 1 gives baselines 1, 2, 2 ✓; **Memory Court baseline absent from Table 1** | — | Partially supported; Memory Court unsupported (M2/M3). |
| "7 of 10 queries" improved | not mentioned | §5 ✓ | — | — | **Unverifiable** (m9). |
| Remaining 27% errors | not mentioned | §5 ✓ (100−73=27 ✓) | — | — | Arithmetically consistent. |
| "improves the hybrid from 73% to 73%" | not mentioned | §5 Analysis | — | — | **Self-contradictory nonsense** (M5); with Memory Court 5→9 and supersession 0→2 the total cannot remain 73. |
| Enhanced index: 4,136 new links | not mentioned | §5 Analysis | — | — | No cross-check possible. |
| 21,300 links / 7,413 entities | not mentioned | §2.1 | — | — | No cross-check possible. |
| LLM extraction 82% success | not mentioned | §6 Discussion | — | — | No supporting table (M11). |
| Q-value weight 0.2; uc capped at 100 | — | §4.1 | — | — | Q never defined (m3). |

**Table 1 internal sum:** 1+0+0+2+2+1+1+2+2+8 = **19**, vs. headline 28/100. **Discrepancy of 8.** Caption's explanation does not account for it.

### B. Citation cross-check (\cite vs \bibitem)

Citations used in text: `\cite{mem0}`, `\cite{zep}`, `\cite{letta}`, `\cite{mab}`, `\cite{conflictbank}` — 5 keys.

Bibitem keys defined: `mem0`, `zep`, `letta`, `mab`, `conflictbank` — 5 keys.

- Every `\cite{key}` has a matching `\bibitem{key}`: **PASS** (5/5).
- Every `\bibitem{key}` is cited in text: **PASS** (5/5, all cited in §7 Related Work).
- No unused bibitems, no undefined citations.

**Bibliographic accuracy notes:** MemGPT arXiv number 2310.08560 ✓; Zep 2501.13956 ✓; ConflictBank 2408.12076 ✓; mem0 2504.19413 ✓; MemoryAgentBench 2507.05257 ✓ (all plausible/correct per reviewer knowledge). Style is minimal ("P. et al.") — acceptable for a preprint, would fail most venue styles.

### C. Cross-reference integrity

- `\ref{tab:baseline}`, `\ref{tab:popularity}`, `\ref{tab:coverage}`, `\ref{tab:results}` — all labels defined. **PASS**.
- The `finding` theorem environment is used once; no numbering issues.
- No unresolved `\ref`/`\label`.

---

## Recommendation

**Overall: Major Revision**

**Justification.** The problem — about-vs-mention in agent-memory retrieval — is real, worth studying, and the proposed direction (subject-proximity scoring over entity indices with coverage gating) is sensible and cheap to deploy. However, the manuscript in its current state contains multiple blocking defects:

1. The ground-truth protocol is circular (defined via the very extractor under test) and cannot reproduce the paper's own Table 1 (M1).
2. The benchmark composition contradicts itself (8 vs 10 queries) and the baseline table sums to 19/100 while the headline claims 28/100 (M2).
3. The Memory Court numbers are mutually exclusive across Table 2, the Finding, and the Analysis (M3).
4. The "no regression guarantee" is refuted by the paper's own reported regression (M4).
5. The enhanced-index result "73% to 73%" is incoherent (M5).

None of these necessarily requires new experiments beyond re-running the existing benchmark with a clean, human-annotation-based protocol and publishing one reconciled per-query table — hence Major Revision rather than Reject. But until the numbers reconcile, no claim in the paper can be trusted, so acceptance is not possible now.

**What a resubmission must contain:**
1. A written annotation protocol (guidelines + ≥2 annotators + κ), independent of any extractor (fixes M1).
2. One per-query table: baseline / entity-aware / enhanced About@10 for all N distinct queries, with all totals derived from it (fixes M2, M3, M5, M7).
3. A precise specification of the baseline scoring function and an ablation isolating the popularity component (fixes M6).
4. Either a proof that the fallback path is bit-identical to the baseline, or removal of the no-regression guarantee (fixes M4).
5. Statistical treatment: Wilson CIs, exact McNemar on paired items, deduplicated queries (fixes M8).
6. Sensitivity analysis of the hyperparameters (fixes M10).
7. Anonymization of memory excerpts and the artifact link, or an explicit consent statement (R3 weakness 5, m17).
