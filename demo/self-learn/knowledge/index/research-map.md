# Research Map: Embodied Intelligence for Power-Grid Control

## A precise research object

The candidate system is a **tool-grounded, safety-gated control loop**. It must be evaluated in a power-system simulator or hardware-in-the-loop setup:

```text
SCADA/PMU/forecast observations
  -> state estimator and uncertainty monitor
  -> planner (RL/MPC/LLM-assisted policy)
  -> typed control proposal
  -> safety shield + power-flow/contingency validator
  -> actuator interface or simulator step
  -> measurements, counterfactual checks and immutable run record
```

The planner may be learned or agentic. The safety validator, numerical solver and action authority are separate components. This distinction is the central boundary between research assistance and unsafe autonomous dispatch.

## Four research layers

| Layer | Research question | Primary assets |
| --- | --- | --- |
| Embodiment | What does the agent see, change and observe after a change? | Grid2Op, PowerGym, Gym-ANM |
| Coordination | How are devices, zones and operators coordinated under partial information? | PowerGridworld, PowerNet-style MARL |
| Safety | Which constraints are enforced and by what mechanism? | CommonPower, safe-RL reviews, MPC baseline |
| Agentic interface | How can natural language help without becoming the numerical authority? | Foundation Models for Power Systems, X-GridAgent |

## Recommended research sequence

1. **Choose one environment and one action class.** Begin with Volt-Var control in PowerGym/Gym-ANM or topology control in Grid2Op. Do not combine them before baselines work.
2. **Define an embodiment contract.** Version the observation variables, action bounds, simulator/backend, time step, forecasting availability, legal-action rules and termination/recovery behavior.
3. **Reproduce non-agent baselines.** Random/rule policy, OPF or MPC where applicable, then a standard RL policy. Save seeds and raw trajectories.
4. **Add a safety gate.** Compare proposed action, accepted action and rejection/projection reason. A higher reward with more violations is a negative result.
5. **Add decentralization or an LLM interface.** The LLM can choose an experiment/tool workflow or explain a solver-grounded decision; it cannot bypass action validation.
6. **Stress-test the loop.** Hold out load/PV profiles, outages, sensor noise, forecast errors, delayed communications and action cooldowns.
7. **Only then consider HIL.** Scope authority to advisory or sandbox modes and preserve an operator approval point.

## Research gaps worth pursuing

- **World-model fidelity for grid control:** learn/calibrate a fast surrogate while using an AC solver as a correctness oracle.
- **Multi-timescale embodiment:** coordinate seconds-to-minutes inverter actions with slower topology/dispatch decisions without hidden information leakage.
- **Safety-aware agent orchestration:** let an LLM select tools and hypotheses, while a typed action compiler and shield certify every candidate action.
- **Uncertainty-aware abstention:** the controller should defer to MPC/operator when state-estimation uncertainty or OOD score crosses a threshold.
- **Evaluation beyond mean reward:** disturbance recovery, violation severity, reject/projection rate, latency, calibration and operator workload.

## Non-claims

This corpus does not support claims of real-grid autonomy, guaranteed safety from reward shaping alone, or performance transfer from a single benchmark. Such claims need a formal safety argument, broader scenarios and hardware/field validation.
