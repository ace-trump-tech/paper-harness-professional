# Gym-ANM (2021)

- **Source:** [arXiv:2103.07932](https://arxiv.org/abs/2103.07932), [code](https://github.com/robinhenry/gym-anm)
- **Control task:** Active network management in electricity distribution systems with renewable generation and storage. It includes the educational `ANM6-Easy` environment and supports task customisation.
- **Embodied loop contribution:** A compact, Gymnasium-compatible environment is useful for proving the controller interface before moving to an OpenDSS or transmission benchmark.
- **Use in this project:** Establish a minimal reproducibility suite: random, rule-based, MPC and RL policy on identical scenario seeds. Add an explicit action projector before comparing learning algorithms.
- **Limitation:** An introductory environment should not be used to claim scalability or operational readiness. It is a controlled testbed for observation/action design and ablation studies.
- **Local status:** source URLs are registered; partial transfer quarantine is intentionally excluded from the corpus.
