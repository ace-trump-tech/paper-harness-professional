# 电网文献调研模式

这是一种专业版的非 CV 扩展模式，适用于“先调研，暂不实现”的任务，例如园区源网荷储经济优化调度。

## 启动

```bash
python -m paper_harness.cli init examples/power_grid_literature_project.json --output ./runs/power-grid-literature
python -m paper_harness.cli run ./runs/power-grid-literature/project.json
```

第一次运行会在文献阶段暂停。确认检索范围后：

```bash
python -m paper_harness.cli approve ./runs/power-grid-literature/project.json --stage adversarial_review
python -m paper_harness.cli approve ./runs/power-grid-literature/project.json --stage evidence_review
python -m paper_harness.cli approve ./runs/power-grid-literature/project.json --stage draft
python -m paper_harness.cli approve ./runs/power-grid-literature/project.json --stage final_review
python -m paper_harness.cli run ./runs/power-grid-literature/project.json
```

## Agent 行为

| Agent | 作用 |
| --- | --- |
| `power-grid-scope` | 将自然语言提示词拆成定义、建模、目标、约束、方法和 LLM 检索块 |
| `literature-scout` | 通过配置来源或 OpenAlex 获取去重后的文献记录；在线失败会记录错误而不崩溃 |
| `power-grid-source-manager` | 记录 DOI/URL、开放获取状态、代码仓库、许可证和一次性全文抽取要求 |
| `power-grid-taxonomy` | 输出源网荷储对象、输入、决策变量、目标函数、约束和算法类别矩阵 |
| `power-grid-evidence-critic` | 阻止从搜索排名推断“最常见”、从单篇论文推断“最优”或从惩罚项推断“硬安全” |
| `power-grid-synthesis` | 只生成带证据要求的综述提纲，不伪造实验结论 |

该模式会生成 `research_boundary` 工件，明确 `experiments`、`simulation` 和 `code_execution` 均为 `not_applicable`。因此不会调用 `GPUSubAgent`、训练脚本或仿真器。

## 扩展到其他非 CV 领域

新增领域时复制 `paper_harness/domain_packs/power_grid.py` 的结构，并提供：

1. 领域边界与检索词；
2. 该领域的对象/输入/变量/目标/约束分类；
3. 证据审查规则；
4. `literature_only` 和 `full` 两种明确模式。

不要把领域 Agent 直接塞进 CV 工作流。编排器通过 `domain` 与 `research_mode` 路由，保持 GPU/runtime 依赖与纯文献任务隔离。
