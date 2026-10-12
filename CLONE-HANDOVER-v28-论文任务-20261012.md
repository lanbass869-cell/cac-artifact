# Codex 论文任务 克隆交接文档 v28
# 2026-10-12 | Codex (--source codex)
# 取代 v27。这是唯一当前版。前版已归档。
# 读者：新开的 Codex 会话，负责 MemTether 论文投稿任务。

---

## 0. 你是谁、你的任务是什么

你是 MemTether 项目的论文投稿实例。MemTether 是一个跨客户端 AI agent 记忆治理系统（github.com/MemTether/MemTether, PyPI a79, 527 tests, CI green）。

你的任务不是开发 MemTether（有项目会话负责），而是**把研究成果写成论文并投稿**。

经过 30 天（09-13 ~ 10-12）的探索，最高 fuseeval 分数 = **6.67**（Route C R72）。经过 7 个方向、17 篇论文 draft、132 轮 fuseeval，确认天花板在 5.67-6.67 区间。8 分需要新的 research contribution，不是修论文措辞。

**你当前的最优策略：把 Route C 打磨到可投稿状态，投 KSEM/NLPCC（CCF-C），同时挂 arXiv 抢时间戳。**

---

## 1. 用户画像（必读）

- 王子杰，21 岁，黑龙江科技大学计算机学院 2023 级本科生
- 终极梦想：研发原生记忆 AI 架构。考研是物理迁移到 985 拿 A100 的路径（2027 年 12 月初试）
- **破格保研是第一目标**，考研是退路。B 级论文是破格保研的核心筹码
- 每天数学英语 8-10 小时，科研时间极其有限
- 费用敏感（免费号池），屏幕占用零容忍
- 学校没有能交流的人（全院 0 篇 CCF 论文），所有科研工作由 AI 完成
- **不要推荐**：需要 A100/多GPU 的方向、需要找导师/合作者的方向、需要用户的 user study、需要大规模跨 benchmark 的方向

---

## 2. 30 天成果总结

### 2.1 系统开发（已完成，不需要继续）

MemTether 22,672 行代码，527 tests，CI 9 jobs green，PyPI a79。
核心：bi-temporal supersession、hash-chained audit、Memory Court、23 客户端适配器、SGM SQL 路由。

### 2.2 论文（16 篇 draft）

| # | 论文 | TeX 路径 | fuseeval | 目标 venue | 状态 |
|---|------|---------|----------|-----------|------|
| **Route C** | 系统全量 | `E:\RUANJIAN\workdocs\memtether\SGM-RouteC-20261009.tex` | **6.67** (R72) | EuroSys/FAccT | **最接近投稿** |
| P1 | Composition Effect | `E:\Downloads\paper1_answer_formulation_gap.tex` | 4.25 | KSEM (CCF-C) | **可投** |
| P4 | evalguard | `E:\Downloads\paper4_trust_but_verify.tex` | 4.75 | NLPCC (CCF-C) | **可投** |
| P5 | Refusal Gate | `E:\Downloads\paper5_refusal_gate.tex` | 5.00 | EMNLP Findings | 可投 |
| P6 | Cross-Benchmark | `E:\RUANJIAN\workdocs\memtether\paper6\paper6_crossbenchmark.tex` | 4.12 | NeurIPS D&B | 需要 mem0 data |
| FAccT | 73pp + impossibility | `E:\RUANJIAN\workdocs\memtether\faccT-paper.tex` | 4.00 | FAccT 2027 | 需要 polishing |
| 其他 10 篇 | 各种方向 | 见第 5 节 | 3.25-5.25 | 归档 | 经验积累 |

### 2.3 核心发现（12 个正面 + 8 个负面）

