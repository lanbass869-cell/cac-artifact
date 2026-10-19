# Peer Review — MemTether (JSS submission, front sections)

**Manuscript:** MemTether: A Local-First Agent Memory System with Bi-Temporal Supersession and Hash-Chained Audit for Multi-Client AI Agents
**Venue:** Journal of Systems and Software (JSS, single-blind)
**Review scope:** Lines 1–279 of `JSS-MemTether-20261018.tex` — Abstract, Highlights, §1 Introduction, §2 Background & Related Work, §3 System Design, §4 Formal Properties, §5 Tamper-Detection Evaluation, §6.1 Cross-Agent Contradiction Analysis (through the start of §6.2).
**Note on scope:** Sections after line 279 (expanded Findings, benchmark details, §repro, cross-system comparison) were not reviewed in this pass. Items marked **[forward-ref]** depend on material expected later; if that material is absent, the concern escalates.

---

## Summary

The paper presents MemTether, a local-first agent memory system built on a single shared SQLite database that multiple AI client adapters access via NTFS junctions / symlinks. Contributions: (1) a bi-temporal supersession model with four formal correctness claims; (2) a hash-chained tamper-evident audit log ("Memory Court") with self-contained browser-verifiable evidence export; (3) an empirical study quantifying downstream accuracy loss from cross-agent contradictions (73pp, n=11) vs. self-corrections (0.7pp, n=300); (4) a supervised Memory Supersession Prediction task (DistilBERT, macro F1=0.947); (5) evaluations on LongMemEval, LoCoMo, ConflictBank plus a 30-day production deployment (15 agents, 2,346 audit entries, 31K+ operations).

The engineering is real, the deployment data is genuine, and the reporting of negative results (Q-value mechanism mostly inert, Chinese-only extractor failing on English, unanchored-tail detection gap, dual LongMemEval configurations) is unusually candid. The main weaknesses are: headline causal claims built on n=11 without inferential statistics, a cross-agent vs. self-correction protocol that is not apples-to-apples, formal "theorems" that are largely restated design invariants, core mechanisms (SGM, B1 gate) evaluated only on author-built synthetic Chinese benchmarks, and several number inconsistencies (one arithmetic impossibility in the abstract).

---

## Reviewer 1 — Methodology & Formal Claims

**Overall rating: 3 / 5** (sound engineering, oversold formalism, under-powered headline causal claim)

### Strengths
- Honest threat model (§3.4, L133–137): explicitly disclaims protection against a full-write adversary, discloses fail-open source attribution, and ships an executable negative test (test_F) for the poisoning limitation. This candor is exemplary.
- Theorem 1's proof sketch admits it "formalizes this design invariant rather than proving a non-trivial property" (L198) — honest, though this honesty then indicts the abstract's framing (see MAJOR-3).
- §4.3 correctly identifies the real limits: OS-level file lock correctness, direct-SQL bypass, detection-not-prevention.

### MAJOR concerns

| # | Concern | Blocking? |
|---|---------|-----------|
| R1-M1 | **The 73pp headline rests on n=11 with no inferential statistics.** §6.1: 9/11 (82%) vs 1/11 (9%). The Wilson 95% CI on 9% with n=11 is roughly [1.6%, 41%]; the paper reports bare percentages as if they were stable population parameters. No Fisher exact test, no CI, no power statement anywhere in the reviewed scope. The abstract states "cross-agent contradictions cause a 73-percentage-point downstream accuracy loss" as a general property. Required: report CIs and an exact test; state the expanded-set (n=43) result as the primary evidence if it holds; otherwise soften the claim. | **Yes** |
| R1-M2 | **Cross-agent vs. self-correction comparison is not matched.** The 11 cross-agent events are pre-selected as "rule-classified temporal flips" (L253) — i.e., value flips by construction, where stale context necessarily yields a wrong answer to a status probe. The 300 self-corrections are an unfiltered sample, most of which plausibly do not change the answer to the probe at all ("update details within the same conceptual framework," L275 — the authors say this themselves). The 73pp-vs-0.7pp asymmetry is therefore partly baked in by the sampling frame, not purely discovered. Required: stratify self-corrections into answer-changing vs. answer-invariant subsets, or match on flip severity, before the asymmetry can be attributed to the cross-agent mechanism. | **Yes** |
| R1-M3 | **"Four formal correctness theorems" (abstract L31, Highlights L36, contribution 1 L62) oversells §4.** Thm 1 is a restatement of Definition 2(4) by construction (admitted at L198); Thm 2 is two lines; Thm 3 is conditional on cycle detection being implemented in `correct()`; Thm 4 is conditional on SQLite atomicity plus an OS file lock whose correctness §4.3 concedes is outside the paper's guarantees. Reframe as "four correctness invariants with proofs-by-construction" or similar, in abstract, highlights, and contribution list. | No |
| R1-M4 | **EU AI Act Article 12 overclaim.** Abstract (L31): evidence export "addressing EU AI Act Article 12 requirements." Art. 12 imposes logging obligations on providers/deployers of *high-risk* AI systems; a local hash-chained SQLite log plus a ZIP verifier does not by itself "address" conformance. Soften to "supports record-keeping obligations such as …" throughout. | No |
| R1-M5 | **[forward-ref] Contribution 3 (L64): "1,857× entity-resolution gap between raw polarity clash and genuine contradiction" is never defined or derived anywhere in the reviewed scope.** If the derivation is not in the later sections, this number must be removed. | No (escalates to Yes if absent later) |

