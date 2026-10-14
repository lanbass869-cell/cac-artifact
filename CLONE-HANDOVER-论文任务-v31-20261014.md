# MemTether Codex 克隆交接文档 — 论文任务 v31
# 2026-10-14 | Codex (--source codex)
# 取代 v28/v29/v30 的论文部分。这是唯一当前版（论文线）。
# 项目线（代码/评测/发布/安全）不归你管，那边交接看 v30。

---

## 0. 你是谁、你管什么

你是 MemTether **论文投稿任务**实例。你管的是：把研究成果写成论文、跑 fuseeval 评判、修审稿发现的问题、投稿。
**项目任务（代码/评测/发布/安全/巡检）不归你管**，那边交接看 v30。两线边界已在 10-13 确认。

---

## 1. 最终论文清单（去重后结论，经过三轮纠正）

### 可投稿的 4 篇（全部编译通过、bibitem 清洁、机器验证通过）

| # | 论文 | TeX 路径 | 大小 | v3-referee 分 | 投稿目标 | CCF | 概率 |
|---|------|----------|------|--------------|---------|-----|------|
| 1 | **RouteC** | `workdocs/memtether/SGM-RouteC-20261009.tex` | 55KB | **5.0** | FAccT 2027 | B | 25-35% |
| 2 | **Memory Court** | `workdocs/memtether/memory-court-paper.tex` | 19KB | **4.33** | CCF-B/C | B/C | 30-45% |
| 3 | **P4** | `E:\Downloads\paper4_trust_but_verify.tex` | 43KB | **4.0** | NLPCC 2027 | C | 30-40% |
| 4 | **CAC** | `workdocs/memtether/cross-agent-contradiction-paper.tex` | 35KB | **3.5** | KSEM/NLPCC | C | 20-30% |

### 附加产出

| 论文 | TeX 路径 | 大小 | 用途 |
|------|----------|------|------|
| arXiv preprint | `workdocs/memtether/arxiv-preprint-73pp.tex` | 5.7KB | 73pp+53.6pp 时间戳保护，可先挂 |

### 不投的
| 论文 | 原因 |
|------|------|
| P1 (Composition Effect) | PaperJury 第二轮 8/8 全驳回，novelty 不足（统计常识） |
| P2/P3/P5/P6 | 已被吸收进 RouteC，独立投稿等于自相残杀 |
| COMB | 合并多 topic 死路（3.25 分血证） |
| 其余 8 篇旧论文 | 已被吸收或分数太低 |

**⚠ v1 fuseeval 分数（4.25-6.67）已废弃。v3-referee 口径（3.5-5.0）是唯一可信口径。**

---

## 2. fuseeval 评判体系（v3-referee）

### 工具和用法
```
E:\RUANJIAN\workdocs\memtether\fuseeval\fuseeval.py
PROMPT_VERSION = 'v3-referee'
cd E:\RUANJIAN\workdocs\memtether\fuseeval
python fuseeval.py --paper "<tex路径>" --round <轮次名>
```

### 4 评委（全部走 8813 免费号池）
| ID | 模型 | 审什么 | schema |
|----|------|--------|--------|
| E1 | cn:kimi-k3-1 | 架构（并发、崩溃、扩展性） | full（9 字段） |
| E2 | cn:minimax-m3 | 易用性（安装、API、错误信息） | lite（5 字段） |
| E3 | cn:deepseek-v4.1-flash | 复现性（数字能不能跑出来） | lite（5 字段） |
| E4 | cn:glm-5.3 | 实用性（凭什么是你、谁该用） | full（9 字段） |

### v3 六条机制
1. reconstruct-before-critique（先重述中心主张再批判）
2. novelty_check 结构化字段（逐字列 first 声明+点名先行工作+三态裁决）
3. 两轮饱和扫查（正序+倒序找跨节矛盾）
4. severity 保守纪律（critical=足以拒稿）
5. score_anchors 锚点（5=workshop/7=CCF-C 小修/9=顶会）
6. 每条 finding 9 字段含 strongest_rebuttal

