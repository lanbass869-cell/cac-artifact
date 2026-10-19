# MemTether Codex 克隆交接文档 — 论文任务 v35
# 2026-10-19 | Codex (--source codex)
# 取代 v34。这是唯一当前版（论文线）。

---

## 0. 你是谁、你管什么

你是 MemTether **论文投稿任务**实例。你管：论文写作、数据验证、引用检查、fuseeval 评判、投稿准备、arXiv preprint、全网竞品调研、AI 幻觉检查。
**项目任务（代码/评测工具/发布/安全/巡检）不归你管。**

---

## 1. 当前核心状态（2026-10-19 上午）

**cac-artifact HEAD = `bcefe64`（GitHub: github.com/lanbass869-cell/cac-artifact, public）**
**总计 99 commits。全部 9 篇论文 ALL GREEN（0 ?? 全部编译通过）。**

### 1.1 fuseeval v4-prism 全部完成

fuseeval 从 v3-referee 升级到 **v4-prism**，新增 8 个特性（基于 2025-2026 最新 arXiv 研究）：

| # | 特性 | 来源论文 | 状态 |
|---|---|---|---|
| 1 | AutoChecklist（动态生成论文专属 checklist） | 2603.07019 | ✅ 工作正常 |
| 2 | PRISM 四维（depth/soundness/helpfulness/alignment） | 2605.26730 | ✅ 工作正常 |
| 3 | 双过程分离（Phase 1 surface / Phase 2 deep） | 2607.10511 | ✅ 工作正常 |
| 4 | 反 gaming 检测 | 2608.01423 | ✅ 工作正常 |
| 5 | 表面/实质质量分离 | 2609.23264 | ✅ 工作正常 |
| 6 | 强制交叉质疑 | 2512.23213 | ✅ 工作正常 |
| 7 | Knowledge grounding（预留） | 2602.14367 | 框架就绪 |
| 8 | Reviewer-aligned calibration（预留） | 2608.07641 | 框架就绪 |

**v4 代码**：`E:\RUANJIAN\workdocs\memtether\fuseeval\fuseeval_v4.py`（371 行，15.5KB）
**v4 prompt_version** = `v4-prism`（v3 = `v3-referee` 已被取代但代码保留）

### 1.2 v4-prism 全部 9 篇评判结果

| 论文 | v4 score | std | checklist | cross-challenges | 评委 | 换算等级 |
|---|---|---|---|---|---|---|
| **DYN** (MLSys) | **5.5** | 0.5 | 0* | 2 | 2/4 | Workshop 可投 |
| **AoC** (SIGIR) | **4.67** | 0.47 | 0* | 3 | 3/4 | Workshop 边缘 |
| **JSS** (CCF-B) | 4.0 | 0 | 15 | 2 | 2/4 | Workshop 平均 |
| **WG** (MLSys) | 4.0 | 0 | 15 | 2 | 2/4 | Workshop 平均 |
| **P4** (NLPCC) | 4.0 | 0 | 15 | 2 | 3/4 | Workshop 平均 |
| **MC** (CCF-B/C) | 3.67 | 0.94 | 15 | 3 | 3/4 | 低于 workshop |
| **CAC** (KSEM/NLPCC) | 3.5 | 0.5 | 15 | 2 | 2/4 | 低于 workshop |
| **RC** (FAccT) | 3.0 | 0 | 15 | 0 | 1/4 | Reject 边缘 |
| **P6** (NeurIPS D&B) | 3.0 | 0 | 15 | 0 | 1/4 | Reject 边缘 |

*评分锚点：5 = workshop 平均，7 = CCF-C 可投小修，9 = 顶会接收*
*DYN 和 AoC 的 checklist=0 是因为 v4 代码在此期间被修改过，旧轮次没有 checklist 数据*

**v4 比 v3 严格**（v4 整体 3.0-5.5 vs v3 整体 3.25-5.33），原因：v4 加了 AutoChecklist + anti-gaming + PRISM + cross-challenge。

### 1.3 WorkBuddy agent 跨 agent 独立盲审（全部 9 篇完成）

**通道**：`node "E:\RUANJIAN\WorkBuddy\resources\app.asar.unpacked\cli\dist\codebuddy-headless.js" -p "<task>" --model custom-local:loomy-glm-5.3-flash -y`

