# 逐篇论文编码模板

复制此模板到 `knowledge/cards/`，文件名使用 `作者-年份-短标题.md`。只填写原文能支持的字段；不确定时写 `unknown`，不要用模型常识补全。

```yaml
source:
  title: ""
  authors: []
  venue: ""
  year: 0
  doi: ""
  url: ""
  license: "unknown"
task:
  grid_level: "distribution|transmission|microgrid|multi-energy|unknown"
  scenario: ""
  time_scale: "day-ahead|intra-day|real-time|episode|unknown"
  environment_or_data: ""
model:
  components: []
  observations_or_inputs: []
  state: []
  actions_or_decisions: []
  objectives: []
  constraints: []
method:
  family: "optimization|MPC|RL|MARL|LLM-agent|hybrid|unknown"
  algorithm: ""
  solver_or_framework: ""
evaluation:
  baselines: []
  metrics: []
  stress_tests: []
  key_result: ""
  limitations: []
provenance:
  evidence_pages: []
  extracted_text: "papers/text/"
  code_url: ""
  checked_by: ""
  checked_at: ""
```

## 编码规则

- “key_result”必须能在正文、表格或图中定位；摘要单独出现的数字标记为 `abstract_only`。
- 将成本、碳排、约束违例、恢复时间和推理延迟分开记录，不能用一个综合分数替代安全指标。
- 明确 proposed action、accepted action 和拒绝/投影原因；没有安全门时写 `not reported`。
- 对代码记录官方 URL、commit/tag 和许可证；无法确认许可证时禁止重新分发。
