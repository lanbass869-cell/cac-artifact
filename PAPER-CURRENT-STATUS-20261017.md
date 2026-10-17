# MemTether 论文线 — 当前状态速查（2026-10-17）

## 一、7 篇投稿论文（v33 清单）

| # | 论文 | TeX | 最新 fuseeval | 评委 | 投稿目标 | 当前状态 |
|---|---|---|---|---|---|---|
| 1 | **RC** | SGM-RouteC-20261009.tex | **5.33** (v3-RC-v2) | 3/4 (E1=6!) | FAccT 2027 | ✅ 修复完成 |
| 2 | **WG** | write-governance-paper.tex | **4.75** (v3-WG-v5) | 4/4 (E2=6!) | MLSys workshop | ✅ 修复完成 |
| 3 | **MC** | memory-court-paper.tex | **4.75** (v3-MC-v4) | 4/4 (E2=6!) | CCF-B/C | ✅ 修复完成 |
| 4 | **CAC** | cross-agent-contradiction-paper.tex | **4.33** (v3-CAC-v10-final) | 3/4 (E3 FAIL) | KSEM/NLPCC | ✅ 修复完成 |
| 5 | **DYN** | memory-dynamics-paper.tex | **4.25** (v3-DYN-v4) | 4/4 | MLSys workshop | ✅ 修复完成 |
| 6 | **AoC** | about-or-contains-paper.tex | **4.12** (v3-AC-v7) | 4/4 | SIGIR workshop | ✅ 修复完成 |
| 7 | **P4** | paper4_trust_but_verify.tex | **4.00** (v3-P4-v4) | 3/4 | NLPCC | ✅ 修复完成 |

**平均分: 4.49**（修复前 3.86 → +0.63）

## 二、附属工件

