# Peer Review: "The Write Governance Problem: Quantifying Waste in Agent Memory Systems"

**Manuscript**: `write-governance-paper.tex` (11 pages, ~6,000 words, 7 tables)
**Review date**: 2026-10-19
**Recommendation summary**: Major revisions required (2 reviewers), Reject & resubmit (1 reviewer)

---

## Reviewer A — Reviewer 1

**Overall rating: 3/5 (Weak accept conditional on revisions)**
**Recommendation: Major revisions**

### Summary of contribution
The authors analyze a real, 30-day, single-operator deployment of MemTether (a local-first agent memory system serving 15 AI clients) and quantify three previously unmeasured properties of production agent memory: write waste (9.5% of active memories never retrieved), an injection coverage ratio of 0.48% (3,980 chars of LLM context vs. 825K chars stored), and a steep power-law retrieval distribution. They argue that the binding constraint on memory utility is *write governance*, not retrieval accuracy, and propose a three-gate admission control framework (novelty, type-prior, length), evaluated retrospectively.

### Strengths
1. The dataset is real, not synthetic. Write/retrieval traces from 1,981 active memories across 2,378 total writes are an honest empirical contribution.
2. The injection-coverage framing is novel and clarifying. The buffer-pool analogy (Section 7, Table 6) is genuinely useful — this is a contribution to mental models, not just metrics.
3. The honesty about the type-prior gate's net $-268$ effect is rare and valuable. The paper does not oversell its proposed intervention.
4. Reproducibility appendix with concrete SQL is appreciated.

### MAJOR concerns

**A1. Single operator limits external validity.** This is the paper's central limitation, but it is acknowledged only in one sentence in §8. The 9.5% dead rate and 0.48% coverage are properties of *one person's usage patterns* of *one tool*. Without multi-operator data, the central claims ("write waste is 9.5%", "injection coverage is 0.48%") are anecdotal. At minimum, the paper should reframe these as point estimates from a single deployment, not population estimates. Add a clear "generality" caveat in the abstract.

**A2. Internal inconsistency in write-share numbers.** Section 5.1 ("Waste by Source") reports WorkBuddy writes "28% of total memories" and Codex "54% of writes", but Table 4 reports WorkBuddy share 28.2% and Codex 53.2%. These two figures (54% vs 53.2%) are inconsistent across the same section. Either align the prose with the table or explain the discrepancy (e.g., 54% may refer to *total* writes including retired, while the table counts *active*).

**A3. The "intent-requiring gate" central claim is unsupported.** The paper claims that an intent-requiring gate "would in principle avoid this loss" and then immediately states "we have not yet simulated this variant, so its true effect is unknown." It then provides a back-of-envelope simulation assuming 80% pass rate and claims a "+200 net effect." This is not evidence — it is a guess. Either run the simulation or remove the "+200" claim entirely. The current presentation lets the reader infer the proposal has empirical support when it does not.

**A4. Causal claim about temporal decay (Section 5.2) is unsupported.** The paper says: "This trend suggests that the writing agent learned to write more retrievable memories over time." With n=1 user over 30 days, this is unfalsifiable storytelling. The same data is consistent with early memories being setup logs. Reframe as a hypothesis.

**A5. The 0.48% figure depends on an arbitrary 3,980-character injection limit.** The paper acknowledges this in passing, but the central claim — "injection coverage is 0.48%" — is really "injection coverage is X% for this particular tool." Context windows already vary from 8K to 1M tokens across deployments; a 200× overscan factor is not a universal property of agent memory. Either expand the analysis across multiple injection limits, or downscale the framing.

### MINOR concerns

- **m1.** Equation in §3.1: "the 416 mean in Table 2 is the average across all 1,981 active memories, while 535 is the average of the 189 dead subset only" — this parenthetical is awkward and reads like a late correction. Move it to a footnote.
- **m2.** Section 7 table title is "Analogy between database buffer pools and agent memory injection" but the rows include "Access locality: Unknown (new domain)" — this is a hand-wave, not a comparison.
- **m3.** The B1 gate (Section 8) is presented as a "complementary approach" but is not integrated into the three-gate framework or the central thesis. Either weave it into the framework or move it to an appendix.
- **m4.** Use "ever" instead of "never" in the framing question. "What fraction of written memories is *ever* retrieved?" reads awkwardly. Consider "is *retrieved at least once*."