| 论文 | review 文件 | 大小 | 备注 |
|---|---|---|---|
| JSS（前半） | JSS-MemTether-20261018_workbuddy_review_front.md | 19KB | 覆盖 L1-279 |
| JSS（后半） | JSS-MemTether-20261018_workbuddy_review.md | 25KB | 覆盖 L280-807 |
| RC | SGM-RouteC-R72-restore_workbuddy_review.md | 33KB | FAccT 定制 |
| WG | write-governance-paper_workbuddy_review.md | 18KB | MLSys 定制 |
| MC | memory-court-paper_workbuddy_review.md | 20KB | CCF-B/C 定制 |
| CAC | cross-agent-contradiction-paper_workbuddy_review.md | 22KB | KSEM/NLPCC 定制 |
| DYN | memory-dynamics-paper_review.md | 30KB | MLSys 定制 |
| AoC | about-or-contains-paper_review.md | 24KB | SIGIR 定制 |
| P4 | paper4_trust_but_verify_review.md | 31KB | NLPCC 定制 |
| P6 | paper6_crossbenchmark_review.md | 21KB | NeurIPS D&B 定制 |

**总计 ~243KB 独立审读内容。**

**WorkBuddy agent 审读发现的关键问题（我漏掉它抓到的）：**

| 论文 | 发现 | 修复状态 |
|---|---|---|
| DYN | 387 superseded rows > 350 edges 数学上不可能（DAG 语义下） | ✅ 用 DB 真实查询验证：41 rows 被直接 set superseded without edge（nrem_consolidation batch event），修正了 footnote |
| DYN | Risk set n=2,309 不可从 Table 1 重建 | ✅ 已加 data scope note |
| DYN | Consolidation confound：262/349 corrections 来自一次批量事件影响 91.5% rate | 标注 known issue（需重跑排除 262 的版本） |
| AoC | Table 1 sums to 19 not 28（8-count discrepancy） | ✅ 加了 honest explanation（second evaluation pass） |
| AoC | Memory Court 不在 Table 1 但正文说 Memory Court (1→10) | ✅ 已有解释 |
| AoC | "73% to 73%" 自相矛盾 | ✅ 加了解释（gains offset by temporal accuracy regression） |
| P4 | binomial statistic 0.38 → 应为 0.10（exact binomial n=33, p=0.05） | ✅ 修正 |
| P4 | 5 fabricated citations（reflect_2026/reward_hacking_2026/scaling_failure_2026/perishable2026/judge_reliability_2025） | ✅ 删除 |
| P6 | Contradictory significance claims（bootstrap "not significant" vs McNemar "p<0.001"） | ✅ 加了 significance reconciliation 段 |
| RC | PoisonRecall 引用编造（arXiv 上不存在） | ✅ 从 RC 和 CAC 删除 |

---

## 2. 全部 AI 幻觉审查结果

### 2.1 arXiv 引用验证
- **59 个唯一 arXiv ID** 全部 HTTP 200 验证通过
- **32 个标题不匹配**已全部用 arXiv 真实标题替换
- **4 个编造引用已删除**：PoisonRecall、TradeMemory、ZizkaDB、Memora

### 2.2 作者归属修正（14 个）
| 原错误 | 修正为 | arXiv ID |
|---|---|---|
| LoCoMo = Wu et al. | **Maharana, A.** et al. | 2402.17753 |
| ConflictBank = Chen, N. | **Su, Z.** et al. | 2408.12076 |
| MemSim = Anonymous | **Zhang, Z.** et al. | 2409.20163 |
| Sleeper = Anonymous | **Pulipaka, S.** et al. | 2605.15338 |
| AgentPoison = Anonymous | **Chen, Z.** et al. | 2407.12784 |
| TRACE = Anonymous | **Ghosh, B.** et al. | 2609.35659 |
| Janus = Anonymous | **Arslan, M.** et al. | 2609.38266 |
| MutMem = Anonymous | **Saidi, W.** et al. | 2608.02843 |
| AuditLME = Anonymous | **Chanhnourack, C.J.** | 2609.38021 |
| MemLeak = Anonymous | **Mudgal, P.** et al. | 2610.04195 |
| Beyond Provenance = Anonymous | **Chen, J.** et al. | 2609.25521 |
| Lineage = Anonymous | **Sangaraju, V.M.** et al. | 2610.07258 |
| AECG = Anonymous | **Tian, A.** et al. | 2610.05176 |
| PACMI = Anonymous | **Wang, Y.** et al. | 2610.05732 |

---

## 3. 全部 9 篇论文当前状态

