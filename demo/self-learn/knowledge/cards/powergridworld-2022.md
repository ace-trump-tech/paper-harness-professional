# PowerGridworld (2022)

- **Source:** [arXiv:2111.05969](https://arxiv.org/abs/2111.05969), [NREL paper record](https://www.nrel.gov/docs/fy22osti/81401.pdf), [code](https://github.com/NatLabRockies/PowerGridworld)
- **Control task:** Lightweight, modular multi-agent Gym environments for composite power-system devices; the paper demonstrates MADDPG and RLlib PPO in two case studies.
- **Embodied loop contribution:** Models heterogeneous devices as distinct agents while rewards can incorporate power-flow quantities at each step. This is useful when storage, inverters, flexible loads and a coordinator have different information and authority.
- **Use in this project:** Treat the hierarchy as an experimental variable: centralized critic, decentralized execution, and a safety-coordinator/shield should be compared under the same data and action budget.
- **Limitation:** Multi-agent decomposition can hide communication assumptions and cause non-stationarity. Report message delay, observation locality, reward allocation and failure behavior.
- **Local status:** canonical PDF and code URLs are in `metadata/source-manifest.json`; only verified files enter `papers/raw/`.
