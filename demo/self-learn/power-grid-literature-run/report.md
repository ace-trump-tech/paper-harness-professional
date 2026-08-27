# 园区源网荷储经济优化调度：第一轮文献调研报告

检索日期：2026-08-27  
任务边界：只做文献调研和方法梳理，不执行代码、仿真或算法实验。  
证据规则：下表 DOI、题名、作者和期刊元数据来自 Crossref；本地具身智能论文来自 `../knowledge/cards/`。没有全文核验的内容标记为“待全文编码”，不据此宣称方法优越性。

## 1. 结论先行

园区源网荷储经济调度的本质，是在给定预测、设备状态、价格和网络边界下，决定每个时间步的能源交换和设备出力，使运行成本、碳排、峰谷差、弃新能源和储能寿命损耗等目标达到可接受的折中，同时满足功率平衡、SOC、设备容量以及可能的潮流/电压/线路安全约束。

最稳妥的技术路线不是“某个智能算法一定最好”，而是：

1. 日前用 LP/MILP 或随机/鲁棒 MILP 形成可解释基线；
2. 日内用滚动 MPC 修正预测误差；
3. 多目标场景报告 Pareto 前沿或敏感性分析，而不是只报一个加权分数；
4. DRL 适合高频、模型不完备或连续控制，但必须和 MPC/OPF、安全过滤器做同场景比较；
5. LLM 目前更适合作为检索、规划和工具编排层，不能替代潮流、优化器和安全校验器。

## 2. 问题定义：到底在“调什么”

| 层次 | 典型内容 |
| --- | --- |
| 源 | 光伏、风电、燃气轮机/柴油机、CHP；决定可用功率、弃电和可控出力 |
| 网 | 园区配电网、联络线、主网购售电；决定功率交换、潮流、网损和电压边界 |
| 荷 | 刚性负荷、可移峰负荷、可中断负荷、EV、冷热负荷；决定需求响应和舒适度代价 |
| 储 | 电池/其他储能；通过充放电把时间上的能量搬移，状态由 SOC 表示 |

经济调度不是单独的“控制器名称”，而是一个带时间索引的优化问题。常见链路是：

```text
预测/价格/设备参数/初始SOC
  -> 决策：购售电、源出力、储能充放电、负荷响应、弃电
  -> 目标：成本、碳、峰谷差、消纳、寿命等
  -> 约束：平衡、SOC、容量、启停、潮流、电压、线路热限
  -> 输出：各时段计划、SOC轨迹、购售电曲线、弃电和约束裕度
```

普通能量管理更强调“协调设备并满足供需”；经济调度进一步把电价、燃料、碳和寿命显式放入目标。电压控制/潮流控制则关注电气状态和网络安全，通常需要无功、节点电压、线路容量或 AC/DC 潮流模型。三者可以在同一个分层 EMS 中协同，但不能把“成本最低”直接等同于“电网安全”。

时间尺度通常分为：日前（小时级、基于预测制定计划）、日内/滚动（15 分钟到小时级、根据新预测修正）和实时（秒到分钟级、跟踪偏差和安全约束）。

## 3. 数学模型骨架

一个常见离散模型可抽象为：

```text
状态 x_t      = [SOC_t, 机组开停状态, 温度/库存, 网络状态]
外生输入 w_t  = [PV/风/负荷预测, 电价, 碳因子, 故障/不确定性]
决策 u_t      = [P_buy, P_sell, P_ch, P_dis, P_gen, P_DR, P_curtail]
目标          = Σ_t(购电费 + 燃料费 + 启停费 + 碳成本 + 电池退化费 + 惩罚)
约束          = 平衡 + SOC递推 + 功率/爬坡/启停 + 需求响应 + 潮流/电压/线路
```

储能状态通常写成 `SOC(t+1)=SOC(t)+η_ch P_ch Δt/E - P_dis Δt/(η_dis E)`，并加上 SOC 上下限、充放电功率上限和终端 SOC。为避免同时充放电，论文会使用二进制互斥变量、互补约束、价格结构假设或事后修正；其中只有显式互斥约束能直接表达设备逻辑。

纯经济能量调度只保留功率平衡、容量、SOC、电价和成本；网络安全调度还要加入节点功率方程、潮流、节点电压、线路热限和网损。因此前者的解不能直接声称可在配电网执行。

## 4. 方法分类与比较