### Recommendation: Major revisions
The empirical contribution is real and worth publishing, but the central thesis needs tighter scoping to one user/data, the central proposal's effect needs empirical (not back-of-envelope) support, and several inconsistencies (A2, m1) need correction. A revised version with these addressed would be a strong accept.

---

## Reviewer B — Reviewer 2

**Overall rating: 2/5 (Reject, encourage resubmission)**
**Recommendation: Reject & resubmit**

### Summary
The paper makes three contributions: (1) measurement of write waste in a production memory system, (2) measurement of injection coverage, and (3) a proposed admission control framework. The measurements are useful; the proposal is not yet ready.

### Strengths
1. Empirical data on real production memory traces — this is uncommon and valuable.
2. The injection-coverage framing is a useful contribution in its own right.
3. Retrospective evaluation of gates, including honest reporting of negative results.
4. Reproducibility is a strong point: SQL queries are provided in the appendix.

### MAJOR concerns

**B1. The proposed solution does not work, and the paper admits it.** The type-prior gate has a net $-268$ effect. The intent-requiring gate "we have not yet simulated." The length gate has a precision of 6.7%. The novelty gate catches 4 dead writes at unknown cost. The combined gate is $-261$. *Every* variant of the proposed framework either loses utility or is unvalidated. The paper is, in effect, a problem statement without a solution.

This is not a fatal flaw if reframed as "we measured the problem and a naive solution doesn't work; here is what we think could work but isn't yet validated." But the paper's framing in §6 and §10 still reads as if admission control is a viable solution, when the retrospective evidence shows it isn't (with current signals).

**B2. The entity-aware retrieval benchmark (Table 3) is a 10-query benchmark with hand-labeled ground truth.** 100 query-result pairs is small. The dramatic improvement (28% → 73%) may not generalize. Worse, the authors' own breakdown (§5.5) shows that 27% of queries still miss — three of those misses are due to a *bug* in the entity extractor (regex missed all 7 "temporal accuracy" facts). The benchmark may be measuring extractor bugs, not retrieval quality.

**B3. Q-value learning section (Section 6) is a tangent.** 74% retain default Q-value, 26% deviate, mostly negatively. The conclusion "write governance at admission time may be more effective than post-hoc learning" is reasonable but not supported by the data presented. The Q-value analysis is one paragraph and does not belong as a top-level section in an 11-page paper.

**B4. B1 gate evaluation (Section 8) is a separate paper pasted in.** It evaluates a Chinese-only regex parser on a synthetic benchmark with 50 conflicts and 80 near-misses. The 100% recall/precision on synthetic data does not generalize — the production DB has zero conflicts after 30 days. The section confuses "perfect on synthetic" with "feasible in practice."

**B5. Statistical claims lack rigor.** "p < 0.01, Mann-Whitney U" is asserted but the test statistic, U value, and sample size are not reported. The effect size d=0.21 is given for one comparison but not for others. A serious statistical report would include test statistics, confidence intervals, and Bonferroni correction across the 6 type comparisons in Table 1.

### MINOR concerns

- **m1.** The "Why does this matter?" paragraph in §8 is rhetorical filler. Cut.
- **m2.** "Memory Court" (Table 3) and "CAC" appear without definition. CAC presumably means "Context-Aware Compression"? Spell out on first use.
- **m3.** Related work is thin (5 citations). No discussion of A-Mem, MemoryBank, or other 2024–2025 memory architectures.
- **m4.** Equation in §7: ARC citation says "Megiddo and Modha (2003)" — verify. ARC was published at FAST 2003 by IBM Almaden; the author list and venue are correct in the bibliography. Good.
- **m5.** LongMemEval and LoCoMo are cited in the bibliography but never discussed in the body. Why are they listed?

### Recommendation: Reject & resubmit
The empirical measurements (Sections 3–5, Tables 1–5) deserve publication. The proposed solution (Sections 6, 8) does not work as written and should be either replaced with a validated intervention or reframed as a problem statement with a research agenda. The paper's claim that "write governance is the right design point" is currently a hypothesis, not a conclusion.

---

## Cross-Reviewer Synthesis

