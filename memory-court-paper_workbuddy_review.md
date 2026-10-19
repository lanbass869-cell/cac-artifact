# Peer Review: *Memory Court: Tamper-Evident Evidence Chains and Human Adjudication for AI Agent Memory*

**Manuscript:** `memory-court-paper.tex`
**Review date:** 2026-10-19
**Recommendation summary (across reviewers):** **Major Revision** (2/3 reviewers); **Reject and Resubmit** (1/3 reviewer)
**Overall confidence:** Medium — the engineering appears credible and the open-source artifact exists, but several evaluation, framing, and citation issues must be resolved before the contribution can be assessed as published research rather than a system note.

---

## Number and Citation Check (cross-reviewer)

| # | Item in paper | Verified finding |
|---|---|---|
| 1 | "1{,}864 active memories, 13 agent sources, 26 days" (abstract + §4.1) | Internally consistent with §4.1 list (1,864 / 2,346 / 235 / 348 / 226). The deployment numbers add up. |
| 2 | "14 integration tests covering 6 dimensions" (abstract) | Matches Table 2 (6+2+1+2+1+2 = 14). ✓ |
| 3 | "packy entity: 33% contradiction rate" (§4.4) | "5 of 15 active memories" → 33.3%. ✓ Wilson 95% CI for p̂=5/15 at n=15 is [11.8%, 61.6%], which matches the paper's stated [12%, 62%]. ✓ |
| 4 | "60% contradiction rate" (limitations §5.2) | **INCONSISTENT** with the 33% figure above. Same entity (packy), same denominator (15 active memories), different numerator (9 vs. 5). This is a clear internal contradiction. |
| 5 | "2,346 audit entries" used in tamper-detection experiment | Consistent with §4.1 deployment count. ✓ |
| 6 | "23 (now 14) integration tests" (§5.2) | Implies a reduction from 23 to 14 between drafts. Not explained anywhere in the body. |
| 7 | arXiv IDs cited | **Multiple IDs appear fabricated or futuristic** — see Citation Check below. |
| 8 | "MemGPT" cited as letta | Packer et al. 2023 ("MemGPT: Towards LLMs as Operating Systems") is the correct citation for the Letta/MemGPT lineage, but the `\bibitem` is keyed `letta` while the title says MemGPT. Label drift. |
| 9 | RFC 6962 attribution | Author date in `\bibitem` says "(2019)" but RFC 6962 was published in **2013**. Author-year mismatch. |
| 10 | "Expected: 8 passed" poisoning-defense line | A reproducibility block is shown for `test_poisoning_defense.py` but poisoning defense is **not described in the evaluation section**. This test suite is referenced only in §5.2 ("self-referential evaluation"). |
| 11 | Reference [lineage] title | Title appears truncated: "A Derivation-Gated Framework for Privacy-Preser…" — incomplete word, presumably "Privacy-Preserving". |
| 12 | Playground URL | `https://memtether.github.io/MemTether/court/` — cannot be verified offline; treat as claim, not fact. |
| 13 | Github repository | `https://github.com/MemTether/MemTether` — claim, not verified. |
| 14 | Competitive-gap table (Table 1) | Repo star counts (27.7K / 486 / 290 / 83) are presented without citation or as-of date beyond "(October 2026)". Reproducibility depends on these being snapshot-accurate at submission time. |
| 15 | "60 days" / "30 days" / "26 days" deployment | §4.1 says "26 days at the time of this writing" but parenthetically "(the system has since been extended to a 30-day deployment, reported in the unified system paper)". Two deployment durations in one paragraph. |

**Verdict on numerical integrity:** There are at least **three substantive inconsistencies** (the 33% vs. 60% contradiction rate, the 23→14 test count, and the 26-vs-30 day deployment). Any one of these would prompt revision; together they signal insufficient copy-editing of an otherwise coherent draft.

---

## Citation Check (arXiv realism)

The paper cites eight 2026 arXiv IDs in the 2606.x / 2608.x / 2609.x / 2610.x range (June–October 2026). As of the current date (2026-10-19), three of these fall in the future relative to the paper's nominal knowledge horizon. Even granting that arXiv submissions can be recent:

- `arXiv:2606.24535` (Caura, Margalit et al.) — plausible
- `arXiv:2608.02843` (MutMem, Chen et al.) — plausible
- `arXiv:2609.25521` (Beyond Provenance, Chen et al.) — plausible
- `arXiv:2609.33517` (TRACE, Xiong et al.) — plausible
- `arXiv:2610.07258` (Lineage-Aware Memory Governance, Sangaraju et al.) — submitted October 2026; title truncated in bibliography, suggesting the entry was auto-generated or copy-pasted without verification
- `arXiv:2610.05732` (PACMI, Wang et al.) — submitted October 2026
- `arXiv:2610.05176` (AECG, Tian et al.) — submitted October 2026
- `arXiv:2606.26511` (MemStrata, Yadav) — plausible

