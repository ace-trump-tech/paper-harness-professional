# Safe RL Reviews for Power Systems (2024)

- **Sources:** [Yu et al., arXiv:2407.00681](https://arxiv.org/abs/2407.00681); [Su et al., arXiv:2407.00304](https://arxiv.org/abs/2407.00304)
- **Scope:** Reviews of safe RL for frequency/voltage control, energy management, dispatch, restoration and related tasks.
- **Knowledge-base conclusion:** Better average reward is not an adequate result for a safety-critical controller. Report constraint violations during training and evaluation, severity and duration of violations, feasibility rate, recovery time, forecast shift robustness and inference latency.
- **Method categories to distinguish:** reward penalties, constrained RL, action projection/shields, Lyapunov or control-barrier approaches, robust/domain-randomized policies, and human approval. These are not equivalent guarantees.
- **Use in this project:** Build every experiment around a safety claim that is testable in the selected simulator. Never promote a penalty-only method as a hard safety guarantee.
