# CV Harness 架构

本仓库借鉴 AutoResearchClaw 的 harness 设计，但只保留 CV 实验所需的最小可信执行面，而不是复制其面向多学科的完整系统。

## 保留的四个机制

1. **Stage contract**：`cv_contracts.py` 规定知识库、组合、实验、评估和写作阶段分别读取什么、输出什么、何时完成、是否需要人类批准。
2. **受控指标出口**：`CVExperimentHarness` 是实验代码上报指标的唯一接口，拒绝 NaN/Inf，并写入统一的 `results.json`。
3. **完整性清单**：每次 Agent 落盘 artifact 后，`artifact-manifest.json` 更新 SHA-256；恢复前可以调用 `verify_artifact_manifest` 检查外部修改。
4. **硬件感知计划**：`hardware.py` 只探测 `nvidia-smi`，为 GPU 子 Agent 提供设备画像；不会据此自动执行训练。

## 为什么不直接复制完整框架

CV 研究需要的是可对比的基线、消融、数据切分和 GPU 调度。过早加入跨学科 executor、自动代码修复或“全自动论文”会掩盖实验协议缺失的问题。这里把每项外部能力留在 provider/runtime 边界：研究者明确配置仓库、数据、容器/Slurm/SSH 和资源预算后，才允许执行。

## 外部训练接入要求

每个真实 run 必须至少保留：组合 ID、Git commit、数据集版本/切分、命令、设备、随机种子、时间预算、stdout/stderr、统一 `results.json`、失败原因和 artifact manifest。缺少这些信息的数字不能进入 `cv_evaluation` 或论文 claim。