**Concern:** the cluster of four 2610.x submissions in October 2026 — all supposedly on the same general topic — raises the question of whether these are real preprints, contemporaneous working papers the author is aware of through insider channels, or placeholder citations. At minimum, the authors should disclose how they discovered four brand-new October 2026 preprints and explain why each is relevant to the specific gap Memory Court fills. The "anonymous companion paper" citation [routec] is acceptable for double-blind review but should be made non-anonymous in the camera-ready.

---

## Reviewer 1 — Dr. A. (Systems / Distributed Systems)

**Overall rating: 3 / 5 — Weak Accept (after major revision)**

**Summary of contribution.** Memory Court layers a SHA-256 hash chain over an append-only audit log, adds a 5-section case-file reconstruction command, and exports a ZIP containing a browser-verifiable HTML page. The engineering is reasonable, the artifact is open-sourced, and the AI-Act angle is timely.

**MAJOR concerns**

1. **No Merkle tree, but no justification for accepting O(n) verification.** The authors note a Merkle tree would give O(log n) proofs and call it a "planned optimization." For a 2,346-entry deployment the linear scan is fine, but the paper claims evidentiary utility for regulated domains — at the scale Article 12 contemplates (lifetime of a high-risk system), O(n) verification is the wrong asymptotic. Either (a) implement a Merkle/Sparse Merkle tree now, or (b) explicitly bound the deployment size at which O(n) verification is acceptable and explain why this bound is sufficient for the claimed compliance story. (R1-M1)

2. **Anchor tail coverage is a real correctness gap, not a recoverable inconvenience.** §5.2 acknowledges that the last <10 entries before a crash are unanchored. The "recovered by the next anchoring pass" claim assumes the next anchor is computed against an honest pre-crash state. If the crash is *adversarial* (an attacker induces a crash to anchor against a tampered state), this is a vulnerability. Recommend: (a) anchor every entry (not every 10), or (b) document the threat model and explicitly state "Memory Court does not survive an attacker who can trigger crashes during the anchor window." (R1-M2)

3. **The hash chain is only valid within one SQLite file.** §5.2 admits single-machine scope. For a system positioned against EU AI Act compliance, this is a significant scope limitation. AI Act Article 12 is concerned with the lifetime of the *system*, not the lifetime of a single database file. Either narrow the claim to "single-machine deployments" or describe the federation/cross-machine trust model. (R1-M3)

4. **No concurrency analysis for anchor computation.** §4.3 acknowledges "concurrent anchor computation" as an engineering gap. The current scheme ("every 10 entries, compute an anchor") is racy under concurrent writes — two writers could both compute an anchor over the same batch boundary, producing two valid-looking but divergent chains. The author should either (a) describe the locking/serialization scheme used to prevent this, or (b) report a controlled experiment showing it cannot happen in practice. (R1-M4)

**MINOR concerns**

5. The audit-entry hash $H(e_i)$ concatenates fields directly with `||`. This is fine for a demo, but if any field contains binary data (e.g., `detail` JSON with non-ASCII) the construction should specify canonical encoding (e.g., length-prefixed, or canonical JSON). (R1-m1)
6. `verify.html` uses `crypto.subtle`. Browsers prior to 2017 lack this. Note minimum browser version. (R1-m2)
7. The "anchor tampering" scenario in the tamper experiment should be enumerated with the other four. Section 4.2 groups "5 scenarios" but only names four (content, timestamp, agent, deletion, anchor). (R1-m3)
8. Table 1 uses repo star counts as a quality signal — this conflates popularity with capability coverage. Cite the actual capability check methodology. (R1-m4)

**Recommendation:** Major revision. Address R1-M1 through R1-M4. After revision the contribution would be a useful systems paper; in current form the gap analysis and compliance framing outrun the actual scope of what's been built.

---

## Reviewer 2 — Dr. B. (Empirical / Evaluation Methodology)

**Overall rating: 2 / 5 — Reject (resubmit encouraged)**

**Summary.** The system description is competent but the evaluation does not support the paper's claims. The headline numbers are small, single-author, and self-reported. The case study, the tamper experiment, and the integration tests together do not constitute an empirical validation of Memory Court as a system.

**MAJOR concerns**

1. **The tamper experiment is not an evaluation of Memory Court — it is a sanity check of SHA-256.** §4.2 is candid about this ("expected property of any correctly implemented hash chain; the contribution is the integration…not the detection mechanism itself"). If the only experimental result is "we did not break SHA-256," then this section should be reframed as a smoke test, not as evaluation. A 5/5 detection rate on 5 anchored-row modifications is uninformative — it would be alarming if SHA-256 *failed* to detect a 1-bit flip. (R2-M1)

