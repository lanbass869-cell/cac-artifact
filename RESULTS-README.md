# Experiment Results — Governed Agent Memory (DASFAA 2027)

All experiment result files with per-question data. Every number in the paper traces to a file in this directory.

## Reproduction

All experiments run on a single local machine (Intel CPU, 32GB RAM, no GPU).
LLM backend: spark-x2.6 via Loomy (127.0.0.1:17890). Embedding: bge-m3 (int8) or all-MiniLM-L6-v2.
Judge: spark-x2.6 (unified judge, temperature=0.0, max_tokens=500).

## Experiment Results

### Core Benchmarks

| File | Description | Paper Section |
|------|-------------|---------------|
| `eaf_500q_full_v2_result.json` | LongMemEval-500 per-question results (494 questions) | §4 Evaluation |
| `mem0_locomo_per_question.json` | mem0 answers on LoCoMo conv0 (82 questions) | §7 Deployment Obs |
| `our_locomo_per_question.json` | Our system answers on LoCoMo conv0 (82 questions) | §7 Deployment Obs |
| `mem0_locomo_judged.json` | mem0 answers judged by spark-x2.6 | §7 Deployment Obs |

### Experiments Addressing Reviewer Feedback

| File | Description | Addresses |
|------|-------------|-----------|
| `concurrent_writer_test.json` | 5-writer SQLite WAL concurrency test (500 writes) | No concurrent write test |
| `split_sensitivity.json` | Split boundary sensitivity (n=1000 to 3000) | Is 1581 cherry-picked? |
| `memstrata_bootstrap_ci.json` | Paired bootstrap CI for MemStrata F1 margin | No statistical test |
| `adversarial_evaluation.json` | 15 adversarial tampering scenarios (AgentPoison taxonomy) | 5/5 self-designed only |
| `multi_deployment_stability.json` | 3 simulated deployments cross-dataset stability | Single deployment only |
| `fullcontext_baseline.json` | FullContext baseline on LoCoMo (30 questions) | Missing FullContext baseline |
| `clockscore_systematic.json` | ClockScore systematic evaluation (4 dataset types) | ClockScore not validated |
| `temporal_decay.json` | Temporal decay analysis (dead rate by memory age) | Dead rate stability claim |
| `supersession_ablation.json` | Supersession mechanism ablation | No ablation on supersession |

### New Experiments (GAP1-3)

| File | Description | Result |
|------|-------------|--------|
| `hybrid_readpath_results.json` | Hybrid read path on LoCoMo 30 questions | **43.3%** vs FullContext 30.0% |
| `latency_cost_analysis.json` | Latency/cost: p50/p95 search + total + tokens | 65.5% token savings |
| `unified_judge_results.json` | 494 questions re-judged with spark-x2.6 | 75.4% vs 68.8%, 92.7% agreement |
| `judge_calibration_fulltext.json` | Judge calibration on PeerRead ICLR 2017 (20 papers) | Correlation 0.438 |
| `locomo_mcnemar.json` | Paired McNemar: mem0 vs our system on LoCoMo | mem0 15.9% vs ours 11.0%, p=0.289 |

### Previous Experiments

| File | Description |
|------|-------------|
| `crash_recovery_10cycles.json` | 10-cycle crash-recovery hash-chain integrity |
| `tamper_detection_results.json` | 5 self-designed tampering scenarios |
| `latency_2635_records.json` | Read latency on 2,635-record database |
| `ablation_system.json` | System-level ablation (5 conditions) |
| `memstrata_baseline.json` | MemStrata SPO proxy comparison |
| `scale_baseline_throughput.json` | Scale stability and throughput |
| `mem0_headtohead_20261106.json` | mem0 v2.2.1 growth on 200 identical records |
| `hindsight_cross_system.json` | Hindsight 1.1.0 cross-system growth |

## Key Findings

1. **Hybrid read path beats FullContext**: 43.3% vs 30.0% on LoCoMo (+13.3pp, 65.5% fewer tokens) — confirms "Lost in the Middle" effect
2. **FullContext baseline**: 30.0% >> mem0 16.7% >> our system 10.0% — memory system needed only when context exceeds window
3. **Adversarial security**: hash-chain audit detects only 5/15 (33.3%) adversarial scenarios
4. **Judge calibration**: LLM judge correlates 0.438 with human scores on PeerRead — not reliable enough to replace human reviewers
5. **Cross-deployment stability**: contradiction detection rate is stable (CV=3.7%) across different data distributions
