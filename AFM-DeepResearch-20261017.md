# 全网深度调研 — 新架构范式突破 60% Ceiling
# Codex source=codex | 2026-10-17 21:00
# 搜索：12 组 arXiv 关键词 + 8 篇 abstract 精读 + LLM advisor 分析

---

## 一、竞品格局（最高优先级发现）

| 系统 | LongMemEval | 核心方法 | 对我们的启示 |
|---|---|---|---|
| **MemStrata** | **95%** | Deterministic (S,R,O) supersession + bi-temporal | **不用 embedding 做 counting，用 SQL** |
| **xmemory** | **97.1%** | Schema-grounded，reads become constrained queries | 闭集 predicate vocabulary，写时验证 |
| **Memanto** | **89.8%** | 13 typed classes + deterministic routing <90ms | 类型化 schema + 问题路由 |
| **我们 (EAF)** | **60%** | embedding + evidence curation + LLM counting | ❌ 用 LLM 做 counting 是错误 |

**结论：三者都不用 embedding 做 aggregation。这是一个范式差异，不是程度差异。**

---

## 二、12 组 arXiv 搜索发现

### 直接竞品（最相关）
| 论文 | 核心做法 | 对 AFM 的启示 |
|---|---|---|
| **TallyMem (2610.19474)** | Event ledger + deterministic aggregation operators（COUNT_DISTINCT, SUM, SPAN_DAYS） | **和 AFM 几乎一样但更成熟。不是自由 SQL，是 ~10 个闭合操作符** |
| **ReFind (2608.12888)** | 原始 FTS5 + iterative keyword search，不加 semantic structure | **反向验证：结构可能不是问题。必须跑这个作为 baseline** |
| **post-graph-rag (2608.24921)** | PostgreSQL-native bi-temporal graph RAG | 我们已有 bi-temporal，但 graph RAG = LLM summarization（已失败） |
| **SuperLocalMemory 4.0 (2608.08253)** | Governed memory OS + RRF + hash chain | 基础设施级，不是 aggregation 方案 |

### 非直接竞品但有启发
| 论文 | 启示 |
|---|---|
| **Engram (2606.09900)** | Extraction 应该是 consolidation pass（批量），不是 write-time inline |
| **MemReader (2604.07877)** | From Passive to Active extraction — 主动抽取比被动抽取好 |
| **ModularSQL (2609.29573)** | Text-to-SQL 的 multiplicity blind spot — SQL 可能返回多个正确答案 |

---

## 三、LLM Advisor 分析（DeepSeek v4.1 Flash）

### ⚠️ 最重要的警告：先跑 Oracle Ceiling Diagnostic

> **"Before you build AFM, run the ceiling diagnostic. Non-negotiable."**
>
> 如果给 LLM gold evidence（正确答案对应的原文），EAF 能到多少？
> - **~70%** → 瓶颈在 reasoning/generation，AFM 无法解决
> - **~90%** → 瓶颈在 retrieval/aggregation，AFM 值得做
> 
> 诊断成本 ~1 天。建 AFM 成本 ~2 周。先跑诊断。

### AFM 的风险（Advisor 指出）

| 风险 | 严重度 | 说明 |
|---|---|---|
| **Extraction 遗漏/扰动** | 🔴 | "about a dozen"/"twice as many" 无法映射到数字 → 静默 NULL → **SQL 返回自信的错误答案**（比 retrieval miss 更糟） |
| **实体归一化** | 🔴 | "Dr. Chen" = "Maria Chen" = "the professor" → COUNT 碎片化 → 少数。**这是 KG 构建的经典陷阱，80% 的工程量** |
| **跨 session 去重** | 🔴 | 同一事件在多个 session 被提及 → 双重计数 |
| **问题-元组不匹配** | 🟡 | "How many..." 不总是简单 COUNT——可能需要 WHERE 过滤、时序条件、比较 |
| **刚性 schema** | 🟡 | 5-tuple 只能回答 "How many X"，其他类型问题需要路由 |

### AFM 的 Novelty 评估