### MINOR concerns
- Definition 1 (L170): timestamps typed as `vf ⊆ T`, `vt ⊆ T ∪ {∞}` — subset notation for scalar timestamps is wrong; should be `∈`. Same for `ra`, `ia`.
- Definition 2 does not accommodate `retired` status (Def 1 allows three statuses; chains terminate only in `active`). State how retirement interacts with chains or restrict the model.
- Thm 4 statement (L221): "concurrent correct() calls on the same the old fact" — grammar typo; also label style inconsistent (`thm:gapfree` vs `theorem:concurrency`).
- §3.1 verbatim schema (L114): `old\_uid` inside a `verbatim` environment — the backslash will render literally. Remove the escape.
- Author note (L23): "Anonymous" must be replaced per JSS single-blind policy before submission (editorial, not review substance).
- The paper says the 11 events are detected by rules; no precision/recall of the rule classifier itself is given in scope — the 11 are "classified," but we never see what the rules rejected.

---

## Reviewer 2 — Evaluation Quality

**Overall rating: 3 / 5** (candid multi-benchmark reporting, but headline mechanisms validated only on self-built synthetic Chinese data; benchmark protocol under-specified)

### Strengths
- Dual-configuration LongMemEval disclosure (L45: 62.4% full-EAF vs. 58.3% standalone) is exactly the kind of honesty the field needs (cf. the audit-LME citation at L84).
- Related work correctly labels competitors' numbers as "claimed results … not independently reproduced" (L78) rather than implying comparability.
- Negative results reported in-line: Q-value inert for 74% of memories (L151), predicate extractor yields zero pairs on English (L145), tail-entry detection gap (L243).

### MAJOR concerns

| # | Concern | Blocking? |
|---|---------|-----------|
| R2-M1 | **Both headline mechanisms are evaluated only on author-constructed synthetic Chinese benchmarks.** SGM (§3.6): 20 entities × 25 sessions, built by the authors; B1 gate (§3.7): 10 entities, 50 conflicts, 80 near-misses, built by the authors. And L145 concedes the extractor produces *zero* pairs on English benchmark data — the SQL path does not activate at all outside Chinese. The abstract and contribution list do not disclose this scope restriction. Required: disclose Chinese-only scope prominently, and add at least one non-synthetic or non-Chinese validation (or an explicit statement that the mechanisms are Chinese-only by design). | **Yes** |
| R2-M2 | **Benchmark protocol under-specified for reproducibility of headline numbers.** In the reviewed scope: no judge model identified for LongMemEval's "LLM-as-judge" (500Q rerun, L45); LoCoMo 0.523 token-F1 with no comparator; ConflictBank F1=0.897 with no baseline and unclear subset definition; no retrieval-k, prompt, or pipeline version pinned. The abstract's four benchmark numbers are currently unreproducible from the front matter alone. **[forward-ref]** If §repro and later sections supply these, downgrade to Minor. | **Yes** (until verified) |
| R2-M3 | **Single LLM judge (GLM-5.3-flash) for the contradiction probe, with no human-agreement validation.** The same model family appears in the pipeline; judge leniency is suggested by the paper's own 6.4pp strict-vs-judge LongMemEval gap. Add a second judge or human annotation on at least the n=11 + a sample of the n=300. | No |
| R2-M4 | **Downstream impact measured via synthetic QA on author-constructed contexts, not a real agent task loop.** The 73pp figure is about a bare LLM answering a status question given a pasted context; it does not establish impact on an actual multi-agent workflow (tool mis-calls, wrong actions). Scope the claim or add an agentic-harness measurement. | No |

