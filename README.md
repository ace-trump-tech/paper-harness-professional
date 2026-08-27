# paper-harness-professional

**Languages:** [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md)

> 面向专业科研工作者的多 Agent Auto-Research harness：可以从一个研究题目推进到文献库、创新方案、实验代码、论文初稿和可复现实验记录。它不是无证据的“输入题目直接吐论文”黑盒：每个结论都要绑定来源、运行记录和人工审批。

<p align="center"><img src="demo/stem_pipeline.svg" alt="CV research harness workflow" width="900"></p>

<p align="center"><a href="docs/cv-exploration-zh.md">CV 工作流</a> · <a href="docs/power-grid-literature-only-zh.md">非 CV 电网调研工作流</a> · <a href="demo/self-learn/README.md">电网具身智能 Demo</a> · <a href="docs/harness-architecture-zh.md">Harness 设计</a> · <a href="examples/cv_exploration_project.json">配置示例</a></p>

## 目标

```text
研究题目/代码仓库 -> 文献下载与知识卡 -> A+B+C 方案候选
     -> 论文/代码任务拆解 -> 一卡一子 Agent 实验 -> 指标/SOTA 对比
     -> REFINE / PIVOT -> 图表、论文初稿、实验仓库和对抗审查
     -> 人工确认后发布
```

`ResearchOrchestrator` 是 MainAgent：维护会话状态、任务分派、证据链和恢复。研究者在关键节点选择组合、批准实验、核验公平对比并确认论文 claim。

## 它可以产出什么

给定一个题目和研究约束，Harness 可以组织以下完整链路：

| 输入 | 自动组织的工作 | 产物 |
| --- | --- | --- |
| 研究题目、已有论文、代码仓库 | 文献检索、全文一次性提炼、去重和知识库索引 | 可复用的本地知识库、来源清单和研究笔记 |
| 方法方向或 A+B+C 假设 | 候选组合、反例审查、资源预算和实验矩阵 | 可比较的创新候选与审查记录 |
| 数据集、基线代码、GPU/仿真器 | 生成可执行实验槽，保存配置、种子、数据版本、日志、指标和失败信息 | 可复现实验结果、失败案例和 SOTA 对比 |
| 通过人工审批的证据链 | 组织表格、图表、论文段落、引用绑定和相似度/AI 使用审查 | 论文初稿、图表文件、claim 审计清单 |
| 研究代码需求 | 将实验拆成仓库任务，记录依赖、入口、测试和运行命令 | 可独立运行的研究代码仓库或补丁计划 |

因此它既能“根据题目推进论文”，也能帮助搭建论文配套代码仓库；它不替研究者做未经验证的科学结论或自动发布。

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m paper_harness.cli init examples/cv_exploration_project.json --output ./runs/cv-demo
python -m paper_harness.cli run ./runs/cv-demo/project.json
```

编辑 `gpu_devices`、`innovation_components`、`cv_metrics` 与 `knowledge_files` 后再次初始化。默认只创建 dry-run 实验槽；批准 `experiment` 并配置外部 runtime、代码和数据集后，才允许真正执行训练。

## 多 Agent 架构

| Agent | 输出 | 职责 |
| --- | --- | --- |
| MainAgent | event log + JSON artifacts | 恢复、审批、调度与全局证据链 |
| Literature + Knowledge | `literature_search`, `knowledge_index` | 本地资料索引、长文分块、文献卡与研究笔记 |
| Combination | `innovation_combinations` | 枚举 A、B、C、A+B、A+C、B+C、A+B+C |
| GPU-SubAgent | `gpu_experiment` | 每张 GPU 一个实验槽，记录设备、配置、日志、指标与失败 |
| Evaluation | `cv_evaluation` | 用一致数据切分/协议比较 mAP、mIoU、F1、误差和 SOTA 参考 |
| Composition | `cv_composition`, `draft` | 图表、写作输入、claim 对抗审查与人工复核清单 |

## Harness 保障

参考 AutoResearchClaw 的可验证实验设计，但针对 CV 收敛为轻量内核：

- `cv_contracts.py`：每一阶段有明确输入、输出、完成定义和审批要求。
- `cv_harness.py`：外部训练代码通过统一接口上报指标，拒绝 NaN/Inf，写入受控 `results.json`。
- `hardware.py`：仅探测本机 CUDA 能力用于资源规划，不会自动启动训练。
- `artifact-manifest.json`：为运行中的 artifact 生成 SHA-256 清单，恢复前可发现外部修改。
- `knowledge/`：原始长文本分块落盘，Agent 传递摘要/索引而非反复传输全文，降低 token 与内存压力。

## 权威边界与可审计性

- Harness 可以生成论文初稿和代码任务，但不会把语言模型生成的段落、指标或控制动作当作事实。未配置数据集、代码仓库和 runtime 时不会伪造 CV 指标。
- 每个实验必须保存配置、随机种子、数据来源/版本、运行环境、原始指标、日志、失败信息、artifact SHA-256 和人工审批事件；这些记录可在中断后恢复并审计。
- 专业版中的仿真器、数值求解器和安全门控才是电网/控制结果的权威来源。LLM 或 Agent 只能提出候选、调用工具和解释结果，不能绕过安全校验直接控制设备。
- 论文生成不是自动投稿：最终引用、claim、图表、代码许可证和数据许可必须由人确认。
- PDF 下载、PDF 解析、代码拉取、Docker/Slurm/SSH 执行器都属于可选外部 provider，需在合规前提下明确接入。
- 组合优胜者只是下一轮候选，不能自动视作创新成立；必须做人类审查、消融、基线和统计核验。
- 不自动投稿、不伪造引用、不绕过数据集许可、登录、付费墙或 robots 规则。

## 专业版 Demo：电网具身智能控制

`demo/self-learn/` 是专业版的第一个领域 Demo。它包含 4 篇已校验的开放论文、页标记文本、逐篇知识卡片、研究路线、实验蓝图、SHA-256 校验和可重试下载脚本。另有一份真实的[园区源网荷储经济调度调研报告](demo/self-learn/power-grid-literature-run/report.md)，展示 Harness 如何先做非 CV 文献任务，再决定是否进入仿真和实验。

```bash
cd demo/self-learn
python3 scripts/extract_pdf_text.py
```

原始 PDF、提炼文本和知识卡片均保留在 Demo 内；完整研究说明从 [Demo README](demo/self-learn/README.md) 开始。

## 非 CV 任务怎么处理

遇到“先做文献调研，暂不写代码/仿真”的任务，使用 `power_grid` 领域和 `power_grid_literature_only` 模式。该模式会调用范围、来源、分类和证据审查 Agent，自动跳过 CV 组合、GPU、训练和仿真。示例见 [电网文献调研模式](docs/power-grid-literature-only-zh.md)。

## 与通用版的关系

`paper-harness-undergraduate` 是独立仓库，面向本科毕业论文、教师课题和零基础用户。专业版保留 GPU/runtime、领域知识库和多 Agent 实验迭代；两个子仓库共同构成完整的 paper-harness 产品。