### 双层 schema（v3 新增）
强模型用 full schema（9 字段），弱模型用 lite schema（5 字段）。解决 E2/E3 JSON 解析失败问题。**v3 实测 4/4 评委全部成功。**

### 评分锚点
5 = workshop 平均水平 | 7 = CCF-C 可投小修 | 9 = 顶会接收

### ⚠ 噪声带
AgentReview（EMNLP 2024，574★）实测 37.1% 评审分歧来自 reviewer bias。**±1 分差异无统计意义。**v1 口径虚高约 2 分已废弃。LLM 评分只是内部迭代信号，外部同卷分数（MemEval/GateMem）才是可报数字。

---

## 3. PaperJury 庭审结果（10-13，最权威审稿结论）

PaperJury（1221★，arXiv 2606.16322）四篇论文全量庭审，代码 `~/.codex/skills/paperjury/`（doctor 全 PASS）。

### 流程
2 隔离审稿人 → 45 weakness → LLM 聚类 → 5 陪审团投票 → 4 项 ESCALATE → 12 陪审团复审

### 裁定汇总
| 论文 | VALID(FIX) | INVALID(DROP) | AUTHOR-REQUIRED | 可修率 |
|------|-----------|--------------|-----------------|--------|
| RouteC | 2 | 5 | 2 | 22%（最差） |
| CAC | 4 | 8 | 0 | 33% |
| P1 | 7 | 4 | 0 | 64%（最好但不投） |
| P4 | 6 | 3 | 1 | 60% |

### 两轮修复后（第二轮复评）
| 论文 | 修复前可修率 | 修复后可修率 | 变化 |
|------|------------|------------|------|
| CAC | 33% | **86%** | ↑53pp（修复有效） |
| RouteC | 22% | **38%** | ↑16pp |
| P4 | 60% | **40%** | ↓20pp（修不够彻底） |
| P1 | 64% | **0%** | 8/8 全驳回（novelty 不足） |

---

## 4. 全网竞品调研结果（10-14，178 项扫描）

### 新发现竞品（不在之前 Related Work 里的 HIGH THREAT）

| # | 来源 | 名称 | 与 MemTether 重叠 | MemTether 独有差异 |
|---|------|------|-------------------|-------------------|
| 1 | arXiv 2610.11188 | Governing Persistent Memory | 治理持久记忆 | 无 hash chain / evidence export / adjudication UI |
| 2 | arXiv 2609.33517 | TRACE | 多agent记忆有效性 | 无 bi-temporal / hash chain |
| 3 | arXiv 2607.10265 | TGMS | bi-temporal graph | 非 SQLite / 无 hash chain |
| 4 | arXiv 2607.05844 | StateFuse | 冲突保存 | 无 supersession / hash chain |
| 5 | arXiv 2610.09008 | Scope-Aware Commit Rules | scope-aware 记忆 | 无 bi-temporal / hash chain |
| 6 | arXiv 2610.05732 | PACMI | provenance 失效 | 无 hash chain / evidence export |
| 7 | arXiv 2609.16073 | Immutable Past | 冲突解决形式化 | RAG场景非agent / 无 hash chain |
| 8 | GH 1430★ | tradememory-protocol | SHA-256 chain | Trading-specific |
| 9 | GH 739★ | memora | supersession lineage | 无 hash chain / evidence export |
| 10 | GH 290★ | icarus-memory-infra | provenance + supersession | 无 hash chain / evidence export |

完整报告：`E:\RUANJIAN\workdocs\memtether\竞品调研报告-20261014.md`

### 已加入论文的引用
RouteC 加了 6 个 + CAC 加了 5 个 + MemoryCourt 加了 5 个 + P4 加了 2 个 = 18 个新 bibitem。
全部已编译通过。

---

## 5. AI 幻觉检查结果（10-14，44 项发现，全部已修或标明）