> **"Is AFM novel? No."**
> - xmemory: "reads become constrained queries" = AFM read path
> - TallyMem: "event ledger + deterministic execution" = AFM write path
> - AFM 的唯一 novelty = "local-first SQLite + no GPU + router + fallback 的组合"
> - **这是工程贡献，不是研究贡献**

---

## 四、LLM Advisor 的最终建议

### 选哪种方案？

> **Bet on: (b) TallyMem-style event ledger + deterministic operators.**
>
> 理由：**降级安全**。AFM-5-tuple 的刚性 schema 意味着 extraction 错误 → 静默错误的 SQL 结果。Event ledger 保留原始事件作为 ground truth，deterministic operators 可以对照源文本验证，extraction 不确定时可以 fallback 到 retrieval。

### 第一步做什么？

> **Day 1-2: Oracle ceiling diagnostic。Non-negotiable.**
>
> 给 LLM gold evidence（正确答案对应的原文），跑 EAF 75 题。看能到多少。
> - **~70%** → 瓶颈在 reasoning，AFM/TallyMem 无法解决，放弃
> - **~90%** → 瓶颈在 retrieval/aggregation，proceed with event ledger
>
> **Day 3+: 如果 ceiling >90%，建 TallyMem-style event ledger**

---

## 五、修正后的 AFM 方案

基于调研结果，AFM 方案需要以下修正：

| 原方案 | 修正后 | 理由 |
|---|---|---|
| 自由 SQL on 5-tuples | ~10 个闭合 aggregation operators | 减少自由度，提高可靠性 |
| (subject, predicate, object, date, quantity) 5-tuple | (event_id, canonical_entity, predicate, object, date, quantity) + event ledger | 加 entity 归一化 + 原始事件回溯 |
| write-time inline extraction | batch consolidation (after write) | Engram 建议：提取是整合不是写入 |
| novelty claim: "first AFM" | novelty claim: "first local-first aggregation memory with bi-temporal + hash chain" | 诚实定位 |
| 直接建 AFM | **先跑 oracle diagnostic** | 1 天成本 vs 2 周赌注 |

---

## 六、行动计划

### Day 1-2: Oracle Ceiling Diagnostic
1. 从 LongMemEval 75 题中取每题的 gold answer_session_ids
2. 只注入这些 session 的内容（不是全部 haystack）→ 这是"完美 retrieval"的 evidence
3. 跑 EAF pipeline → 看 strict%
4. **判据：>90% = AFM 值得做 / <70% = 放弃，转投其他方向**

### Day 3-14: （如果 diagnostic >90%）
1. 建 event ledger（append-only，每个 turn 一行）
2. 实现 ~10 个 aggregation operators（COUNT_DISTINCT, SUM, SPAN_DAYS, SET_DIFF...）
3. LLM 写 event spec（不是自由 SQL），deterministic executor 执行
4. 问题路由：counting → event ledger / 其他 → EAF fallback
5. 75 题全量测试

### 论文贡献（若成功）
- 不是"first AFM"（novelty 已被占）
- 而是"first local-first aggregation memory with bi-temporal supersession + event ledger + deterministic aggregation"
- 加上 9+1 次失败文档 = "我们尝试了 10 种方法打破 60%，第 10 种成功了"

---

## 七、Full Search Summary

| 搜索方向 | 找到的关键论文 | 评估 |
|---|---|---|
| Schema-grounded | xmemory / SDAM / PatchBoard | xmemory = 最强，AFM read path 的 prior art |
| SQL + LLM | Graph Memory: At What Cost / ModularSQL | Graph DB 不是必需的（SQL 就够） |
| KG + agent memory | Selective Forgetting / MELD / GraphWake | 方向热但多为 graph DB，不是 SQLite |
| Text-to-SQL | DSABench / HarnessSQL | 成熟领域，AFM 可以借鉴 |
| Counting + LLM | Memorilla / Memento 3 | LLM counting 是已知弱点 |
| Event aggregation | **TallyMem** ⭐ | **最直接竞品/参考** |
| Temporal reasoning | EngramRAG / SF-AMS / MemReader | consolidation 方向有启发 |
| Bi-temporal | post-graph-rag / SuperLocalMemory / MemStrata | 直接竞品但可行性已验证 |
| ReFind | Raw chat search vs structured memory | **反向 baseline，必须跑** |
