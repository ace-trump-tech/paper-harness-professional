<div align="center">

# Paper Harness Professional

**从研究想法到可复现论文：一个可审计的多 Agent 研究流水线**

[简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md)

</div>

---

## 📖 它到底是什么？

它不是“输入题目 → 直接吐论文”的魔术黑盒。  
它是**面向专业科研工作者的研究编排框架**——你可以把它理解为一个“研究操作系统”：

- **多 Agent 分工协作**：文献、组合、实验、写作各司其职；
- **证据驱动**：每一个结论、每一组数据、每一段文字都绑定来源（文献页码、运行日志、人工审批）；
- **可中断 / 可恢复**：即使实验跑了一周，断电后也能从断点继续；
- **人工始终在环**：候选方案、实验批准、公平对比、论文 Claim，全部需要你点头。

它的核心工作流只有一条主线：

> **研究题目 / 代码仓库** → 文献下载与知识卡片 → A+B+C 候选方案 → 任务拆解 → 每张 GPU 一个子 Agent 实验 → 指标 / SOTA 对比 → REFINE / PIVOT → 图表、论文初稿、实验仓库 → **你确认后发布**

---

## ⚙️ 核心原理：合同驱动，不留模糊地带

Harness 的每一阶段都通过 `cv_contracts.py` 明确定义了：

- 输入（必须有什么）
- 输出（必须产出什么）
- 完成定义（什么算“做完”）
- 审批要求（需要你确认什么）

所有运行产物都会生成 **SHA-256 清单**（`artifact-manifest.json`），外部任何人修改了文件，恢复时立刻能发现。  
实验记录强制保存：配置、随机种子、数据版本、原始日志、指标、失败信息——**可复现不是口号，是默认行为**。

---

## 🚀 先跑一个 Demo：电网具身智能控制（10 分钟上手）

光说不练假把式。我们提供了一个**完整的电网控制领域 Demo**，包含 4 篇已校验的开放论文、逐页文本、知识卡片、研究路线和实验蓝图。

```bash
cd demo/self-learn
python3 scripts/extract_pdf_text.py
```

跑完后你会得到：

- 原始 PDF + 页标记文本
- 每篇论文的知识卡片（方法 / 贡献 / 局限）
- 研究路线与可执行的实验槽
- 一份真实的 **园区源网荷储经济调度调研报告**（[demo/self-learn/power-grid-literature-run/report.md](demo/self-learn/power-grid-literature-run/report.md)）

> 这个 Demo 不是为了炫技，而是让你亲眼看到：**Harness 如何把 4 篇散落的论文，自动组织成一份结构清晰的研究起点**。  
> 详细说明请移步 [Demo README](demo/self-learn/README.md)。

---

## 🔌 非 CV 任务怎么办？以电网文献调研为例

很多研究课题**根本不需要写代码或跑仿真**，前期只需要扎实的文献调研。Harness 同样覆盖这个场景。

使用 `power_grid` 领域 + `power_grid_literature_only` 模式，系统会自动：

- 调用范围审查 Agent（界定调研边界）
- 调用来源审查 Agent（筛选高价值文献）
- 调用分类与证据审查 Agent（提炼核心观点并交叉验证）
- **完全跳过** CV 组合、GPU 分配和训练执行

最终输出的是研究笔记、分类综述和证据清单，而不是实验代码。  
这个模式已经在真实电网项目中验证过，产出了一份完整的调研报告。  
👉 参阅 [电网文献调研模式](docs/power-grid-literature-only-zh.md)。

---

## 🌟 这个 Harness 从哪来？——MindPaw 的实战验证

> **这不是一个象牙塔里的玩具，而是一套从成功开源项目中提取的成熟基础设施。**

Paper Harness Professional 的架构设计，直接脱胎于：

<div align="center">
  <a href="https://github.com/ace-trump-tech/MindPaw">
    <strong>MindPaw</strong>
  </a>
  — 面向具身智能控制的研究自动化框架  
  ⭐ <strong>2.4k Stars</strong> · 🍴 <strong>2.2k Forks</strong>
</div>

MindPaw 已经在真实研究场景中跑通了“文献 → 方案 → 实验 → 论文”的全链路，证明了多 Agent 协作、证据审计和人工审批的实战价值。我们将其中**通用、可复用**的核心能力抽象出来，形成了 Paper Harness Professional。

**这意味着**：你不需要从零搭建这套复杂的研究基础设施，直接站在 2.4k 开发者和研究者的肩膀上开始自己的课题。

---

## 🧠 多 Agent 架构速览

| Agent | 核心产出 | 职责 |
| :--- | :--- | :--- |
| **MainAgent** | event log + 全局状态 | 恢复、审批、调度、维护证据链 |
| **Literature + Knowledge** | 文献索引 + 知识卡片 | 本地资料索引、长文分块、研究笔记 |
| **Combination** | 创新组合候选 | 枚举 A/B/C/A+B/A+C/B+C/A+B+C |
| **GPU-SubAgent** | 每卡实验槽 | 记录设备、配置、日志、指标、失败信息 |
| **Evaluation** | 公平对比结果 | 统一协议下对比 mAP/mIoU/F1 与 SOTA |
| **Composition** | 图表 + 论文初稿 | 写作输入、Claim 对抗审查、复核清单 |

---

## 📦 它能为你产出什么？

| 你的输入 | Harness 自动组织 | 最终产物 |
| :--- | :--- | :--- |
| 研究题目 + 论文 + 代码仓 | 文献检索、全文提炼、去重、索引 | 本地知识库 + 来源清单 + 研究笔记 |
| A+B+C 假设方向 | 候选组合枚举、反例审查、资源预算 | 可比较的创新候选 + 审查记录 |
| 数据集 + 基线代码 + GPU/仿真器 | 生成可执行实验槽，固化全部上下文 | 可复现实验结果 + SOTA 对比 + 失败案例 |
| 通过审批的证据链 | 组织表格、图表、段落、引用绑定 | 论文初稿 + 图表文件 + Claim 审计清单 |
| 代码需求描述 | 拆解仓库任务，记录依赖 / 入口 / 测试 | 可独立运行的研究代码仓库或补丁计划 |

---

## 🛡️ 专业保障与审计边界

- **不伪造指标**：未配置数据集、代码仓和 runtime 时，系统不会凭空生成任何实验数据。
- **所有外部执行器可选**：PDF 下载、代码拉取、Docker/Slurm/SSH 均需你在合规前提下明确接入。
- **权威来源不可绕过**：电网/控制类结果只认仿真器、数值求解器和安全门控的输出；LLM 只能解释结果，不能直接控制设备。
- **论文不自动投稿**：最终引用、图表、许可证、Claim 必须经你人工确认。
- **组合候选不自动成立**：必须做消融、基线对比和统计核验，通过后才会进入下一轮。

---

## ⚡ 一分钟快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m paper_harness.cli init examples/cv_exploration_project.json --output ./runs/cv-demo
python -m paper_harness.cli run ./runs/cv-demo/project.json
```

> 默认只创建 **dry-run 实验槽**，不会真的跑训练。只有在你批准 `experiment` 并配置好外部 runtime、代码和数据集后，才允许执行实际计算。

---

## 📂 更多文档

- [CV 工作流详解](docs/cv-exploration-zh.md)  
- [电网文献调研模式](docs/power-grid-literature-only-zh.md)  
- [Harness 架构设计](docs/harness-architecture-zh.md)  
- [完整配置示例](examples/cv_exploration_project.json)

---

<div align="center">

**Paper Harness Professional** —— 让你的每个研究脚印，都清晰可溯。  
从今天起，用它来组织你的下一个项目。

</div>