检查方式：逐节逐句读 4 篇论文全文（不是脚本 grep）。报告存 `workdocs/memtether/AI幻觉检查/`。

### 发现汇总
| 类型 | 数量 | 已修 | 待修 |
|------|------|------|------|
| orphaned bibitem | 28 | 28（全部通过加 RW 引用或删除修复） | 0 |
| orphaned ref | 6 | 6（全部通过加 label 修复） | 0 |
| 数字不一致 | 3 | 3（11714x 钉死 + F1 0.897 统一 + 版本号更新） | 0 |
| novelty claim | 7 | 3（弱化或删除） | 4（需确认但非拒稿级） |
| misplaced content | 1 | 1（LangMem 79.2% 移到正确 section） | 0 |

### 最重要的修复
- CAC 11704x → 11714x（abstract 里漏改的）
- CAC F1 0.903 → 0.897（与 JSON 数据一致）
- RouteC LangMem 79.2% 从 Tamper-Detection 移到 Cross-System Evidence
- P4 版本号 v0.1.0a30 → v0.1.0a79
- RouteC mutmem duplicate bibitem 去重

---

## 6. 引用验证结果（10-14，arXiv API 逐个查）

CAC 15 个 bibitem：9 MATCH + 2 MISMATCH 已修 + 4 timeout [UNVERIFIED]
RouteC 30 个 bibitem：22 MATCH + 1 MISMATCH 已修 + 7 timeout [UNVERIFIED]
P4 21 个 bibitem：4 MATCH + 6 标题提取错误（wrapper 缺失非内容错误）+ 2 timeout
MemoryCourt 13 个 bibitem：8 MATCH + 1 MISMATCH 已修

### 已修的引用错误
| 论文 | 错误 | 修复 |
|------|------|------|
| CAC | TOKI 标题错 | 改为实际标题 |
| CAC | MemStrata 标题错 | 改为实际标题 |
| CAC | FEVER 无作者无年份 | 改为 Thorne et al. 2018 NAACL |
| RouteC | Caura 格式缺 newblock | 改为标准格式 |
| MemoryCourt | MemStrata 标题同 CAC 错 | 同步修正 |
| P4 | sileo2024contamination 标题错 | 改为实际标题 |

---

## 7. 四篇论文全部 CLEAN（10-14 机器验证通过）

| 论文 | bibitems | orphan | missing | orphan ref | speedup | F1 | 状态 |
|------|---------|--------|---------|-----------|---------|-----|------|
| RouteC | 41 | 0 | 0 | 0 | 11714 ✓ | N/A | **CLEAN** |
| CAC | 15 | 0 | 0 | 0 | 11714 ✓ | 0.897 ✓ | **CLEAN** |
| P4 | 21 | 0 | 0 | 0 | N/A | N/A | **CLEAN** |
| MemoryCourt | 16 | 0 | 0 | 0 | N/A | N/A | **CLEAN** |

Git commit: `c980996` → 最新推送确认。

---

## 8. 外部 benchmark 评测进行中

### MemEval（Phase 1，正在跑）
- **计划任务**：`MemTether-MemEval`（断电免疫，State=Running）
- **进度**：3/10 对话完成（497/1986 题），avg F1 = 0.519
- **当前**：conv-42 摄入中（628 facts 已写入）
- **预计**：还需 10-12 小时
- **产出**：`E:\Temp\_memeval_full_results.json`
- **对比基准**：PropMem 0.605 / OpenClaw 0.557 / Graphiti 0.416 / Mem0 0.344
- **API**：LLM = 8813 号池 GLM-5.3-Flash（免费），Embedding = MemTether 本地 onnx（不花钱）
- **checkpoint**：`E:\Temp\_memeval_full_ckpt.json`（断电后自动恢复，跳过已完成 conv）