2. **The case study is n=1.** §4.4 describes a single entity (packy) with 15 active memories. The 33% → 0% contradiction resolution is a single observation. The Wilson 95% CI of [12%, 62%] on the pre-adjudication rate is honest, but reporting the post-adjudication rate (0%) with no CI is misleading — the upper bound on the post-rate at n=15 is non-zero. Add a Wilson CI on the post-rate (it will be wide, but honest). (R2-M2)

3. **Internal contradiction: 33% vs. 60% contradiction rate.** §4.4 says 33%; §5.2 (limitations) says 60%. These cannot both be correct. Resolve before resubmission. (R2-M3)

4. **"23 (now 14) integration tests" with no explanation.** §5.2 mentions a reduction from 23 to 14 tests but the paper never describes what was removed or why. If 9 tests were dropped, the reader needs to know whether this affected coverage. (R2-M4)

5. **The "self-referential evaluation" caveat is doing too much work.** §5.2 acknowledges that all evaluation is self-designed, self-executed, and unverified. This is appropriate honesty, but it means the paper is presenting a system and a *reproducibility promise*, not empirical results. The evaluation section should be reframed as a test-coverage summary (which is what it actually is), not as "Evaluation." (R2-M5)

6. **Free-tier LLM judge.** §5.2 mentions GLM-5.3-flash. GLM-5.x is plausible as a free-tier API name, but this is the first place in the paper where the LLM judge model is named. If the contradiction rate is partly an artifact of a specific model, the evaluation must either (a) hold the model constant across comparisons, or (b) report results across multiple judges. (R2-M6)

**MINOR concerns**

7. "26 days" deployment (§4.1) vs. "30-day deployment" parenthetical in the same paragraph. Pick one. (R2-m1)
8. Table 2 test counts (6+2+1+2+1+2 = 14) are correct, but the "6 dimensions" framing makes one expect 6 test functions each of which exercises one dimension — actually 6 is the number of dimensions, not the number of tests. The caption should clarify "tests per dimension" vs. "dimensions covered." (R2-m2)
9. The Playground is described as "a demonstration artifact, not an evaluated component" (§3.5). This sentence is good and should appear earlier — possibly in the abstract — to manage reader expectations. (R2-m3)
10. Reproducibility block (§6) lists `pytest tests/test_poisoning_defense.py` with "Expected: 8 passed" — but the poisoning-defense test suite is not described in the body. If it exists, document what it tests. If it does not, remove. (R2-m4)

**Recommendation:** Reject. The system is interesting; the evaluation does not yet support the framing. Resubmit with (a) corrected numbers, (b) reframed evaluation that does not over-claim on a 5/5 SHA-256 sanity test, and (c) a multi-entity or multi-judge extension of the case study.

---

## Reviewer 3 — Dr. C. (Legal / Compliance / HCI)

**Overall rating: 3 / 5 — Weak Accept (after major revision)**

**Summary.** The AI-Act framing is the most novel part of this paper. The author correctly identifies that EU AI Act Article 12 requires automatically generated event logs "over the lifetime of the system" with traceability. Memory Court's `evidence.zip` is a thoughtful implementation of this requirement at the memory layer. However, several regulatory claims need scrutiny, and the human-adjudication side is under-developed.

**MAJOR concerns**

1. **The AI Act claim is overstated.** §2.2 states "Memory Court's evidence export directly implements this requirement at the memory layer." This is true in a narrow sense, but Article 12 concerns the AI *system*, not just one component. A high-risk AI system may have multiple subsystems — model serving, retrieval, memory, UI — and the record-keeping requirement applies to the functioning of the *system*. Memory Court records memory operations; it does not record model inference, retrieval calls, or user interactions. Either narrow the claim to "memory-layer compliance contribution" or describe how Memory Court integrates with broader system-level logging. (R3-M1)

2. **GPAI compliance date is wrong.** §2.2 says "compliance is required by 2027-08-02." The EU AI Act GPAI obligations (Articles 53–55) apply from **2 August 2025**, not 2027. (Article 113(a) sets the application date for most provisions at 2 August 2026, with GPAI rules applying 12 months earlier per Article 113(b).) This is a factual error that undermines the regulatory credibility of the paper. (R3-M2)

3. **"Human adjudication" is not evaluated.** §3.3 lists case-file reconstruction and §4.4 mentions a supersession workflow, but there is no user study, no workflow analysis, and no description of who performs the adjudication. In a deployment where all 13 agent sources are operated by the author (§5.2), the "human adjudication" claim is empty. Either (a) remove the "human adjudication" framing, or (b) describe what the adjudication workflow looks like, who performs it, and what UI/UX support is provided. The Playground suggests a UI exists; this needs to be evaluated or its existence needs to be downgraded to a claim. (R3-M3)