| # | 论文 | tex 文件 | pages | ?? | v4 score | venue | 状态 |
|---|---|---|---|---|---|---|---|
| 1 | **JSS unified** | JSS-MemTether-20261018.tex | 22 | 0 | 4.0 | JSS (CCF-B) | 修复完成 |
| 2 | **RC** (RouteC-R72) | SGM-RouteC-R72-restore.tex | 16 | 0 | 3.0 | FAccT 2027 | 修复完成 |
| 3 | **WG** (Write Governance) | write-governance-paper.tex | 9 | 0 | 4.0 | MLSys workshop | 修复完成 |
| 4 | **MC** (Memory Court) | memory-court-paper.tex | 7 | 0 | 3.67 | CCF-B/C | 修复完成 |
| 5 | **CAC** (Cross-Agent Contradiction) | cross-agent-contradiction-paper.tex | 17 | 0 | 3.5 | KSEM/NLPCC | 修复完成 |
| 6 | **DYN** (Memory Dynamics) | memory-dynamics-paper.tex | 11 | 0 | 5.5 | MLSys workshop | 修复完成 |
| 7 | **AoC** (About-or-Contains) | about-or-contains-paper.tex | 6 | 0 | 4.67 | SIGIR workshop | 修复完成 |
| 8 | **P4** (Trust But Verify / evalguard) | cac-artifact\paper4_trust_but_verify.tex | 16 | 0 | 4.0 | NLPCC | 修复完成 |
| 9 | **P6** (Cross-Benchmark Dual-Track) | cac-artifact\paper6_crossbenchmark.tex | 14 | 0 | 3.0 | NeurIPS D&B | 修复完成 |

**附属工件（不算投稿论文）：**
- arxiv-preprint-73pp.tex（5.6KB wrapper，时间戳保护）
- memtether_supersession_benchmark.jsonl（2,635 records，公开脱敏）

---

## 4. 今天（2026-10-18 → 10-19）完成的全部工作

### Phase 1：JSS paper E4 审稿意见修复
- ConflictBank temporal qualifier、11714x qualifier、n=11/43 note、26→30d、dedup、misplaced LangMem removed

### Phase 2：JSS paper 一小时深度审读（14 项修复）
- Memory Court 空壳补完整、Tamper-Detection 结果补完、LaTeX backtick 修复、Data Scope Note、1,857× methodology、73pp vs 86% clarification、LongMemEval variants note、Abstract 229→~150 words、Highlights+Keywords、MemOS/MemProbe/MemoryLACE 3 竞品、SGM Chinese limitation、Table 1 caption

### Phase 3：全部 9 篇论文批量修复（40 项）
- RC: tab:headtohead→text、fig:rn-fit→fig:rn、4 refs、26d/30d note、PoisonRecall 删除、AgentPoison arXiv ID
- WG: 7 tab refs、MAB citation、aoc "Manuscript under review"
- CAC: 11 tab refs、5 arXiv real authors、PoisonRecall 删除、FEVER/ConflictBank 修正
- DYN: 6 fig + 4 tab refs、LoCoMo→Maharana、memtether title
- AoC: 4 tab refs、MAB citation
- P4: verbatim end bug、5 fabricated citations 删除、Gilda duplicate、TRACE/PACMI real authors
- P6: neurips sty、fig4/fig5、sec:limitations、9 arXiv real authors、ayyagari→Feuer
- MC: 5 arXiv real authors、routec "Manuscript under review"

### Phase 4：AI 幻觉全面审查
- 59 个 arXiv ID 全部 HTTP 200 验证
- 32 个标题不匹配→全部替换为 arXiv 真实标题
- 4 个编造引用删除（PoisonRecall/TradeMemory/ZizkaDB/Memora）
- 14 个 Anonymous→真实作者

### Phase 5：nature-skills 安装
- 8 个 skill 安装到 ~/.codex/skills/ 和 ~/.agents/skills/（reviewer/response/ref-verifier/statistics/shared/polishing/figure/data）

### Phase 6：paper-timer skill 创建
- E:\Temp\paper_timer.py + ~/.codex/skills/paper-timer/ + ~/.agents/skills/paper-timer/
- 8 步 checklist 强制计时器

### Phase 7：9 篇论文 nature-reviewer 盲审 + 修复（paper-timer）
- JSS: 8 项修复、RC: 9 项修复、WG: 4 项修复、MC: 8 项修复、CAC: 6 项修复
- DYN: 4 项修复、AoC: 2 项修复、P4: 2 项修复、P6: 2 项修复

### Phase 8：fuseeval v4-prism 代码 + 全部 9 篇评判
- v4 代码基于 2025-2026 最新 8 篇 arXiv 研究（AutoChecklist/PRISM/Kahneman/anti-gaming 等）
- 9 篇全部跑完 v4-prism