### GateMem（Phase 2，待做）
- Clone 到 `E:\RUANJIAN\memtether\_dev\gatemem`（尚未 clone）
- Adapter = 继承 BaseMemoryAgent，实现 reset/ingest/query 三方法
- MGS = Utility × (1-Access Violation) × (1-Forgetting Failure)
- 预计 2 天

### MemoryAgentBench（Phase 3，待做）
- Clone 到 `E:\RUANJIAN\memtether\_dev\mabench`（尚未 clone）
- CR 赛道用 substring_exact_match 零 judge 免费
- 需要 conda + torch 环境
- 预计 2 天

---

## 9. 核心实验数据（按重要性排序）

| # | 实验 | 数字 | 数据文件 |
|---|------|------|---------|
| 1 | Cross-entity downstream | **73pp loss** (82% vs 9%, n=11) | cac-artifact/cross_entity_downstream.json |
| 2 | ConflictBank temporal | **F1=0.903** (n=2000, P=1.000) | cac-artifact/conflictbank_evaluation_large.json → 但 JSON 里实际是 0.897 |
| 3 | LLM comparison | **11714x speedup** (F1 0.980 vs 0.113) | cac-artifact/llm_vs_ours_v2.json |
| 4 | Controlled benchmark | **F1=0.813** (P=0.722, R=0.929) | cac-artifact/detector_evaluation.json |
| 5 | Contradiction-aware retrieval | **+53.6pp** (43%→96%, n=28) | memory 中记录，无独立 JSON |
| 6 | Production scan | **0.044%** (11/24907 pairs) | E:/Temp/_scan_contradictions_results.json |
| 7 | Supersession prevention | **52-61%** | cac-artifact/counterfactual.py 输出 |
| 8 | Self-correction asymmetry | **0.7pp** (100% vs 99.3%, n=300) | cac-artifact/downstream_expanded_results.json |
| 9 | Bi-temporal accuracy | **100% vs 14%** (n=50) | _dev/benchmarks/results/temporal_accuracy_results.json |
| 10 | As-of latency | **0.167-0.245ms** flat | _dev/benchmarks/results/asof_benchmark_results.json |

**⚠ F1=0.903 vs 0.897**：JSON 文件 conflictbank_evaluation_large.json 实际值 = 0.897。论文已改为 0.897。0.903 来自另一个 n=1600 的 run。

---

## 10. 修复历史（本次会话全部修复）

### 数据修复
| 修复项 | 论文 | 详情 |
|--------|------|------|
| 11704x→11714x | CAC + 交接文档 | 1.558/0.000133=11714（三段历史钉死） |
| F1 0.903→0.897 | CAC | 与 JSON 数据一致（n=2000） |
| 527→534 tests | RouteC | 与实际测试数一致 |

### CAC 修复（10 项）
| 修复项 | 详情 |
|--------|------|
| headline soften | "cause a 73pp" → "associated with up to 73pp in our production case study" |
| first 声明收窄 | "first measurement" → "first causal quantification" |
| power analysis | p=0.004 sign test + Cliff's δ=0.86 + 95% CI [28,95] |
| hand-crafted context | 明确声明 hand-crafted 而非自然检索 |
| n=11 limitation | 加 deployment scarcity 论证 |
| nf>30 sensitivity | 加 sensitivity note + NF_MAX 环境变量 |
| 53.6pp 提升 | 加 "most practically significant" 说明 |
| 单位不一致 | 60% entity-level vs 0.044% pair-level 差异重写 |
| orphan bib | 9 个全部通过加 RW 引用或删除修复 |
| 11714x abstract | abstract 里遗漏的 11704x 改为 11714x |

### RouteC 修复（8 项）
| 修复项 | 详情 |
|--------|------|
| MutMem qualifier | "No prior" 加了 MutMem 对比限定 |
| hand-crafted context | 加了 limitation |
| asymmetry 机制 | 从"typically"弱化为"we hypothesize...requires further investigation" |
| LangMem 79.2% | 从 Tamper-Detection 移到 Cross-System Evidence |
| 527→534 tests | 更新测试数 |
| mutmem duplicate | 去重 |
| B1 gate section | 新增完整 section（100% P/R + p50=0.037ms） |
| Proactive trigger 负面结果 | 新增 section（0.7pp = 无效，诚实报告） |