| 方法类别 | 代表算法 | 精确模型 | 训练 | 最优性 | 速度/可解释性 | 适合场景与主要风险 |
| --- | --- | --- | --- | --- | --- | --- |
| 数学规划 | LP/QP/MILP/MINLP | 需要，程度不同 | 否 | LP/QP/MILP 在建模和求解终止条件下有最优性界；MINLP 常为局部/启发式 | 小中型问题快且最可解释；整数和非线性会变慢 | 日前计划、启停、储能逻辑；对预测和模型误差敏感 |
| MPC | 线性/非线性/混合整数 MPC | 需要预测模型 | 否 | 每个滚动窗口求解局部最优 | 能持续纠偏；实时计算和模型失配是风险 | 日内、实时调度；需报告求解延迟和失稳处理 |
| 鲁棒/随机 | RO、两阶段随机、机会约束、分布鲁棒 | 需要不确定性集合或概率 | 否 | 对给定集合提供鲁棒/概率意义的保证 | 场景数和保守性增加计算量 | PV/负荷/价格不确定性；分布假设错误会失效 |
| 智能优化 | PSO、GA、DE、SA、ACO、WOA 等 | 可弱化或黑箱化 | 否 | 通常无全局最优证明 | 易编码、可处理非光滑目标；结果依赖随机种子、参数和约束修复 | 复杂非凸模型或论文原型；容易出现不可行解和不公平比较 |
| 多目标 | 加权和、ε-约束、NSGA-II、MOPSO | 视底层模型而定 | 否 | 输出 Pareto 近似或单一折中解 | 能展示经济/低碳/舒适度权衡；权重和尺度影响结论 | 需要明确偏好、归一化和 Pareto 选择规则 |
| 强化学习 | Q-learning、DQN、DDPG、TD3、SAC、PPO | 可不显式建模，但依赖环境 | 是 | 不保证全局最优或安全 | 推理快、适合连续控制；训练样本、分布外状态和安全是主要风险 | 高频实时 EMS、不确定性和模型难写场景；必须有安全层和基线 |
| LLM/Agent | 检索、规划、工具调用、LLM+优化器 | 数值决策仍应交给求解器/仿真器 | 视模型而定 | 无数值最优性或安全保证 | 降低人机交互门槛；文本幻觉和不可重复性必须审计 | 文献整理、场景编排、解释和候选方案生成；不能直接下发控制量 |

PSO/GA 与 MILP 的本质区别是：MILP 把目标和约束写入可求解的数学结构，求解器可以给出可行性和最优性界；PSO/GA 只需要一个可评价的目标函数，靠群体搜索逼近解，约束通常要靠罚函数或修复算子处理。因此“改进 PSO 比 MILP 好”只有在相同数据、约束、停止时间、种子和可行率下比较才成立。中文论文大量使用 PSO/改进 PSO，常见原因是实现门槛低、可处理非线性和多目标、容易与设备模型拼接；这不等价于它在工程上优于 MILP。

## 5. 储能与碳排放

储能通过低价充电、高价放电实现削峰填谷和峰谷套利，也能吸收光伏剩余电量、降低弃光。SOC 是状态变量，因为当前充放电会改变未来可用能量；忽略 SOC 会得到不可执行的“免费能量”。充放电效率降低套利收益，频繁循环还带来退化成本，因此近期模型越来越多地加入吞吐量、等效循环或寿命成本。

最低运行成本和最低碳排不一定相同：电价低的时段可能对应高碳电源，高价时段也可能有较高可再生出力；储能的充电时机还会改变碳因子。常见处理是把购电量乘以时变排放因子、给碳排加价格，或用成本-碳排双目标/Pareto 方法。报告时必须同时给出成本、碳排和权重/碳价，不能只报“综合目标”。

## 6. 代表性论文（已核验 DOI 元数据）

以下 15 篇覆盖模型规划、MPC、随机/鲁棒、多目标、储能寿命和 RL。它们是第一轮核心样本，不是按引用量排序；每篇仍需下载全文后补齐系统组成、时间步长、约束和实验基线。

