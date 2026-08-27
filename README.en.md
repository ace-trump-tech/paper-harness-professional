# paper-harness-professional

**Languages:** [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md)

> An auditable professional Auto-Research harness for CV exploration and power-grid embodied-control studies: local knowledge, innovation combinations, per-GPU experiments, metric evaluation and evidence-bound writing.

```bash
python -m paper_harness.cli init examples/cv_exploration_project.json --output ./runs/cv-demo
python -m paper_harness.cli run ./runs/cv-demo/project.json
```

The repository uses explicit stage contracts, a finite-metric experiment harness, GPU discovery for planning, and SHA-256 artifact manifests. GPU work is dry-run by default: real training requires an approved repository, dataset, runtime, budget and experiment configuration. It never fabricates metrics or accepts an idea as a validated contribution automatically.

See the [CV workflow](docs/cv-exploration-zh.md), [power-grid embodied-control demo](demo/self-learn/README.md), and [harness architecture](docs/harness-architecture-zh.md).

The general undergraduate edition is maintained separately at [paper-harness-undergraduate](https://github.com/ace-trump-tech/paper-harness-undergraduate). Together, the two repositories form the complete paper-harness product.
