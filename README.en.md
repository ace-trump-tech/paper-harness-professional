# paper-harness-professional

**Languages:** [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md)

> An auditable professional Auto-Research harness that can move from a research question to a literature base, innovation candidates, experiment/code tasks, reproducible results and a paper draft. It is not an evidence-free black box: claims remain bound to sources, runs and human approval.

```text
question/codebase -> local literature knowledge -> hypotheses and A+B+C candidates
    -> experiments, simulators or code-repository tasks -> metrics and failure analysis
    -> figures, paper draft and audit review -> human-approved release
```

Experiments preserve configuration, random seeds, data provenance, metrics, failure logs, artifact hashes and approvals. For power-grid/control work, the simulator, numerical solver and safety gate are authoritative; an LLM/Agent may plan, call tools and explain results, but cannot directly issue an unvalidated control action or submit a paper.

```bash
python -m paper_harness.cli init examples/cv_exploration_project.json --output ./runs/cv-demo
python -m paper_harness.cli run ./runs/cv-demo/project.json
```

The repository uses explicit stage contracts, a finite-metric experiment harness, GPU discovery for planning, and SHA-256 artifact manifests. GPU work is dry-run by default: real training requires an approved repository, dataset, runtime, budget and experiment configuration. It never fabricates metrics or accepts an idea as a validated contribution automatically.

See the [CV workflow](docs/cv-exploration-zh.md), [power-grid embodied-control demo](demo/self-learn/README.md), [power-grid literature report](demo/self-learn/power-grid-literature-run/report.md), and [harness architecture](docs/harness-architecture-zh.md).

The general undergraduate edition is maintained separately at [paper-harness-undergraduate](https://github.com/ace-trump-tech/paper-harness-undergraduate). Together, the two repositories form the complete paper-harness product.