### Areas of agreement
1. **The empirical measurements are real and valuable.** All three reviewers agree the production data (write waste, injection coverage, power-law usage) is a genuine contribution.
2. **The proposed solution does not yet work.** The type-prior gate's net $-268$ effect is admitted by the authors but inadequately addressed. The intent-requiring variant is unvalidated.
3. **External validity is severely limited.** n=1 operator over 30 days is acknowledged in one sentence but should be foregrounded.
4. **Statistical rigor is insufficient.** p-values are asserted without test statistics; multiple comparisons are not corrected.

### Areas of disagreement
- Reviewer A rates 3/5 (weak accept conditional); Reviewer B rates 2/5 (reject). Reviewer C (below) rates 4/5.
- The disagreement turns on whether the problem statement alone is publishable. Reviewer A and C say yes; Reviewer B says no.

### Consolidated recommendations to authors
1. Reframe the central claims as point estimates from a single deployment, not population estimates.
2. Either simulate the intent-requiring gate or remove the "+200 net" claim.
3. Fix the internal inconsistency in write-share numbers (54% vs 53.2%).
4. Add test statistics and effect sizes for all statistical claims.
5. Reconsider the Q-value section (§6) — either expand or move to appendix.
6. Move or trim the B1 gate section (§8) — it is not integrated into the thesis.
7. Spell out all acronyms on first use.
8. Add related-work citations for A-Mem, MemoryBank, and other recent memory architectures.
9. Drop or expand the B1 gate section: a synthetic benchmark is not evidence.
10. In the abstract, qualify claims: "from one 30-day deployment" instead of "in agent memory systems."

---

## Number & Citation Check

### Internal arithmetic consistency
| Claim | Location | Verified? | Issue |
|-------|----------|-----------|-------|
| 189/1,981 = 9.5% | §3, Table 1 | ✓ | — |
| 55/378 = 14.6% | §3, Table 1 | ✓ | — |
| 3980/825032 = 0.48% | §4, Table 2 | ✓ | — |
| 825032/416 = 1981.4 ≈ 1981 | §4, Table 2 | ✓ | — |
| 0.5% of memories hold 15% of retrievals | §3.3, Table 1 | ✓ | — |
| 100/189 = 52.9% | §5.1, Table 4 | ✓ | — |
| 53.2% vs 54% (Codex write share) | §5.1 prose vs Table 4 | ✗ | **Inconsistency** |
| WorkBuddy 17.9% dead vs Codex 4.1% | §5.1, Table 4 | ✓ | — |
| 17.9/4.1 = 4.36 ≈ "4.4×" | §5.1 | ✓ | — |
| 1.5× system average for experience | §6 Finding 5 | ✓ | (14.6/9.5 = 1.54) |
| 21/312 = 6.7% (length gate precision) | §5.4 Finding 6 | ✓ | — |
| 80/100 + 45pp improvement | §5 | ✓ | — |
| 74% retain default Q-value | §6 | ✓ (given 1,981 active) | — |
| 316/1981/30 = 0.159/day/memory | §6 | ✓ | (close to 0.16) |
| 153/1651 = 9.3% | §3.2 | ✓ | — |

### Citation check
| Citation | Verifiable? | Note |
|----------|------------|------|
| Chhikara et al. 2025, arXiv:2504.19413 (mem0) | ✓ Verified — mem0 paper exists |
| Rasmussen et al. 2025, arXiv:2501.13956 (Zep) | ✓ Verified |
| Packer et al. 2023, arXiv:2310.08560 (MemGPT/Letta) | ⚠ Title mismatch — paper title is "MemGPT," not Letta. The body text and bibliography disagree: text says "Letta" but citation is for MemGPT. Letta is a different system. |
| Hu et al. 2025, arXiv:2507.05257 (MemoryAgentBench) | ✓ Verified |
| Berg et al. 2017 (TinyLFU) | ✓ Verified — ACM TOS 2017 |
| O'Neil et al. 1996 (LSM-tree) | ⚠ Originally published in Acta Informatica 1996, but the canonical "LSM-tree" paper is the 1996 paper. ✓ Acceptable |
| Megiddo and Modha 2003 (ARC) | ✓ Verified — FAST 2003 |
| Wu et al. 2024, arXiv:2410.10813 (LongMemEval) | ✓ Verified |
| Maharana et al. 2024, arXiv:2402.17753 (LoCoMo) | ✓ Verified — "Evaluating Very Long-Term Conversational Memory" |
| Anonymous 2026 (companion paper) | N/A | Self-citation, not verifiable |