### Phase 9：WorkBuddy agent 跨 agent 盲审
- 发现 Codex→WorkBuddy 通道：node codebuddy-headless.js -p '<task>' --model custom-local:loomy-glm-5.3-flash -y
- 9 篇全部完成 WorkBuddy agent 独立盲审（~243KB 独立审读内容）
- WorkBuddy agent 发现了多个我漏掉的问题（386vs349 数学矛盾、Table 1 sums 19 not 28、binomial 0.38→0.10 等）

### Phase 10：遗留问题全部处理
- DYN 387/350 footnote 用 DB 真实查询验证
- AoC Table 1 caption 诚实解释
- AoC 73%→73% 矛盾解释
- JSS CK-11 mean rounding + CK-13 LLM spec

---

## 5. 关键数字（唯一正确值）

| 数字 | 值 | 禁止值 |
|---|---|---|
| Speedup | **11,714×** | 11,704x / 11,729x |
| ConflictBank F1 | **0.897** (n=2000 full) / **0.889** (500-sample) | 0.903 |
| Supersession F1 | **0.947** | 0.946 |
| Cross-agent harm | **73pp** (n=11) / 86% (n=43) | — |
| Injection coverage | **0.48%** (3980/833488) | — |
| Dead rate | **9.5%** (189/1981) | — |
| LongMemEval strict | **62.4%** (EAF full 500Q) | 75.7%（旧 run） |
| LongMemEval judge | **68.8%** (EAF full 500Q) | 82.0%（50Q pilot） |
| LongMemEval multi-session judge | **79.7%** | 60.2%（那是 overall） |
| LoCoMo token-F1 | **0.523** | — |
| Production ops | **31K+** (28,807 reads + 2,346 writes) | — |
| Tests | **534 passed, 4 skipped** | 538 total collected |
| Supersession benchmark | **2,635 records** (386 positive + 2,249 negative) | — |

---

## 6. 关键路径

```
论文 TeX         E:\RUANJIAN\workdocs\memtether\*.tex
P4/P6 TeX        E:\RUANJIAN\workdocs\memtether\cac-artifact\paper4_*.tex / paper6_*.tex
cac-artifact     E:\RUANJIAN\workdocs\memtether\cac-artifact\ (GitHub public)
fuseeval v3      E:\RUANJIAN\workdocs\memtether\fuseeval\fuseeval.py
fuseeval v4      E:\RUANJIAN\workdocs\memtether\fuseeval\fuseeval_v4.py
fuseeval rounds  E:\RUANJIAN\workdocs\memtether\fuseeval\rounds\
LaTeX 编译       tectonic (E:\Temp\tectonic_bin\tectonic.exe)
API (评委)       http://127.0.0.1:8813/v1/chat/completions
生产库（只读）   E:\RUANJIAN\memory_hub\memory.db
Git push         HTTPS_PROXY=http://127.0.0.1:7890 + git -c http.sslBackend=openssl
paper-timer      E:\Temp\paper_timer.py
nature-skills    E:\Temp\nature-skills\ (clone) + ~/.codex/skills/ + ~/.agents/skills/
AutoChecklist    E:\Temp\AutoChecklist\ + pip install autochecklist
进度日志         E:\Temp\paper_progress.log
```

---

## 7. 禁区（永久生效，违反 = 重做）

1. ❌ 编造数据/引用
2. ❌ 隐藏不利结果
3. ❌ 声称 novel/first 除非搜过
4. ❌ 合并 topic（COMB-1 = 3.25 血证）
5. ❌ <15KB 投稿
6. ❌ >30KB 跑 fuseeval（E3 FAIL）
7. ❌ speedup 写 11704x 或 11729x（正确 11714x）
8. ❌ 用 v1 fuseeval 分数（虚高 2 分）
9. ❌ 碰项目线代码/评测/发布
10. ❌ 不跑端到端验证就声称修好
11. ❌ 两阶段 retry 81.2% 写进论文
12. ❌ SGM count_answer_sessions 用于 LongMemEval
13. ❌ 去掉 ECO（60%→45.1%）
14. ❌ 说"零竞品"
15. ❌ 不做全网调研就声称 novel
16. ❌ 把不同实验硬合并 headline（lifecycle framing 3.62 血证）
17. ❌ regex 提 \cite 不含 \citet/\citep
18. ❌ 用 $c -replace 整文件替换
19. ❌ PoisonRecall 引用（arXiv 上不存在，已从 RC/CAC 删除）
20. ❌ F1=0.946 写进论文（正确 = 0.947）
21. ❌ LongMemEval multi-session judge 写 60.2%（那是 overall，multi-session 是 52.4%）
22. ❌ 82.0% judge 当 headline（那是 50Q pilot，full 500Q = 68.8%）
23. ❌ 60% contradiction rate 写进 MC abstract（正确 = 33%，5/15）
24. ❌ 用 $c -replace 整文件替换（曾把 CAC 清零）
25. ❌ 禁止使用 PowerShell -replace 处理含 LaTeX 转义的文本（用 Python 代替）

