# Large Foundation Models for Power Systems (2023)

- **Source:** [arXiv:2312.07044](https://arxiv.org/abs/2312.07044)
- **Scope:** Evaluates general foundation-model capabilities across OPF, EV scheduling, technical-document retrieval and situation awareness.
- **Embodied loop contribution:** Natural-language and multimodal models can lower the interface cost for engineers, retrieve procedures and formulate tool calls. They should sit above, rather than replace, power-flow, optimization and protection engines.
- **Use in this project:** Constrain the model to a typed tool schema: inspect state, query knowledge, propose action, call simulator, check safety, explain evidence. Store each call and numeric result.
- **Limitation:** The work motivates operational assistance; it does not prove that unverified free-form text is a safe grid-control policy.
