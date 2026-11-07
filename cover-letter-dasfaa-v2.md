Dear DASFAA 2027 Program Committee,

We submit "Governed Agent Memory: Bi-Temporal Architecture, Write-Side Analysis, and Deployment-Aligned Evaluation" for consideration in the Research Track.

**Summary.** Agent memory systems are evaluated on retrieval accuracy, yet three deployment-critical capabilities remain unaddressed: temporal correctness guarantees, tamper-evident auditability, and deployment-aligned evaluation. We present a local-first memory system integrating all three, validated through 17 experiments including a 30-day pilot deployment serving 15 AI clients through 22 adapters.

**Key contributions:**

1. *Bi-temporal data governance.* A supersession model with four protocol-level correctness properties and a hash-chained audit layer (5/5 self-designed tampering scenarios detected; adversarial evaluation with 15 scenarios shows 33.3% detection rate, honestly reported).

2. *Write-side analysis from a pilot deployment.* At least 9.5% of memories are never retrieved; injection coverage is 0.48% (208× overscan). Temporal decay simulation reveals dead rate varies by memory age (CV=41.7%), correcting an earlier stability assumption.

3. *Deployment-aligned evaluation.* ClockScore (validated AUC=1.000 across 4 dataset types) quantifies deployment-generalization gaps. Cross-benchmark strict–judge gap direction reversal discovered.

4. *Hybrid read path.* Keyword-matched context slice with provenance tags beats full-context by +13.3pp (43.3% vs 30.0%) on LoCoMo while using 65.5% fewer tokens, confirming the "Lost in the Middle" effect. On LongMemEval_S, single-session questions achieve 84.0%; multi-session questions improved from 4.0% to 76.7% with graph-enhanced entity bridging.

5. *Cross-deployment stability.* Contradiction detection rate is stable (CV=3.7%) across three simulated deployment profiles with different data distributions.

6. *An open artifact.* GovernedMemory Bench (8,005 tasks) with chronological split. All experiment results (15 files with per-question data) publicly available.

**Honest limitations.** Single-operator deployment; no independent validation; adversarial security evaluation shows significant gaps; LongMemEval comparison uses different runs and judges; multi-session questions require knowledge graph architecture (partially addressed with SQLite recursive CTEs).

**Fit to DASFAA 2027.** The call explicitly welcomes AI-native data systems, data governance, and responsible data management. Our paper contributes bi-temporal data governance, write-side measurement, and deployment-aligned evaluation methodology.

**Double-blind compliance.** The submission is fully anonymized; all system names are replaced by generic descriptors.

The paper is 16 pages in LNCS format including references. It is not under consideration elsewhere.

Sincerely,
Anonymous Submission
