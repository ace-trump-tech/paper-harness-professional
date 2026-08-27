# Local Corpus Index

## Verified local papers

| ID | PDF | Extracted text | Main use |
| --- | --- | --- | --- |
| PowerGym | `papers/raw/powergym.pdf` | `papers/text/powergym.txt` | Volt-Var control benchmark |
| PowerGridworld | `papers/raw/powergridworld.pdf` | `papers/text/powergridworld.txt` | Multi-agent environment design |
| Gym-ANM | `papers/raw/gym-anm.pdf` | `papers/text/gym-anm.txt` | Active network management prototype |
| CommonPower | `papers/raw/commonpower.pdf` | `papers/text/commonpower.txt` | Safe RL and model-based safeguards |

## Retrieval rule

Start from the relevant card in `knowledge/cards/`. Use `papers/text/` for retrieval and quote verification, then return to the page-marked PDF only for equations, figures, tables or nuanced claims. This keeps subsequent agent context bounded while retaining a direct path to the source.

## Suggested search terms

- `voltage violation`, `reactive power`, `OpenDSS`, `battery`
- `topology`, `redispatch`, `contingency`, `L2RPN`
- `multi-agent`, `MADDPG`, `centralized critic`, `partial observation`
- `safeguard`, `constraint`, `projection`, `MPC`, `feasibility`
- `tool calling`, `digital twin`, `world model`, `human approval`