### MINOR concerns
- Reads counted only "over the first 26 days of the 30-day window" (L121) — why 26? Unexplained truncation.
- `use_count` summed "across active facts" (L121) — reads served before a fact was superseded are presumably dropped from the cumulative figure; clarify the counting rule.
- SGM noise experiment (L143, L145): "embedding drops further" under 300+ distractors — no number is given for embedding-under-noise; report it or delete the claim.
- SGM embedding F1=0.78 is derived by *assuming* 100% precision ("assuming comparable precision," L143) — embedding retrieval precision is typically <100%; either measure it or drop the F1.
- "50× speedup" from "<1 ms vs ~50 ms" (L143) — report both medians properly instead of bounds; 1ms/50ms is 50×, but "<1" vs "~50" could be anywhere from 50× to 500×.
- B1 gate latency: p50 only (n=1,000, L157); report p95/p99 — a gate on the write path is tail-sensitive.
- §5 scenario enumeration: "six tamper scenarios: (1)…(5)…; plus (6)" — renumber cleanly; also state explicitly that anchor #235 covers the 6-entry partial block (2,346 = 234×10 + 6).
- `verify_chain()` scalability: 2,346 entries is tiny; report recompute time/complexity at, say, 10⁶ entries or state the limitation.

---

## Reviewer 3 — Practical Impact & Deployment

**Overall rating: 3 / 5** (genuinely useful local-first engineering with real production mileage; impact narrowed by Chinese-only core paths, a threat model that excludes the most realistic adversary, and unremarkable benchmark accuracy)

### Strengths
- Real 30-day multi-agent production deployment (15 clients, 2,346 audit entries, 28,807 tracked reads) with daily integrity checks — rare and valuable in this literature.
- 23 client adapters sharing one SQLite file via junctions/symlinks is a simple, deployable idea that solves a real friction point (per-client memory silos on one machine).
- Consistent candor: Q-value mechanism admitted non-functional (L151), B1 gate admits it "detects value-flip conflicts only" and is Chinese-only (L159), fail-open registry default disclosed (L118, L137).
- Apache-2.0 + PyPI + 534 passing tests supports reproduction.

### MAJOR concerns

