# Open-Source Code Sources

These repositories are recorded separately from the downloaded corpus. The download script uses shallow clones and validates the Git object database before making a clone visible under `code/`.

| Project | Role in this research direction | Upstream | License reported upstream |
| --- | --- | --- | --- |
| Grid2Op | Transmission-grid sequential decision environment; topology, redispatch, curtailment and maintenance actions | https://github.com/Grid2op/grid2op | MPL-2.0 |
| PowerGym | Distribution Volt-Var benchmark backed by OpenDSS | https://github.com/siemens/powergym | MIT |
| PowerGridworld | Modular multi-agent RL power-system environments | https://github.com/NatLabRockies/PowerGridworld | BSD-3-Clause |
| Gym-ANM | Active-network-management environments for distribution grids | https://github.com/robinhenry/gym-anm | MIT |
| CommonPower | Symbolic safe-RL / MPC framework for smart-grid control | https://github.com/TUMcps/commonpower | Inspect upstream `LICENSE` before reuse |

Do not merge these projects into a new codebase without preserving attribution and each upstream license. Their primary value here is as reproducible environments and reference implementations, not as production dispatch software.