4. **Tamper-evidence ≠ tamper-prevention.** The paper is careful in §5.1 ("does not prevent memory poisoning attacks… makes such writes detectable and attributable"), but the abstract's "tamper-evident by construction" risks reader over-claim. Recommend tightening the abstract to read "tamper-evident post-hoc" or "tamper-detectable" to match the actual mechanism. (R3-M4)

5. **Conflict between AI-Act framing and limitations.** §5.2 admits the deployment has no external users and is single-author. This is incompatible with the regulated-domain framing of the introduction ("healthcare, finance, legal"). Either the contribution is *toward* compliance infrastructure (in which case the limitations are acceptable as a system note) or it is *evidence of compliance* (in which case the limitations are fatal). The paper oscillates between these two framings. Pick one. (R3-M5)

**MINOR concerns**

6. The MemGPT/Letta citation confusion (`letta` label, MemGPT title) is a minor issue, but the Letta project is now commercially rebranded and the relationship to the original MemGPT paper is non-trivial. Cite Letta (the system) and MemGPT (the paper) as separate entries if both are relevant. (R3-m1)
7. RFC 6962 author-year: listed as "Laurie et~al.(2019)" but RFC 6962 was published in **June 2013**. The 2019 date may refer to an erratum or a later revision — clarify. (R3-m2)
8. The truncated bibliography entry for [lineage] ("Privacy-Preser…") should be fixed in the source. (R3-m3)
9. Certificate Transparency is a good precedent but is not directly analogous: CT logs are *publicly* auditable (Merkle tree + gossip), while Memory Court's chain is *privately* verifiable. Note this distinction in §6.1. (R3-m4)
10. §6.3 mentions a "companion system paper" [routec] which is anonymized. This is acceptable for review but should be de-anonymized before camera-ready. (R3-m5)

**Recommendation:** Major revision. The regulatory framing is the paper's strongest angle but is currently the weakest executed. Fix R3-M1 through R3-M5, correct the GPAI date, and either evaluate or downgrade the "human adjudication" claim.

---

## Synthesis and Editor-Level Recommendation

**Strengths (all reviewers agree):**
- The system exists, is open-sourced, and addresses a real gap.
- The hash-chain construction is clearly described and reproducible.
- The browser-verifiable evidence export (`verify.html`) is a clean engineering contribution.
- The limitations section is unusually candid.

**Weaknesses (all reviewers agree):**
- **Internal numerical inconsistencies** (33% vs. 60%; 26 vs. 30 days; 23 vs. 14 tests). These alone justify revision.
- **Evaluation does not match framing.** The paper claims regulatory and evidentiary utility but reports a single-entity, single-author, self-evaluated deployment. The reviewers disagree on whether this is "weak accept with revision" or "reject and resubmit."
- **AI Act GPAI date error** (Reviewer 3, R3-M2). This is a factual error in a regulatory-framed paper.
- **Citation hygiene:** truncated title, mismatched dates, label drift on Letta/MemGPT, cluster of October-2026 arXiv IDs.

**Decision: Major Revision (consensus).**

Reviewer 2's "reject and resubmit" reflects a strict reading: the evaluation is too thin to support the framing. Reviewers 1 and 3 read the contribution as a credible system paper that over-claims on evaluation and compliance scope. The editor's call is **Major Revision** — fix the numbers, narrow the claims, either implement or remove the Merkle/federation gaps, correct the GPAI date, and either substantiate or retract the "human adjudication" framing.

**Required for acceptance (any reviewer would block on these):**
1. Resolve 33% vs. 60% contradiction rate (R2-M3).
2. Explain 23 → 14 test count (R2-M4).
3. Reconcile 26 vs. 30 days deployment (R2-m1).
4. Correct GPAI compliance date (R3-M2).
5. Fix truncated bibliography entry for [lineage] (R3-m3).
6. Fix MemGPT/Letta citation labeling (R3-m1).
7. Fix RFC 6962 year (R3-m2).

**Strongly recommended:**
8. Reframe §4.2 as a smoke test, not an evaluation result (R2-M1).
9. Add Wilson CI on post-adjudication contradiction rate (R2-M2).
10. Document or remove poisoning-defense test reference (R2-m4).
11. Narrow the AI Act claim to "memory-layer contribution to Art. 12" (R3-M1).
12. Specify the locking scheme for anchor computation or report a controlled concurrency experiment (R1-M4).

**If the authors address items 1–7, the paper would be publishable as a system note. To be publishable as a research contribution, items 8–12 are also required.**

---

*Review prepared by three independent reviewers; consensus aggregated. Comments reflect reviewer opinions only, not an institutional position.*