| 论文 | 年 | 作者 | 期刊 | 方法/覆盖点 | DOI |
| --- | ---: | --- | --- | --- | --- |
| An Energy Management System for the Control of Battery Storage in a Grid-Connected Microgrid Using Mixed Integer Linear Programming | 2021 | Sigalo, Pillai, Das, Abusara | Energies | MILP、并网电池调度 | [10.3390/en14196212](https://doi.org/10.3390/en14196212) |
| Battery aging in multi-energy microgrid design using mixed integer linear programming | 2018 | Cardoso et al. | Applied Energy | MILP、储能退化 | [10.1016/j.apenergy.2018.09.185](https://doi.org/10.1016/j.apenergy.2018.09.185) |
| Optimal design and operation of a multi-energy microgrid using mixed-integer nonlinear programming: Impact of carbon cap and trade system and taxing on equipment selections | 2023 | Akulker, Aydin | Applied Energy | MINLP、碳约束/碳交易 | [10.1016/j.apenergy.2022.120313](https://doi.org/10.1016/j.apenergy.2022.120313) |
| Predictive active-reactive optimal power dispatch in PV-battery-diesel microgrid considering reactive power and battery lifetime costs | 2019 | Alramlawi, Mohagheghi, Li | Solar Energy | 有功/无功、储能寿命 | [10.1016/j.solener.2019.09.034](https://doi.org/10.1016/j.solener.2019.09.034) |
| Nonlinear Economic Model Predictive Control for Microgrid Dispatch | 2016 | Zachar, Daoutidis | IFAC-PapersOnLine | 非线性经济 MPC | [10.1016/j.ifacol.2016.10.260](https://doi.org/10.1016/j.ifacol.2016.10.260) |
| Intra-Hour Microgrid Economic Dispatch Based on Model Predictive Control | 2020 | Velasquez et al. | IEEE Transactions on Smart Grid | 日内 MPC | [10.1109/tsg.2019.2945692](https://doi.org/10.1109/tsg.2019.2945692) |
| Distributed EMPC of multiple microgrids for coordinated stochastic energy management | 2017 | Kou, Liang, Gao | Applied Energy | 分布式随机 EMPC | [10.1016/j.apenergy.2016.09.092](https://doi.org/10.1016/j.apenergy.2016.09.092) |
| Adaptively Constrained Stochastic Model Predictive Control for the Optimal Dispatch of Microgrid | 2018 | Guo, Bao, Li, Yan | Energies | 随机 MPC、约束自适应 | [10.3390/en11010243](https://doi.org/10.3390/en11010243) |
| Stochastic Optimization of Economic Dispatch for Microgrid Based on Approximate Dynamic Programming | 2019 | Shuai et al. | IEEE Transactions on Smart Grid | 随机优化、近似动态规划 | [10.1109/tsg.2018.2798039](https://doi.org/10.1109/tsg.2018.2798039) |
| An optimal stochastic energy management system for resilient microgrids | 2021 | Silva et al. | Applied Energy | 三相、随机 MINLP、韧性 | [10.1016/j.apenergy.2021.117435](https://doi.org/10.1016/j.apenergy.2021.117435) |
| An integrated framework of agent-based modelling and robust optimization for microgrid energy management | 2014 | Kuznetsova et al. | Applied Energy | ABM、鲁棒优化 | [10.1016/j.apenergy.2014.04.024](https://doi.org/10.1016/j.apenergy.2014.04.024) |
| Real-time optimal energy management of microgrid with uncertainties based on deep reinforcement learning | 2022 | Guo et al. | Energy | DRL、不确定性、实时 EMS | [10.1016/j.energy.2021.121873](https://doi.org/10.1016/j.energy.2021.121873) |
| Deep reinforcement learning for energy management in a microgrid with flexible demand | 2021 | Nakabi, Toivanen | Sustainable Energy, Grids and Networks | DRL、柔性负荷 | [10.1016/j.segan.2020.100413](https://doi.org/10.1016/j.segan.2020.100413) |
| Multi-agent deep reinforcement learning based distributed control architecture for interconnected multi-energy microgrid energy management and optimization | 2023 | Zhang et al. | Energy Conversion and Management | 多 Agent DRL、互联多能源微网 | [10.1016/j.enconman.2022.116647](https://doi.org/10.1016/j.enconman.2022.116647) |
| Secure energy management of multi-energy microgrid: A physical-informed safe reinforcement learning approach | 2023 | Wang et al. | Applied Energy | 物理约束、安全 RL | [10.1016/j.apenergy.2023.120759](https://doi.org/10.1016/j.apenergy.2023.120759) |

补充综述：[Microgrid Management Strategies for Economic Dispatch of Electricity Using Model Predictive Control Techniques: A Review](https://doi.org/10.3390/en16165935)（Energies, 2023）适合用来扩展 MPC 样本，但不能替代逐篇全文编码。

## 7. LLM 与电力调度的现状判断

本轮没有找到足以支持“LLM 已经可以独立完成园区经济调度”的证据。现有方向更接近：技术文档/标准检索、OPF 或 EMS 工具调用、自然语言场景编排、结果解释和 Agent 协调。`self-learn/knowledge/cards/foundation-models-power-systems-2023.md` 与 `x-gridagent-2025.md` 已将这一边界记录为：LLM 负责接口和规划，数值求解器、潮流模型和安全过滤器负责决定动作。

因此当前可提出的研究问题是“LLM 如何可靠地编排预测、优化、潮流和安全校验工具”，而不是“让 LLM 直接输出可执行功率序列”。任何 LLM 调度结果都应绑定输入状态、工具版本、求解器结果、约束检查和人工确认记录。

## 8. 研究空白与下一步

优先级较高的方向包括：

- 预测误差、价格不确定性和极端天气下的分布鲁棒/机会约束调度；
- 多时间尺度调度：日前 MILP、日内 MPC、实时安全控制之间的接口；
- 储能退化、碳排和用户舒适度的可解释多目标权衡；
- 经济调度与配电网电压/潮流安全的统一模型；
- 在同一数据、同一约束、同一时间预算下比较 MILP、MPC、PSO、DRL；
- LLM/Agent 的工具编排、拒答和安全过滤，而非自由文本控制；
- 从仿真到硬件在环的验证，并报告约束违例率、恢复时间、拒绝率和延迟，而不只报告平均成本。

下一步应对表中 15 篇论文逐篇下载全文，按“系统组成—时间尺度—输入—状态—决策—目标—约束—求解器—基线—数据—指标—代码/许可证”字段补齐结构化知识卡，再决定是否开展仿真。当前报告已经足够回答问题定义和方法地图，但还不能作为最终论文的系统性综述或“主流方法统计”依据。