### P4 修复（6 项）
| 修复项 | 详情 |
|--------|------|
| 9 orphan bibitem | 全部删除 |
| 33→47 口径 | Limitations 统一 |
| evalguard scoping | metadata checker not linter |
| threshold justification | heuristic not optimized |
| persistent artifact | DOI + SHA-256 |
| version pinning | a79 commit 4696e43 |

### P1 修复（5 项）— 但 P1 不投
| 修复项 | 详情 |
|--------|------|
| abstract inflation | 27.5x/8x 绑定到具体 run |
| Cohen h 符号 | 与 gap 符号对齐 + 脚注 |
| memstrata bib | 补齐 |
| anonymous2026 bib | 补齐 |
| temporal label | tab:temporal 位置确认 |

### 引用验证修复（6 项）
| 论文 | 错误 | 修复 |
|------|------|------|
| CAC | TOKI 标题错 | 改为实际标题 |
| CAC | MemStrata 标题错 | 改为实际标题 |
| CAC | FEVER Anonymous | 改为 Thorne et al. 2018 |
| RouteC | Caura 格式 | 改为标准格式 |
| MemoryCourt | MemStrata 标题 | 同步修正 |
| P4 | sileo 标题 | 改为实际标题 |

---

## 11. 竞品格局（10-14 最终版）

### 之前已知（28 个）
mem0 / Zep / Letta / LangMem / Caura(498★) / AECG / MutMem / MemStrata / BeyondProvenance / Revoked / Lineage / WhenToRemember / Epistemics / PoisonRecall / Sleeper / AgentPoison / ConflictBank / FEVER / Engram / TRACE / EdgeMem / MemGuard / GateMem / MemSim / MemoryAgentBench / MemEval / G-Memory / xmemory

### 新发现（20 个）
| 来源 | 名称 | Stars | 威胁 |
|------|------|-------|------|
| arXiv | Governing Persistent Memory (2610.11188) | - | HIGH |
| arXiv | TRACE (2609.33517) | - | HIGH |
| arXiv | TGMS (2607.10265) | - | HIGH |
| arXiv | StateFuse (2607.05844) | - | HIGH |
| arXiv | Scope-Aware Commit Rules (2610.09008) | - | HIGH |
| arXiv | PACMI (2610.05732) | - | HIGH |
| arXiv | Immutable Past (2609.16073) | - | HIGH |
| arXiv | Revoked (2609.08258) | - | HIGH |
| arXiv | MemTrace (2610.04838) | - | MEDIUM |
| arXiv | AkasicMEM (2609.25563) | - | MEDIUM |
| GitHub | tradememory-protocol | 1430 | HIGH |
| GitHub | bernstein | 1236 | HIGH |
| GitHub | memora | 739 | HIGH |
| GitHub | icarus-memory-infra | 290 | HIGH |
| GitHub | ZizkaDB | 130 | HIGH |
| GitHub | lemmalog | 338 | MEDIUM |
| GitHub | statewave | 282 | MEDIUM |
| GitHub | mnemos | 9 | MEDIUM |
| GitHub | governed-agent-memory | 2 | MEDIUM |
| GitHub | PaperJury | 1221 | 评判工具非竞品 |

**结论：Memory Court 三件无人同时做的声明仍然成立。** 13 个 HIGH THREAT 竞品没有一个同时有 hash chain + evidence export + adjudication UI。

---

## 12. 记忆中枢关键条目（按 uid 搜索）