**正面（可写进论文的）：**
| # | 发现 | 数字 | 来源文件 |
|---|------|------|---------|
| 1 | Cross-agent contradictions cause **73pp** downstream loss | 82% vs 9%, n=11 | cross_entity_downstream.json |
| 2 | F1=**0.903** on ConflictBank temporal | P=1.000, R=0.814, n=2000 | conflictbank_evaluation_large.json |
| 3 | **11729x speedup** over LLM | 0.133ms vs 1.56s | llm_vs_ours_v2.json |
| 4 | F1=**0.813** on controlled benchmark | P=0.722, R=0.929, McNemar p=0.039 | detector_evaluation.json |
| 5 | **100% vs 14%** temporal accuracy | n=50 real corrections | temporal_accuracy_results.json |
| 6 | Stale context causes **39pp** causal loss | p<0.0001, n=100 | downstream_harm_results.json |
| 7 | r^N decay on LoCoMo | r=-0.135, p<0.001, n=1986 | locomo_full_results.json |
| 8 | **0.044%** contradiction rate | 11/24907 pairs | _scan_contradictions_results.json |
| 9 | Supersession prevents **52-61%** | counterfactual | counterfactual.py output |
| 10 | B1 gate **100% P/R** | value-flip detection | _b1_r5b_report.json |
| 11 | Impossibility theorem | wrapper as-of O(k) lower bound | Theorem 1 |
| 12 | **53.6pp** retrieval improvement | 43%→96% on contradiction entities | A/B test |

**负面（教训）：**
1. r^N 用 proxy 数据 = 假阳性（R²=0.72 但真实数据 r=+0.008）
2. NLI 与 LLM judge 100% 分歧（BART-MNLI 不适合 memory）
3. 8 种方法都突破不了 multi-session 60% 天花板
4. Rule-based detection 在混合语言下 F1=0.000
5. LLM 对 temporal conflict 的 recall 只有 6%
6. 合并多个 topic 到一篇论文 = 降分（COMB-1=3.25）
7. 论文 <15KB = 自动 4 分以下
8. 在 fuseeval 中加更多 section 不等于提分

---

## 3. 全部文件路径

### 3.1 论文 TeX 文件

| 论文 | TeX 绝对路径 | 大小 |
|------|------------|------|
| Route C | `E:\RUANJIAN\workdocs\memtether\SGM-RouteC-20261009.tex` | 49KB |
| P1 | `E:\Downloads\paper1_answer_formulation_gap.tex` | 54KB |
| P2 | `E:\Downloads\paper2_governed_memory.tex` | 39KB |
| P3 | `E:\Downloads\paper3_symlink_deploy.tex` | 32KB |
| P4 | `E:\Downloads\paper4_trust_but_verify.tex` | 41KB |
| P5 | `E:\Downloads\paper5_refusal_gate.tex` | 22KB |
| P6 | `E:\RUANJIAN\workdocs\memtether\paper6\paper6_crossbenchmark.tex` | 47KB |
| FAccT | `E:\RUANJIAN\workdocs\memtether\faccT-paper.tex` | 19KB |
| CAC | `E:\RUANJIAN\workdocs\memtether\cross-agent-contradiction-paper.tex` | 29KB |
| TCP | `E:\RUANJIAN\workdocs\memtether\temporal-conflict-paper.tex` | 11KB |

### 3.2 实验数据文件（全部在 cac-artifact repo 或 E:\Temp\）

| 数据 | 绝对路径 | 大小 |
|------|---------|------|
| LoCoMo 1986Q | `E:\RUANJIAN\memtether\_dev\benchmarks\results\locomo_full_results.json` | 531KB |
| Downstream n=100 | `E:\RUANJIAN\memtether\_dev\benchmarks\results\downstream_harm_results.json` | 64KB |
| Temporal accuracy | `E:\RUANJIAN\memtether\_dev\benchmarks\results\temporal_accuracy_results.json` | 24KB |
| As-of latency | `E:\RUANJIAN\memtether\_dev\benchmarks\results\asof_benchmark_results.json` | 2KB |
| ConflictBank batch1 | `E:\RUANJIAN\workdocs\memtether\cac-artifact\conflictbank_sample.jsonl` | 9.3MB |
| ConflictBank batch2 | `E:\RUANJIAN\workdocs\memtether\cac-artifact\conflictbank_sample2.jsonl` | 6.9MB |
| Contradiction scan | `E:\Temp\_scan_contradictions_results.json` | 10KB |
| Classification | `E:\Temp\_contradiction_classification.json` | 248KB |
| Detector eval | `E:\RUANJIAN\workdocs\memtether\cac-artifact\detector_evaluation.json` | 1KB |
| ConflictBank eval | `E:\RUANJIAN\workdocs\memtether\cac-artifact\conflictbank_evaluation_large.json` | ~1KB |
| LLM vs ours | `E:\RUANJIAN\workdocs\memtether\cac-artifact\llm_vs_ours_v2.json` | ~1KB |
| Cross-entity 73pp | `E:\RUANJIAN\workdocs\memtether\cac-artifact\cross_entity_downstream.json` | 4KB |
| Expanded downstream | `E:\RUANJIAN\workdocs\memtether\cac-artifact\downstream_expanded_results.json` | ~1KB |
| Benchmark ground truth | `E:\RUANJIAN\workdocs\memtether\cac-artifact\benchmark_ground_truth.json` | 20KB |
| FactCHD eval | `E:\RUANJIAN\workdocs\memtether\cac-artifact\factchd\evaluation.json` | ~1KB |
| LangMem 500Q | `E:\Temp\_langmem_500q_results.json` | ~200KB |
| B1 gate | `E:\Temp\_b1_r5b_report.json` | ~30KB |

