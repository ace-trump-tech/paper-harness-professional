# Self-Learn: Embodied Intelligence for Power-Grid Control

This directory is a local, evidence-first research knowledge base. It follows the useful pattern in the supplied `paper/` and `code/` collections: keep the original paper and implementation separate from the distilled notes used during later reasoning.

## What "embodied" means here

The target is not an LLM that gives dispatch advice in text. It is a physically grounded closed loop:

```text
measurements / forecasts -> grid digital twin -> constrained decision -> validated action -> grid response -> audit record
```

An embodied grid controller must connect perception, state estimation or a world model, planning, a tool-backed action, physical constraints, and feedback. Real-grid actuation remains human-supervised. The first research target should be a simulator or hardware-in-the-loop digital twin, never autonomous production dispatch.

## Layout

- `papers/raw/`: only PDF files that passed a readable-page check.
- `papers/text/`: page-marked extracted text, so later retrieval does not repeatedly load PDFs.
- `knowledge/cards/`: one compact, citable research card per source.
- `knowledge/index/`: topic map, research gaps and experiment blueprint.
- `metadata/source-manifest.json`: canonical URLs, scope and download state.
- `metadata/code-sources.md`: official open-source implementations and licenses.
- `scripts/`: restartable download and extraction tools. A file enters a final directory only after validation.
- `metadata/incomplete/`: quarantined partial transfers. These are not source material.

At this snapshot, four papers are verified locally. No upstream code snapshot has passed the full-transfer check yet, so `code/` is intentionally empty; use `metadata/code-sources.md` and `scripts/download_code.sh` to refresh it when the network is stable.

## Literature-only dispatch study

The checked-in [first-round report](power-grid-literature-run/report.md) is the output of the non-CV workflow for “park-level source-grid-load-storage economic dispatch”. It contains a 15-paper DOI-verified core sample, a model/method comparison, and explicit claims that still require full-text coding. This run intentionally performs no simulation or algorithm implementation.

## Learn and query locally

Start with [the learning path](knowledge/index/learning-path.md), then use the [innovation bank](knowledge/index/innovation-bank.md) and [experiment blueprint](knowledge/index/experiment-blueprint.md) to move from concepts to a falsifiable study. The [Agent protocol](knowledge/index/agent-protocol.md) defines the Tutor, Literature, Research Designer and Safety Auditor roles.

```bash
python3 scripts/query_knowledge.py "储能 安全 门控 预测误差" --prompt
python3 scripts/test_query_knowledge.py
```

The query tool returns bounded snippets with relative source paths. It is intentionally model-agnostic: paste the context into your preferred Agent and require claims, evidence, assumptions, unknowns and human decisions in the returned JSON.

## Starting Point

Read `knowledge/index/research-map.md`, then choose one track:

1. **Distribution voltage control:** PowerGym or Gym-ANM.
2. **Transmission operation/topology control:** Grid2Op and L2RPN-style tasks.
3. **Decentralized coordination:** PowerGridworld or PowerNet.
4. **Safety before autonomy:** CommonPower plus the safe-RL reviews.
5. **Agentic orchestration:** foundation-model and X-GridAgent literature, but with numerical solvers as the authority.

## Refreshing Sources

```bash
cd /Users/tuozhongyao/Downloads/self-learn
./scripts/download_papers.sh
python3 scripts/extract_pdf_text.py
./scripts/download_code.sh
```

The scripts intentionally preserve a failed transfer outside the trusted corpus. Check the manifest and each upstream license before redistributing papers or code.
