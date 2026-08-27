# PowerGym (2022)

- **Source:** [arXiv:2109.03970](https://arxiv.org/abs/2109.03970), [code](https://github.com/siemens/powergym)
- **Local evidence:** `papers/raw/powergym.pdf`, `papers/text/powergym.txt` (19 pages; extracted text is the retrieval target).
- **Control task:** Distribution-grid Volt-Var control. The controller dispatches regulators, capacitor banks and batteries to reduce voltage violations and losses under network and device constraints.
- **Embodied loop contribution:** A clear observation-action-reward interface grounded in OpenDSS power-flow responses; suitable as the first digital-twin embodiment layer.
- **Benchmarks:** IEEE-derived 13-, 34-, 123-bus and 8500-node systems, with variants intended to test generalization and uncertainty.
- **Use in this project:** Start with a non-learning baseline and an explicit action validator, then compare PPO/SAC-style policies under held-out load/PV traces.
- **Limitation:** Gym interaction does not establish deployable operational safety. It models selected quasi-static distribution control decisions, not protection or transient dynamics.
- **Evidence to retain per run:** feeder/config version, observation schema, action bounds, OpenDSS version, seed, voltage-violation rate, loss, rejected actions and scenario split.