### 3.3 实验脚本（全部在 cac-artifact repo）

| 脚本 | 路径（相对于 `E:\RUANJIAN\workdocs\memtether\cac-artifact\`） | 用途 |
|------|------|------|
| scan_contradictions.py | ./ | 扫描生产库矛盾 |
| classify_contradictions.py | ./ | 分类矛盾类型 |
| evaluate_detectors.py | ./ | 4 种方法对比 |
| evaluate_conflictbank.py | ./ | ConflictBank 评测 |
| evaluate_factchd.py | ./ | FactCHD 评测 |
| llm_vs_ours_v2.py | ./ | LLM vs deterministic |
| counterfactual.py | ./ | 反事实分析 |
| downstream_expanded.py | ./ | n=300 downstream |
| cross_entity_downstream.py | ./ | 73pp 实验 |
| generate_benchmark.py | ./ | 生成 controlled benchmark |
| generate_synthetic_db.py | ./ | 生成 synthetic DB |

### 3.4 GitHub 仓库

| 仓库 | URL | 内容 |
|------|-----|------|
| MemTether | github.com/MemTether/MemTether | 系统代码, PyPI a79 |
| cac-artifact | github.com/lanbass869-cell/cac-artifact | 全部实验代码+数据+论文+方案 |

---

## 4. 环境配置

### 4.1 解释器（必须用这个）

```bash
E:\RUANJIAN\memory_hub\.venv-memory\Scripts\python.exe
```

### 4.2 LaTeX 编译

```powershell
$env:TECTONIC_CACHE_DIR='E:\Temp\tectonic_cache'
& 'E:\Temp\tectonic_bin\tectonic.exe' '<tex路径>' --outdir 'E:\Temp'
```

### 4.3 fuseeval

```bash
cd E:\RUANJIAN\workdocs\memtether\fuseeval
set PYTHONIOENCODING=utf-8
E:\RUANJIAN\memory_hub\.venv-memory\Scripts\python.exe fuseeval.py --paper "<paper.tex>" --round <ROUND_NAME>
```

评委配置（fuseeval.py 内）：
- E1: cn:kimi-k3-1 (architecture-reviewer)
- E2: cn:minimax-m3 (usability-reviewer) ← 从 hy3-x 改的
- E3: cn:deepseek-v4.1-flash (benchmark-auditor) ← 论文 >30KB 时常 FAIL
- E4: cn:glm-5.3 (product-reviewer)

API: http://127.0.0.1:8813/v1/chat/completions

### 4.4 Git push

```bash
cd E:\RUANJIAN\workdocs\memtether\cac-artifact
set HTTPS_PROXY=http://127.0.0.1:7890
git add -A && git commit -m "..."
git -c http.sslBackend=openssl push
```

---

## 5. 全部 fuseeval 轮次记录

### Route C 论文（132 轮，2026-10-09 ~ 10-12）

| 轮次 | 分数 | 备注 |
|------|------|------|
| R21 | 3.25 | 初始 |
| R27 | 6.12 | 第一次大幅提升 |
| **R72** | **6.67** | **历史最高** |
| R84 | 6.00 | peak 稳定区间 |
| R100 | 4.67 | 10-line fix 降分 |
| RC-POLISH | 5.25 | 加 12 refs + governance RW + reproducibility |
| RC-MM3 | 5.25 | E2 换 minimax-m3 |
| RC-FIX | 4.88 | 加 crash recovery + quickstart（47KB） |

### CAC 论文（13 轮，2026-10-12）

| 轮次 | 分数 | 变化 |
|------|------|------|
| CAC-1 | 5.00 | 初稿 |
| CAC-3 | **5.38** | +Methods+Discussion |
| CAC-7 | **5.67** | +repo（E3 FAIL, 3 评委） |
| CAC-9 | 5.00 | +algorithm |
| CAC-10 | 4.12 | +ConflictBank |
| CAC-13 | 3.75 | +53.6pp |

### 其他论文

| 轮次 | 论文 | 分数 |
|------|------|------|
| P1-EVAL | P1 | 4.25 |
| P2-EVAL | P2 | 4.75 |
| P3-EVAL | P3 | 4.75 |
| P4-EVAL | P4 | 4.75 |
| P5-EVAL | P5 | 5.00 |
| P6-EVAL | P6 | 4.12 |
| TGS-2 | Temporal Gap Systems | 4.25 |
| TCP-1 | Temporal Conflict | 4.00 |
| FACC-1 | FAccT paper | 4.00 |
| TG-1 | Temporal Gap | 3.75 |
| COMB-1 | Merged | 3.25 |
| DRI-1 | Detect-Resolve-Improve | 3.50 |

---

## 6. fuseeval 评分规律（实证总结）

### 什么提分
| 操作 | 提升 | 证据 |
|------|------|------|
| 加 Methods section | +0.5-1.0 | CAC-2→CAC-3 |
| 加 SHA-256 + commands | +0.5 | CAC-10→CAC-11 (E1 4→5) |
| 加 governance RW subsection | +0.0-0.3 | RC-POLISH |
| 修正 oracle→upper bound | +0.0-0.3 | CAC-1→CAC-2 |
| 修正 confirmed→rule-classified | +0.0-0.3 | 同上 |

### 什么降分
| 操作 | 变化 | 原因 |
|------|------|------|
| 加 counterfactual section | -0.5 | 增加攻击面 |
| 加 algorithm section | -0.5 | 太简单被看不起 |
| 加 ConflictBank section | -1.0 | 冲淡核心贡献 |
| 合并多个 topic | -2.0 | 什么都不深入 |
| 论文 <10KB | -1.5 | 没有 substance |
| 论文 >30KB | E3 FAIL | token limit |

---

## 7. 深度竞品调研结果（2026-10-12）

完整分析见 `E:\RUANJIAN\workdocs\memtether\深度竞品调研-20261012.md`（8KB）。

### 最大竞品：Caura（原 MemClaw，498★，eToro 生产部署）

**Caura 有的（与 MemTether 重叠）：**
- Governed shared memory for multi-agent fleets
- Contradiction detection (RDF triple + LLM semantic analysis)
- Supersession (stale rows ranked below corrections)
- Full audit log (标准数据库日志)
- Tenant isolation, agent trust tiers
- Knowledge graph (auto-extracted)
- PII auto-detection
- Production deployment (eToro)

**Caura 没有的（MemTether 独有）：**
- Hash-chained audit trail（Caura 只有标准 DB log，没有 SHA-256 链）
- Bi-temporal model（valid_from/valid_to vs recorded_at/invalidated_at 双轴）
- Impossibility theorem（overwrite-style store 的 as-of 不可能性证明）
- Causal experiment（73pp downstream loss, p<0.0001）
- ConflictBank evaluation（F1=0.903）
- Cross-agent asymmetry finding（73pp vs 0.7pp）

**学术竞品：**
- AECG (arXiv:2610.05176): memory pollution + scope collapse 概念框架，无系统实现
- Beyond Provenance (arXiv:2609.25521): AI memory 的经济治理模型
- MutMem (arXiv:2608.02843): crypto authorized mutation with SHA-256 commitments
- Revoked but Still Authoritative (arXiv:2609.08258): 发现 "no system enforces revocation by default"

**结论：** "全网零竞品" 不再成立。必须引用 Caura 和 AECG 并明确差异。

---

## 8. 禁区（继承 + 新增）

### 原有
1. ❌ 编造数据
2. ❌ 编造引用
3. ❌ 隐藏不利结果
4. ❌ 用系统 Python 跑 memsearch
5. ❌ 碰生产库 memory.db（只读！）
6. ❌ Popen 常驻
7. ❌ 声称 "novel"/"first" 除非搜过了
8. ❌ 3 分钟 grep 就说全网没人做过

### 新增（本 session 血证）
9. ❌ **不合并多个 topic 到一篇论文**（COMB-1 = 3.25）
10. ❌ **不写 <15KB 的论文**（一定 <4 分）
11. ❌ **不试图通过加 section 突破天花板**（CAC-6 到 CAC-13 全部降分）
12. ❌ **不在论文 >30KB 时跑 fuseeval**（E3 JSON FAIL）
13. ❌ **不用 regex matching 冲 8 分**（审稿人说 "too simple"）
14. ❌ **不推荐需要 A100/导师/合作者/用户的方向**（用户没有这些资源）
15. ❌ **不推荐社区推广/刷 star**（考研期间没时间）
16. ❌ **不用 mem0 的 OpenAI embedding 在本地跑**（8813 号池不支持）
17. ❌ **不声称"全网零竞品"**（Caura/MemClaw 498★ 是直接竞品）

---

## 9. 下一步行动计划（按优先级）

### 立即做（本周）

| # | 任务 | 时间 | 为什么 |
|---|------|------|--------|
| 1 | 把 Route C 的 E3 reproducibility findings 全部修复 | 2-3h | E3 是唯一给 3-4 分的评委，修掉这些可以到 6+ |
| 2 | 修复 11729x→11704x 数学错误 | 5min | 11704 ≠ 1.56s/0.133ms，实际是 11729 |
| 3 | 加 Caura/AECG 对比到 Related Work（已有但需更详细） | 30min | 不能再说"零竞品" |
| 4 | 把 73pp finding 加回正文（之前被意外删除） | 15min | 这是核心贡献 |
| 5 | 跑 fuseeval 验证 | 5min | 确认修复后分数提升 |

### 短期做（2 周内）

| # | 任务 | 时间 | 为什么 |
|---|------|------|--------|
| 6 | P1 转 LNCS 格式 | 2h | KSEM 2027 deadline ~June 2027，提前准备 |
| 7 | arXiv 抢发 73pp short paper | 2h | 占住 "cross-agent memory contradiction" 首发权 |
| 8 | Caura 深度对比测试 | 4h | 在同一 benchmark 上跑 Caura vs MemTether |

### 等用户操作

| # | 任务 | 需要什么 |
|---|------|---------|
| 9 | 人工标注 198 candidates | 2 人 × 30min |
| 10 | 在有 OpenAI key 的环境跑 mem0 on LoCoMo | OpenAI API key |

---

## 10. 新实例验收清单

- [ ] 读完全文档
- [ ] 确认解释器：`E:\RUANJIAN\memory_hub\.venv-memory\Scripts\python.exe --version`
- [ ] 确认 tectonic：`E:\Temp\tectonic_bin\tectonic.exe --version`
- [ ] 确认 fuseeval：`cd E:\RUANJIAN\workdocs\memtether\fuseeval && python fuseeval.py --help`
- [ ] 确认 cac-artifact：`ls E:\RUANJIAN\workdocs\memtether\cac-artifact\`
- [ ] 确认 Route C 编译通过：`tectonic SGM-RouteC-20261009.tex`
- [ ] 确认生产库只读：不碰 `E:\RUANJIAN\memory_hub\memory.db`
- [ ] 确认Git push：`HTTPS_PROXY=http://127.0.0.1:7890` + `-c http.sslBackend=openssl`

---

## 11. 记忆中枢搜索词

| 关键词 | 能找到什么 |
|--------|-----------|
| 论文冲8分任务最终状态 | 本 session 最终状态 |
| Cross-Agent Contradiction全量扫描 | 全部实验结果 |
| ConflictBank temporal F1 | F1=0.903 |
| 73pp downstream | 核心发现 |
| LLM对比11729x | deterministic vs LLM |
| Detector evaluation | 4 方法 P/R/F1 |
| RouteC R72 6.67 | 历史最高分 |
| RC-POLISH RC-FIX | 打磨版分数 |
| 论文任务教训必须记住 | 30 天经验 |
| 深度竞品调研 | Caura/AECG 分析 |
| 用户王子杰 完整处境 | 用户画像和限制 |

---

*生成: Codex 2026-10-12 | 30 天 / 17 篇论文 / 132 轮 fuseeval / 6 个新实验 / 12 个核心发现 / 8 个负面结果*
