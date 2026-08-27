# Minimal Experiment Blueprint

## Research question

Can a tool-grounded controller improve a grid objective while preserving operational constraints under distribution shift?

## Initial setting

- **Environment:** PowerGym 13Bus or Gym-ANM ANM6-Easy for a small controlled study.
- **Observation:** all variables actually available at decision time; no future measurements unless declared as forecasts.
- **Action:** reactive-power/battery/regulator action within environment-provided bounds.
- **Baselines:** random, rule/OpenDSS controller if available, MPC/OPF where valid, PPO or SAC.
- **Candidate:** RL policy plus action projection or safety shield. Treat an LLM only as a non-real-time experiment planner/explainer in phase one.

## Evaluation protocol

| Dimension | Required report |
| --- | --- |
| Benefit | power loss, control cost, task reward |
| Safety | voltage/thermal violations, severity, duration, feasibility rate |
| Robustness | held-out demand/PV traces, noise, forecast error, contingencies |
| Intervention | proposed vs accepted action, shield activation/rejection rate |
| Reproducibility | code commit, package versions, scenario/config hash, seeds, trajectories |
| Operational realism | decision latency, action cooldowns, observability assumptions, failure recovery |

## Ablations

1. No shield vs projection/shield.
2. Perfect vs noisy/lagged observations.
3. In-distribution vs held-out scenarios.
4. Centralized vs decentralized information.
5. Solver-only planner vs LLM-assisted tool orchestration, with the same numerical validator.

## Stop conditions

Stop promoting a method if it increases violation severity, relies on unavailable observations, has unreported action rejection, or fails under basic forecast/communication shift. Record the negative result rather than tuning it away.