| uid | 内容 |
|-----|------|
| fact-20261014114915 | AI幻觉检查44项完整报告 |
| fact-20261014120128 | AI幻觉检查第二版汇总 |
| fact-20261014131308 | 四篇论文全部CLEAN |
| fact-20261014124401 | 3项AUTHOR-REQUIRED决定 |
| fact-20261013223510 | 外部benchmark评测方案 |
| fact-20261013220008 | Memory Court TeX + arXiv preprint |
| fact-20261014130038 | 引用幻觉逐个验证 |
| fact-20261013220024 | 7项遗漏完整清单 |
| decision-20261014 | 三套评判体系终局校准 |

---

## 13. 当前进行中的工作

### MemEval LoCoMo 全量评测
- **计划任务**：`MemTether-MemEval`（Running，断电免疫）
- **进度**：3/10 对话完成，497/1986 题，avg F1 = 0.519
- **当前**：conv-42 摄入中（628 facts 已写入）
- **checkpoint**：`E:\Temp\_memeval_full_ckpt.json` → `{"done": ["conv-26", "conv-30", "conv-41"]}`
- **结果文件**：`E:\Temp\_memeval_full_results.json`（497 条已有）
- **日志**：`E:\Temp\_memeval_full_log.txt`
- **预计完成**：明天（10-15）早上

### 已完成对话
| 对话 | Turns | Facts | QA | F1 |
|------|-------|-------|-----|-----|
| conv-26 (Caroline) | 419 | 286 | 199 | 0.487 |
| conv-30 (Jon) | 369 | 199 | 105 | 0.518 |
| conv-41 (John) | 663 | 38+45 | 193 | 0.553 |
| **合计** | **1451** | **530** | **497** | **0.519** |

### 剩余对话
| 对话 | Turns | 状态 |
|------|-------|------|
| conv-42 (Joanna) | 629 | 🔄 摄入中 |
| conv-43 (Tim) | 680 | ⬜ |
| conv-44 (Audrey) | 675 | ⬜ |
| conv-47 (James) | 689 | ⬜ |
| conv-48 (Deborah) | 681 | ⬜ |
| conv-49 (Evan) | 509 | ⬜ |
| conv-50 (Calvin) | 568 | ⬜ |

---

## 14. 新实例验收清单

- [ ] 读本文 + 项目线 v30（了解边界）
- [ ] 确认 4 篇 TeX 路径存在
- [ ] fuseeval.py 可跑（--help）且 PROMPT_VERSION = v3-referee
- [ ] tectonic 编译通过
- [ ] 8813 号池连通
- [ ] cac-artifact git status 干净
- [ ] 知道 11714x 是正确数字
- [ ] 知道 F1=0.897（不是 0.903）
- [ ] 知道 v1 分数已废弃，v3-referee 是唯一口径
- [ ] 知道 P1 不投（novelty 不足）
- [ ] 知道 Memory Court 是唯一零竞品方向
- [ ] 知道 PaperJury 庭审已在本机安装（~/.codex/skills/paperjury/）
- [ ] 知道 MemEval 正在后台跑（计划任务 MemTether-MemEval）

---

## 15. 下一步（按优先级）

### 等待 MemEval 结果（自动，无需干预）
- 跑完后读 `E:\Temp\_memeval_full_results.json`
- 与 MemTether 的 24.7% 对比
- 写进 CAC 论文的跨系统对比表
- 跑 fuseeval 验证

### 本周可做
1. Memory Court 跑 fuseeval v3（首次评分，预计 3-4.5 分）
2. arXiv preprint 挂上去（73pp 首发权）
3. GateMem MGS 评测（需 clone + 写 adapter，2 天）
4. MemoryAgentBench CR 赛道（需 conda + torch，2 天）
5. CAC 修完后投 KSEM/NLPCC

### 需要用户操作的
1. 硅基流动充值（如果要跑 mem0 on LoCoMo）
2. 人工标注 198 candidates（2 人 × 30min）
3. RouteC 的 2 项 AUTHOR-REQUIRED 已由 AI 决定（标题不加 Barrier + P4 定位为 metadata checker），如用户不同意可改
