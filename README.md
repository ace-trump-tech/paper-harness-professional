# Paper Harness Professional

**Languages:** [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md)

> **从研究想法到可复现论文：一个可审计的多 Agent 研究流水线**  
> 它不替你做科学结论，但替你管好证据、实验、代码和论文，让你在每个关键节点都能掌控全局。

---

## 核心原理：多 Agent 协作，证据驱动

Paper Harness Professional 不是“输入题目 → 吐论文”的黑盒。它是一个**可中断、可恢复、可审计**的研究编排框架，由多个专业 Agent 分工协作，将你的研究想法逐步推进为：

- 本地知识库与文献卡片
- 可比较的创新方案候选
- 可执行的实验槽（GPU/仿真器）
- 带证据链的论文初稿、图表和可复现实验仓库

它的运作遵循一条清晰的主线：

```
研究题目/代码仓库 → 文献下载与知识卡 → A+B+C 方案候选
     → 论文/代码任务拆解 → 一卡一子 Agent 实验 → 指标/SOTA 对比
     → REFINE / PIVOT → 图表、论文初稿、实验仓库和对抗审查
     → 人工确认后发布
```

**核心设计原则：**

- **每个结论都绑定来源**（文献、数据、运行日志、人工审批）
- **每一阶段都有明确合约**（输入、输出、完成定义、审批要求）
- **所有实验可复现**（保存配置、随机种子、数据版本、指标、失败信息、SHA-256 清单）
- **人工始终在环**（组合选择、实验批准、公平对比核验、论文 claim 确认）

---

## 🚀 快速体验：电网具身智能控制 Demo

我们提供了一个完整的领域 Demo，展示 Harness 如何从 4 篇开放论文出发，自动生成知识卡片、研究路线、实验蓝图和一份真实的研究报告。

```bash
cd demo/self-learn
python3 scripts/extract_pdf_text.py
```

Demo 包含：
- 原始 PDF 与页标记文本
- 逐篇知识卡片（方法、贡献、局限性）
- 研究路线图与实验蓝图
- SHA-256 校验和可重试下载脚本
- 一份完整的[园区源网荷储经济调度调研报告](demo/self-learn/power-grid-literature-run/report.md)

你可以在 10 分钟内跑通这个流程，亲眼见证 Harness 如何将零散文献组织成结构化的研究起点。  
👉 详细说明从 [Demo README](demo/self-learn/README.md) 开始。

---

## 🔧 非 CV 任务？照样高效支持

如果你当前只需要做**文献调研**，不涉及代码/仿真，使用 `power_grid` 领域和 `power_grid_literature_only` 模式即可。该模式会自动调用范围、来源、分类和证据审查 Agent，跳过 CV 组合、GPU 训练和仿真，专注于：

- 文献检索与去重
- 全文分块提炼与知识索引
- 研究笔记与综述草稿

以电网领域为例，Harness 已经成功生成过一份真实的调研报告，展示如何先完成文献任务，再决定是否进入仿真和实验。  
👉 参阅 [电网文献调研模式](docs/power-grid-literature-only-zh.md)。

---

## 🌟 这个 Harness 从哪里来？—— MindPaw 的成功实践

Paper Harness Professional 的架构和设计，**直接提取自一个已在 GitHub 上获得广泛验证的开源项目**：

> **[MindPaw](https://github.com/ace-trump-tech/MindPaw)** —— 一个面向具身智能控制的研究自动化框架  
> ⭐ **2.4k Stars** | 🍴 **2.2k Forks**

MindPaw 证明了多 Agent 协作、证据链审计和人工审批在研究中的实际价值。我们将其中成熟、通用的部分抽象为 **Paper Harness Professional**，让你能够将其应用于自己的研究课题，无论是 CV、电网控制，还是其他领域。

> 你不再需要从零搭建这套复杂的基础设施，直接站在巨人的肩膀上。

---

## 🧠 多 Agent 架构一览

| Agent | 输出 | 职责 |
| --- | --- | --- |
| **MainAgent** | event log + JSON artifacts | 恢复、审批、调度与全局证据链 |
| **Literature + Knowledge** | `literature_search`, `knowledge_index` | 本地资料索引、长文分块、文献卡与研究笔记 |
| **Combination** | `innovation_combinations` | 枚举 A、B、C、A+B、A+C、B+C、A+B+C |
| **GPU-SubAgent** | `gpu_experiment` | 每张 GPU 一个实验槽，记录设备、配置、日志、指标与失败 |
| **Evaluation** | `cv_evaluation` | 用一致数据切分/协议比较 mAP、mIoU、F1、误差和 SOTA 参考 |
| **Composition** | `cv_composition`, `draft` | 图表、写作输入、claim 对抗审查与人工复核清单 |

每个 Agent 的输出都经过合约检查，确保可追溯、可复现。

---

## 🛡️ 保障与可审计性

- **不伪造指标**：未配置数据集、代码仓库和 runtime 时，不会凭空生成实验数据。
- **每个实验都固化**：配置、种子、数据版本、日志、指标、失败信息、SHA-256 清单和人工审批事件全部保存。
- **外部工具可插拔**：PDF 下载、代码拉取、Docker/Slurm/SSH 执行器按需接入，但必须在合规前提下明确配置。
- **论文生成不是自动投稿**：最终引用、claim、图表、许可证必须由人确认。
- **组合候选不自动视为成立**：必须经过人类审查、消融、基线和统计核验。

---

## ⚡ 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m paper_harness.cli init examples/cv_exploration_project.json --output ./runs/cv-demo
python -m paper_harness.cli run ./runs/cv-demo/project.json
```

编辑 `gpu_devices`、`innovation_components`、`cv_metrics` 与 `knowledge_files` 后再次初始化。默认只创建 dry-run 实验槽；批准 `experiment` 并配置外部 runtime、代码和数据集后，才允许真正执行训练。

---

## 📂 它可以产出什么

| 输入 | 自动组织的工作 | 产物 |
| --- | --- | --- |
| 研究题目、已有论文、代码仓库 | 文献检索、全文提炼、去重和知识库索引 | 可复用的本地知识库、来源清单和研究笔记 |
| 方法方向或 A+B+C 假设 | 候选组合、反例审查、资源预算和实验矩阵 | 可比较的创新候选与审查记录 |
| 数据集、基线代码、GPU/仿真器 | 生成可执行实验槽，保存全部上下文 | 可复现实验结果、失败案例和 SOTA 对比 |
| 通过人工审批的证据链 | 组织表格、图表、论文段落、引用绑定 | 论文初稿、图表文件、claim 审计清单 |
| 研究代码需求 | 拆解为仓库任务，记录依赖、入口、测试和运行命令 | 可独立运行的研究代码仓库或补丁计划 |

---

## 🔗 更多文档

- [CV 工作流](docs/cv-exploration-zh.md)
- [电网文献调研模式](docs/power-grid-literature-only-zh.md)
- [Harness 设计文档](docs/harness-architecture-zh.md)
- [配置示例](examples/cv_exploration_project.json)

---

## 📌 权威边界与合规声明

- 仿真器、数值求解器和安全门控是专业版中电网/控制结果的**唯一权威来源**。LLM 只能提出候选、调用工具和解释结果，不能绕过安全校验。
- 不自动投稿、不伪造引用、不绕过数据集许可、登录、付费墙或 robots 规则。
- 所有外部 provider（PDF 下载、代码拉取、执行器）需在合规前提下明确接入。

---

**Paper Harness Professional** —— 让你的研究可复现、可审计、可迭代。  
从今天开始，用它组织你的下一个项目。