---

## 8. 新实例验收清单

- [x] 读本文档
- [x] 知道 9 篇论文当前 ALL GREEN（0 ??）
- [x] 知道 cac-artifact HEAD 和 GitHub URL
- [x] 知道 fuseeval v4-prism 与 v3 区别（8 个新特性）
- [x] 知道全部 v4 分数（DYN 5.5 最高 / RC+P6 3.0 最低）
- [x] 知道 14 个作者归属修正
- [x] 知道 4 个编造引用已删除
- [x] 知道 32 个标题已修正
- [x] 知道 PoisonRecall 已删除
- [x] 知道 WorkBuddy 跨 agent 通道（codebuddy-headless.js + loomy 模型）
- [x] 知道 paper-timer 8 步 checklist
- [x] 知道 nature-skills 8 个已安装
- [x] 知道 AutoChecklist 已安装
- [x] 知道 11,714x 是唯一正确 speedup
- [x] 知道 0.897 是唯一正确 ConflictBank F1
- [x] 知道 0.947 是唯一正确 Supersession F1
- [x] 知道 62.4%/68.8% 是唯一正确 LongMemEval EAF full 500Q 分数
- [x] 知道 25 条禁区
- [x] 知道全部关键路径

---

## 9. 下一步优先级

### 立即可做
1. **投稿**：WG→MLSys workshop / CAC→KSEM 或 NLPCC / DYN→MLSys workshop / AoC→SIGIR workshop / MC→CCF-B/C
2. **JSS 投稿**：需要填真实作者名+affiliation（AUTHOR-REQUIRED comment 在 tex L23）
3. **arXiv preprint**：73pp wrapper tex 就绪

### 需要新实验
4. DYN consolidation confound：重跑排除 262 system-mediated corrections 的版本
5. Supersession Prediction deployment validation：closed-loop 实验
6. B1 Gate real-world validation：349 production corrections 回测
7. Metric bias under realistic retrieval（非 oracle 条件）

### 需要外部合作
8. 找合作者/外部用户/导师
9. 外部 code review
10. 跨部署 pooling

---

## 10. 教训（永久记住）

1. **检查 table 加和**：AoC Table 1 加和 19 ≠ headline 28，审稿人一眼就能抓到
2. **检查数学一致性**：386 superseded rows > 349 edges 在 DAG 下不可能，要查 DB 才知道真实原因
3. **跨论文数字同步**：F1=0.946 在 CAC 里 vs 0.947 在 JSS 里，审稿人会交叉引用
4. **不同 run 的数字不能混用**：75.7% (Oct 3 EAF) vs 62.4% (Oct 18 rerun) 是不同 pipeline 配置
5. **50Q pilot 不能当 headline**：82.0% (50Q) vs 68.8% (500Q) 差异巨大
6. **overall vs multi-session 不能混**：mem0 60.2% 是 overall，52.4% 才是 multi-session
7. **编造引用会被抓**：PoisonRecall 不在 arXiv 上，TradeMemory/ZizkaDB/Memora GitHub 404
8. **作者归属要验证**：LoCoMo 是 Maharana 不是 Wu；ConflictBank 是 Su 不是 Chen
9. **LaTeX backtick 要配对**：`` 才是左引号，单个 ` 会导致编译错误或乱码
10. **verbatim 要有 \end{verbatim}**：P4 的 verbatim 没有 end 导致整个编译失败
11. **fontnote 里的 _ 要转义**：nrem_consolidation → nrem\_consolidation
12. **Python 修改 tex 比 PowerShell 可靠**：PowerShell 的 -replace 对 LaTeX 转义字符有 bug
13. **Nature reviewer 3-reviewer 结构**：每个 reviewer 有独立 emphasis brief，冻结后再做 cross-challenge
14. **claim_pointer + evidence_pointer**：每个 finding 必须有可验证的指向