### Other numerical issues
- **Reviewer A's concern (A2) confirmed**: §5.1 prose says Codex accounts for "54% of writes" but Table 4 says 53.2%. One of these is wrong.
- **B1 gate latency** (p50 = 0.037 ms): this is below the timer resolution on most systems for a single call. The benchmark methodology should be specified.

---

## Reviewer C — Reviewer 3

**Overall rating: 4/5 (Accept conditional on minor revisions)**
**Recommendation: Minor revisions**

### Summary
This is an empirical paper that measures three properties of a production agent memory system and argues — with evidence — that retrieval accuracy is the wrong optimization target. The argument is clear, the data is real, and the central insight (the binding constraint is write governance, not retrieval quality) is correct and timely.

### Strengths
1. **The injection coverage insight (Section 4) is the paper's most valuable contribution.** The 0.48% figure and the buffer-pool analogy (Section 7) together constitute a new way of thinking about agent memory systems. This alone justifies publication.
2. **Honest reporting of negative results.** The type-prior gate's net $-268$ effect is a stronger contribution than a positive result would be, because it shows the limits of base-rate arguments.
3. **Clean experimental setup.** The SQL queries in the appendix mean anyone with the database can verify every number in the paper.
4. **The power-law finding (Section 3.3)** is consistent with prior work on long-tail distributions in recommender systems and caches; the paper correctly identifies this as evidence that agent memory has cache-like structure.

### MAJOR concerns

**C1. The admission control framework needs stronger empirical backing.** The retrospective simulation in §5.4 (Table 5) is the paper's only quantitative evaluation of the proposed solution, and it shows *every* variant either has negative net effect or is unvalidated. Either (a) drop the framework proposal and reframe as a problem statement, or (b) add an A/B test or live evaluation.

**C2. The 30-day window may be too short for power-law analysis.** With only ~316 retrieval write-backs, the top-5% analysis is based on sparse counts. A 6-month or 1-year window would yield a more robust power-law fit. Acknowledge this limitation more strongly.

### MINOR concerns

- **m1.** §3.2 ("Recency Correction") is a single sentence. Either expand or fold into the broader recency analysis in §5.2.
- **m2.** §8 ("Reproducibility") has a duplicated sentence: "All measurements are reproducible from the production SQLite database" appears twice (lines 313–314). Remove one.
- **m3.** The "Related Work" section (line 333) is short (one paragraph). It also appears to be missing a section header break before it (the .tex source has \section{Related Work} at line 333 with content starting on the same line). Verify LaTeX compiles.
- **m4.** "Mann-Whitney U test, p < 0.01" without test statistic. Add: "U = X, n1 = X, n2 = X, p = X."
- **m5.** The "About or Contains" companion citation is anonymous. If both papers are under review together, ensure the review process is coordinated.
- **m6.** "Memory Court" in Table 3 should be described briefly. Is this a project name? A benchmark query?
- **m7.** The reproducibility SQL queries (Section 8) reference columns `status`, `type`, `use_count`, `content` from table `facts`. The schema should be documented or referenced (a separate schema.sql file or appendix).

### Recommendation: Minor revisions
The paper makes a genuine empirical contribution. The injection-coverage framing and the buffer-pool analogy are independently valuable. The proposed solution is not yet ready, but the problem statement is publishable as-is. With the minor revisions above and either (a) reframing the solution as a research agenda or (b) adding an A/B test, this is a strong accept.

---

## Editor's Decision

**Decision: Major revisions required**

**Rationale**: All three reviewers agree the measurements are valuable. Reviewer A and C are willing to accept with revisions; Reviewer B requires resubmission. The path forward is:

1. Authors must address all MAJOR concerns from Reviewer A and B, plus the MINOR concerns from all reviewers.
2. The proposed admission control framework either needs live evaluation or must be reframed as a research agenda.
3. Internal numerical inconsistencies must be fixed.
5. Statistical rigor must be improved (test statistics, effect sizes, multiple-comparison corrections).

**Estimated time to revision**: 3–6 months for major, 1–2 months for minor.

---

*Review compiled from 3 reviewer reports. All numerical checks performed manually against the .tex source.*