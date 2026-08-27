# Grid2Op (2020-)

- **Source:** [official code](https://github.com/Grid2op/grid2op), [documentation](https://grid2op.readthedocs.io/)
- **Control task:** Sequential transmission-grid operation, including topology changes, generator set points, redispatch, curtailment, load shedding and maintenance contingencies.
- **Embodied loop contribution:** Its explicit `observation -> legal action -> backend power flow -> next observation` boundary is an appropriate action interface for an agentic controller.
- **Use in this project:** Prefer topology-control and N-1 contingency scenarios for studying long-horizon planning, tool calls and action approval.
- **Key architectural lesson:** The language/strategy agent must not be the numerical authority. It should propose a typed action; Grid2Op plus its backend should reject illegal actions and produce the state transition.
- **Limitation:** A simulator is still an approximation of a grid. Train/test splits must include outages, forecast shifts and action cooldowns; no result transfers directly to dispatch practice.
- **Local status:** upstream and reproduction instructions are indexed in `metadata/code-sources.md`; code download is retryable through `scripts/download_code.sh`.