- **arXiv preprint** (`arxiv-preprint-73pp.tex`, 5.5KB wrapper) — CAC 论文的 73pp 时间戳保护，不是第 8 篇投稿
- **cac-artifact** (github.com/lanbass869-cell/cac-artifact, public) — 14+ commits，全部 8 tex 已同步
- **Supersession Model** (`E:\Temp\supersession_model\`) — DistilBERT fine-tuned
- **Benchmark** (`memtether_supersession_benchmark.jsonl`, 2635 records) — 公开脱敏

## 三、关键数字（唯一正确值）

| 项 | 值 | 禁数 |
|---|---|---|
| Speedup | **11714×** | 禁 11704x / 11729x |
| ConflictBank F1 | **0.897** | 禁 0.903 |
| Method Spec. F1 (500 sample) | 0.889 | - |
| Downstream loss (cross-agent) | **73pp** | - |
| Downstream divergence (expanded) | **86%** (37/43) | - |
| Retrieval filter improvement | **+53.6pp** (43%→96%) | - |
| LongMemEval EAF | **75.7%** | - |
| mem0 baseline | 60.2% | - |
| LoCoMo token-F1 | **0.523** | - |
| mem0 LoCoMo | 0.344 | - |
| Supersession Prediction F1 | **0.9467** | - |
| Supersession best baseline | 0.8043 | - |
| C1 contradictory | **45.5%** | - |
| C2 filter recovery | **+36.4pp** | - |

## 四、18 条禁区

### 继承禁区（15 条）
1. ❌ 编造数据/引用
2. ❌ 隐藏不利结果
3. ❌ 合并 topic 到一篇论文（COMB-1 = 3.25）
4. ❌ <15KB 投稿
5. ❌ >30KB 跑 fuseeval（E3 FAIL）
6. ❌ 声称 novel/first 除非搜过
7. ❌ speedup 写 11704x 或 11729x（正确 = 11714x）
8. ❌ 用 v1 fuseeval 分数
9. ❌ 碰项目线代码/评测/发布
10. ❌ 不跑端到端验证就声称修好
11. ❌ 两阶段 retry 81.2% 写进论文
12. ❌ SGM count_answer_sessions 用于 LongMemEval
13. ❌ 去掉 ECO（60%→45.1%）
14. ❌ 说"零竞品"
15. ❌ P1 不投（PaperJury 8/8 驳回）

### 本轮新增（3 条）
16. ❌ 不许把不同实验（不同 n、不同 entity set）的结果硬合并成 headline number（v7 lifecycle framing = 3.62 血证）
17. ❌ regex 提 \cite 必须含 \citet/\citep（natbib 会漏判 orphan）
18. ❌ 不用 `$c -replace` 整文件替换（曾把 CAC 清零）

## 五、v33 交接核心成果

### 任务 1: Supersession Prediction（新任务+新方法）
- DistilBERT CPU fine-tune, macro F1 = **0.9467**
- 全部 7 baseline ≤ 0.8043
- Model 超最好 baseline **14.2pp**

### 任务 2: 公开 Benchmark
- `memtether_supersession_benchmark.jsonl` = **2635 records** (2.9MB)
- 2635/2635 全部 clean（零敏感 pattern 命中）
- 已推 cac-artifact (commit d624cc2)

### 任务 3: 第三方 Benchmark 对比
- LongMemEval EAF: MemTether **75.7%** vs mem0 60.2% = **+15.5pp**
- LoCoMo token-F1: MemTether **0.523** vs mem0 0.344 = **+17.9pp**
- 超过 Graphiti (0.416) / SimpleMem (0.358) / MemU (0.299)

### CAC 重写（v9 = 方法论文）
- 从"测量报告"重写为"方法论文"（48.5KB）
- 4 贡献：新任务 / 新方法 / 新 benchmark / 第三方 SOTA

## 六、2026-10-17 本轮修复（24 项）

### 第一轮修复（21 项）
- RC abstract LaTeX 错字 ×4（\^N\$ → $r^N$）
- 5 处 undefined refs（WG×2/CAC×1/DYN×1/AoC×1）
- 4 处重复段（WG/AoC/MC/DYN）
- CAC/WG/AoC 26/30/31 days 统一为 30 days
- RC 26→30 days ×8 / 347→349 ×4 / 256 重复段删除
- RC Tamper-Detection results 补齐
- RC 1,699 vs 1,936 加 snapshot 说明
- P4 abstract garbled 重写
- P4 加 \section{Conclusion}
- arXiv preprint 26→30 days

### 第二轮追加修复（3 项）
- AoC Table 1 caption 加 "8 distinct + 2 reruns" 说明
- P4 Reproducibility 加 PyPI + source_audit + MMLU/SWE-bench 说明
- P4 footnote 加 PyPI evalguard==0.1.1

### cac-artifact 推送
- Commit **1bf8c12**（8 files: 7 papers + P4）
- 修复前 HEAD: 4f77070 (v33 handover)

## 七、下一步优先级

### 立即可做
1. **投稿**: WG→MLSys / CAC→KSEM/NLPCC / MC→CCF-B/C / RC→FAccT 2027
2. **arXiv preprint**: 73pp 时间戳保护（需要 arXiv 账号）

### 追求 7 分的新实验
3. **Multi-session 聚合突破**: EAF 60% → LLM-based evidence summarization
4. **Supersession Prediction 扩展**: GPU 跑 DistilBERT-large → F1 > 0.96

### 长期方向
5. Admission control 活体实验 (retrospective → live A/B)
6. Cross-agent contradiction 全量扫描（400K pairs 抽样）
7. 找合作者/外部用户/导师

## 八、关键路径

```
论文 TeX         E:\RUANJIAN\workdocs\memtether\*.tex
P4 TeX           E:\Downloads\paper4_trust_but_verify.tex
fuseeval         E:\RUANJIAN\workdocs\memtether\fuseeval\fuseeval.py
轮次记录         E:\RUANJIAN\workdocs\memtether\fuseeval\rounds\
cac-artifact     E:\RUANJIAN\workdocs\memtether\cac-artifact\
benchmark        cac-artifact\memtether_supersession_benchmark.jsonl
Supersession模型  E:\Temp\supersession_model\
LaTeX编译        tectonic (E:\Temp\tectonic_bin\tectonic.exe)
API              http://127.0.0.1:8813/v1/chat/completions
生产库（只读）   E:\RUANJIAN\memory_hub\memory.db
Git push         HTTPS_PROXY=http://127.0.0.1:7890 + git -c http.sslBackend=openssl
进度日志         E:\Temp\paper_progress.log
本文档           E:\Temp\PAPER_MEMORY_INDEX_20261017.md
```
