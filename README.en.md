# paper-harness-cv

**Languages:** [简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md)

> An auditable multi-agent Auto-Research harness for computer vision: local knowledge, A+B+C idea combinations, one planned sub-agent per GPU, metric evaluation and evidence-bound writing.

```bash
python -m paper_harness.cli init examples/cv_exploration_project.json --output ./runs/cv-demo
python -m paper_harness.cli run ./runs/cv-demo/project.json
```

The repository uses explicit stage contracts, a finite-metric experiment harness, GPU discovery for planning, and SHA-256 artifact manifests. GPU work is dry-run by default: real training requires an approved repository, dataset, runtime, budget and experiment configuration. It never fabricates metrics or accepts an idea as a validated contribution automatically.

See [CV workflow notes](docs/cv-exploration-zh.md) and [harness architecture](docs/harness-architecture-zh.md).
