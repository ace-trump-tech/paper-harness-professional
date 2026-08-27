# paper-harness-professional

**Languages:** [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md)

> 面向专业科研工作者的多 Agent Auto-Research harness。当前重点支持 CV 与电网具身智能控制，不是“输入题目直接吐论文”，而是让文献、创新组合、仿真实验、指标评估和写作审查共享同一条可追溯证据链。

<p align="center"><img src="demo/stem_pipeline.svg" alt="CV research harness workflow" width="900"></p>

<p align="center"><a href="docs/cv-exploration-zh.md">CV 工作流</a> · <a href="demo/self-learn/README.md">电网具身智能 Demo</a> · <a href="docs/harness-architecture-zh.md">Harness 设计</a> · <a href="examples/cv_exploration_project.json">配置示例</a></p>

## 目标

```text
本地文献/PDF -> 结构化知识库 -> A+B+C 组合候选
     -> 一卡一子 Agent 实验 -> 指标/SOTA 对比 -> REFINE / PIVOT
     -> 证据绑定的图表、草稿和对抗审查 -> 人工最终决策
```

`ResearchOrchestrator` 是 MainAgent：维护会话状态、任务分派、证据链和恢复。研究者在关键节点选择组合、批准实验、核验公平对比并确认论文 claim。

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

## 诚实边界

- 本仓库当前实现的是受控编排与可审计实验接口，未配置数据集、代码仓库和 runtime 时不会伪造 CV 指标。
- PDF 下载、PDF 解析、代码拉取、Docker/Slurm/SSH 执行器都属于可选外部 provider，需在合规前提下明确接入。
- 组合优胜者只是下一轮候选，不能自动视作创新成立；必须做人类审查、消融、基线和统计核验。
- 不自动投稿、不伪造引用、不绕过数据集许可、登录、付费墙或 robots 规则。

## 专业版 Demo：电网具身智能控制

`demo/self-learn/` 是专业版的第一个领域 Demo。它包含 4 篇已校验的开放论文、页标记文本、逐篇知识卡片、研究路线、实验蓝图、SHA-256 校验和可重试下载脚本。重点不是让 LLM 直接控制电网，而是把 Grid2Op/PowerGym/Gym-ANM/CommonPower 等仿真器、控制策略和安全门控组织成可审计闭环。

```bash
cd demo/self-learn
python3 scripts/extract_pdf_text.py
```

原始 PDF、提炼文本和知识卡片均保留在 Demo 内；完整研究说明从 [Demo README](demo/self-learn/README.md) 开始。

## 与通用版的关系

`paper-harness-undergraduate` 是独立仓库，面向本科毕业论文、教师课题和零基础用户。专业版保留 GPU/runtime、领域知识库和多 Agent 实验迭代；两个子仓库共同构成完整的 paper-harness 产品。
