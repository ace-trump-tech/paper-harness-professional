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

## Distilled learning layers

| Layer | Entry point | Purpose |
| --- | --- | --- |
| Orientation | `index/learning-path.md` | Zero-to-research sequence with checkpoints |
| Concepts | `cards/*.md` and `index/research-map.md` | Short, citable explanations of environments, safety and agents |
| Research | `index/innovation-bank.md` and `index/experiment-blueprint.md` | Falsifiable ideas, baselines, ablations and stop conditions |
| Agent interface | `index/agent-protocol.md` and `index/catalog.json` | Stable context and JSON output contract |
| Applied survey | `../../power-grid-literature-run/report.md` | Economic dispatch problem and method taxonomy |

Use `python3 scripts/query_knowledge.py "your question" --prompt` to retrieve bounded context. The script reads only distilled cards, indexes and reports; it does not repeatedly load full PDFs.

## Suggested search terms

- `voltage violation`, `reactive power`, `OpenDSS`, `battery`
- `topology`, `redispatch`, `contingency`, `L2RPN`
- `multi-agent`, `MADDPG`, `centralized critic`, `partial observation`
- `safeguard`, `constraint`, `projection`, `MPC`, `feasibility`
- `tool calling`, `digital twin`, `world model`, `human approval`