| # | Concern | Blocking? |
|---|---------|-----------|
| R3-M1 | **The audit mechanism's residual value excludes the adversary users will actually care about.** §3.4 concedes no protection against an attacker with write access who recomputes anchors, and external checkpointing is ruled out by the local-first design. What remains is detection of *accidental* corruption or naive tampering. That is still useful, but the abstract sells "tamper-evident audit … addressing EU AI Act Article 12" without this scoping. State the realistic adversary (buggy agent, accidental edit, unsophisticated tampering) in the abstract and contributions. | No |
| R3-M2 | **Chinese-only core paths substantially limit the practical audience of an English-language paper.** The predicate extractor yields zero pairs on English (L145); the B1 parser is "Chinese-only" (L159). For an international JSS audience, both flagship mechanisms are inert out-of-the-box. This must appear in the abstract/intro, not only deep in §3. | **Yes** (disclosure required, not a code change) |
| R3-M3 | **Deployment study is n=1 environment.** The 15 agents are on one machine under one usage pattern (apparently the authors' own). No workload diversity, no other-user data, no failure/anomaly analysis beyond "zero data loss." Frame §deployment explicitly as a single-environment case study. | No |

### MINOR concerns
- Fail-open source registry default (L118): reasonable for usability, but combined with the poisoning limitation (L137) the practical audit story is "bookkeeping, not security" — one sentence making this explicit in the abstract would prevent misuse by adopters.
- LongMemEval strict 62.4% is well below several cited systems (Engram 83.6%, Memanto 89.8%, MemStrata 95% — all self-reported, L75/78). The honest framing is appreciated, but the paper should directly address the implication: MemTether's competitive ground is governance, not retrieval accuracy. Say so.
- Who consumes the evidence export? No story about verification cadence, external anchoring options, or integration with existing compliance tooling — the practical value of `memtether court export` is asserted, not demonstrated.
- Read counting via `use_count` on fact rows means retrieval-that-matches-but-not-selected is untracked; fine, but note it when quoting "31K+."

---

## Number Consistency Check

| # | Claim | Locations (line numbers) | Status |
|---|-------|--------------------------|--------|
| 1 | 31K+ total operations | L31, L58 | ✓ 28,807 (reads, L121) + 2,346 (writes) = 31,153 |
| 2 | "31K+ **read** operations" | L58 | ✗ Mislabel — reads alone are 28,807 (28.8K); 31K includes the 2,346 writes. Abstract's "31K+ operations" (L31) is correct; fix the Intro wording. |
| 3 | Reads counted over first 26 of 30 days | L121 | ⚠ Unexplained 4-day truncation; reconcile or explain. |
| 4 | 2,346 audit entries | L58, L63, L121, L243 | ✓ Consistent |
| 5 | 235 anchors from 2,346 entries @ every 10 | L243 | ✓ 2,346/10 = 234.6 → 235 (partial final anchor); state the partial-anchor assumption explicitly. |
| 6 | 5/5 anchored-row scenarios detected; 6 scenarios total | L63, L243 | ✓ Consistent (5 anchored + 1 unanchored tail). |
| 7 | 15 agents / 15 clients / 15 sources | L31, L58, L92, L243 | ✓ Consistent |
| 8 | 23 client adapters; enumerated list | L31, L38, L92 | ✓ List counts to 23 only if WorkBuddy CN and WorkBuddy Intl are counted separately — make this explicit. |
| 9 | 73pp = 82% − 9% (9/11 − 1/11) | L253, L264, L272 | ✓ 72.7pp → 73pp, acceptable rounding. |
| 10 | 0.7pp = 100% − 99.3% (n=300) | L255, L265 | ✓ Consistent (300/300, 298/300). |
| 11 | Abstract: "n=11 discovery; **n=43 expanded, 57% gradeable**" | L31 | ✗ **Arithmetic impossibility:** 57% of 43 has no integer solution (24/43 = 55.8% → 56%; 25/43 = 58.1% → 58%). 24/42 = 57.1%, suggesting the denominator is 42, or the percentage comes from a different base. Verify and fix. |
| 12 | Abstract n=43 expanded vs §6.1 reporting only n=11 | L31 vs L253 | ⚠ [forward-ref] The 73pp headline in §6.1 is derived solely from n=11; the abstract's parenthetical implies an expanded analysis exists later. Ensure the later section reconciles 11 → 43 explicitly. |
| 13 | 1,857× entity-resolution gap | L64 | ⚠ [forward-ref] Not derived anywhere in the reviewed scope. |
| 14 | SGM: 84% = 105/125; 64% = 80/125; SQL F1 0.91; embedding F1 ≈0.78; 50× speedup; 1.3× recall ratio | L143 | ✓ 105/125 = 84%; 80/125 = 64%; F1 = 2·(1.0·0.84)/1.84 = 0.913; 84/64 = 1.31. ⚠ Embedding F1 assumes 100% precision (unmeasured); "50×" from "<1 ms vs ~50 ms" is loose. |
| 15 | LongMemEval 62.4% strict / 68.8% judge; standalone 58.3% strict | L31, L45, L66 | ✓ Consistent across abstract, note, and contributions. |
| 16 | B1: 100%/100% on 50 conflicts + 80 near-misses; dev 20/20; p50 = 0.037 ms (n=1,000) | L157 | ✓ Internally consistent; synthetic-only. |
| 17 | "zero uncorrected contradictions after 30 days" (L159) vs 11 cross-agent contradictions analyzed (L253) | L159 vs L253 | ✓ Reconcilable ("uncorrected" = all 11 were superseded), but the wording invites misreading; consider "zero unresolved contradictions." |
| 18 | Definition 1 type notation: `vf ⊆ T` etc. | L170 | ✗ Should be ∈ (scalar timestamps), not ⊆. |
| 19 | 534 passing tests | L31 | ⚠ Single mention; ensure the count matches the repository at submission time. |
| 20 | Table 1 vs Finding 1 vs §6.1 text | L257–273 | ✓ Consistent. |

**Summary:** 13 consistent, 5 with caveats/forward-references, 2 outright errors (items 2 and 11), plus the notation error in item 18. Item 11 (57% of 43) must be fixed before submission; item 2 is a one-word fix in the Introduction.

---

## Overall Recommendation

**Major Revision.** (R1: 3/5, R2: 3/5, R3: 3/5)

This is a genuinely useful systems paper with real production evidence and commendable honesty about its own limitations. It should not be rejected. But it cannot be accepted in its current form because:

1. The headline empirical claim (73pp) is carried by n=11 with no uncertainty quantification and a sampling design that partially presupposes the asymmetry (R1-M1, R1-M2) — **blocking**.
2. Both novel mechanisms are validated only on synthetic, Chinese-only, author-built benchmarks, and the Chinese-only scope is not disclosed at the paper's front (R2-M1, R3-M2) — **blocking**.
3. Benchmark results are not reproducible from the front matter (judge model, protocols, baselines unspecified) — **blocking until verified** against later sections.
4. The formal contribution is oversold relative to what §4 actually proves, and two numbers in the abstract are wrong or arithmetically impossible ("31K+ read operations"; "57% gradeable" of n=43).

Required for resubmission: statistical treatment of the contradiction analysis (CIs, exact test, matched comparison), prominent scoping of Chinese-only mechanisms, full benchmark protocol details, reframing of the "four theorems," softening of the EU AI Act claim, and correction of all items marked ✗ in the consistency table.

---

*Review generated from lines 1–279 of the manuscript source; items marked [forward-ref] are contingent on material expected in the unreviewed sections.*
