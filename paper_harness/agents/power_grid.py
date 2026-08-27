from __future__ import annotations

from typing import Dict, List

from .base import Agent, AgentContext, artifact
from ..models import AgentResult


SEARCH_BLOCKS = {
    "definition": ["source-grid-load-storage economic dispatch park microgrid", "园区 源网荷储 经济调度"],
    "modeling": ["microgrid economic dispatch photovoltaic wind battery load grid purchase sale model", "源网荷储 目标函数 约束 储能 SOC"],
    "optimization": ["microgrid economic dispatch MILP MPC robust stochastic optimization", "园区综合能源 经济调度 混合整数 多目标"],
    "learning": ["reinforcement learning microgrid energy management economic dispatch", "深度强化学习 微电网 能量管理 经济调度"],
    "agentic": ["LLM microgrid energy management economic dispatch optimal scheduling", "大语言模型 微电网 能量管理 经济调度"],
}


class PowerGridScopeAgent(Agent):
    name = "power-grid-scope"

    def run(self, context: AgentContext) -> AgentResult:
        questions = [
            "源、网、荷、储的系统边界与设备角色是什么？",
            "输入、决策变量、目标函数、约束和输出分别是什么？",
            "日前、日内、实时调度和能量管理/电压控制如何区分？",
            "数学规划、智能优化、多目标优化、强化学习和 LLM 方法如何比较？",
            "纯经济能量调度与含潮流/电压/线路安全约束的调度有什么差异？",
        ]
        payload = {"research_question": context.project.objective or context.project.title, "scope": "园区级源网荷储经济优化调度", "questions": questions, "search_blocks": SEARCH_BLOCKS, "exclusions": ["implementation", "simulation", "algorithm programming", "unsupported claims from abstracts only"], "deliverable": "structured literature review before any experiment"}
        return AgentResult(self.name, "completed", [artifact("power_grid_scope", context.project, self.name, payload, 0.85)], "Parsed the power-grid literature-only scope and search blocks.")


class PowerGridSourceAgent(Agent):
    name = "power-grid-source-manager"

    def run(self, context: AgentContext) -> AgentResult:
        literature = next((item for item in reversed(context.artifacts) if item.kind == "literature_search"), None)
        records = literature.payload.get("records", []) if literature else []
        manifest = [{"source_id": item.get("external_id") or item.get("url") or item.get("title"), "title": item.get("title"), "url": item.get("url"), "year": item.get("year"), "abstract_status": "present" if item.get("abstract") else "missing", "full_text_status": "download_required", "code_status": "inspect_source"} for item in records]
        payload = {"records": manifest, "download_policy": "download open-access PDFs only; preserve DOI/URL/license", "local_text_policy": "extract once, retrieve bounded text thereafter", "code_policy": "record official repository and license; do not execute during literature-only mode", "missing_fields": sorted({field for row in manifest for field in ("abstract_status", "full_text_status") if not row.get(field)})}
        return AgentResult(self.name, "completed", [artifact("power_grid_source_manifest", context.project, self.name, payload, 0.65)], "Recorded source acquisition and extraction requirements without executing code.")


class PowerGridTaxonomyAgent(Agent):
    name = "power-grid-taxonomy"

    def run(self, context: AgentContext) -> AgentResult:
        matrix: List[Dict[str, object]] = [
            {"category": "system", "fields": ["PV", "wind", "grid exchange", "load", "storage", "EV/flexible load"], "evidence_required": "system boundary and data source"},
            {"category": "inputs", "fields": ["renewable forecast", "load forecast", "buy/sell tariff", "capacity", "SOC", "efficiency", "power limits"], "evidence_required": "forecast horizon and availability"},
            {"category": "decisions", "fields": ["charge/discharge", "grid purchase/sale", "dispatchable generation", "demand response", "curtailment"], "evidence_required": "variable domain and time step"},
            {"category": "objectives", "fields": ["operating cost", "peak-valley", "renewable utilization", "degradation", "carbon", "comfort"], "evidence_required": "normalization/weights or Pareto protocol"},
            {"category": "constraints", "fields": ["power balance", "SOC", "charge/discharge exclusivity", "ramp/start-stop", "network flow", "voltage/thermal limits"], "evidence_required": "hard vs soft constraint"},
            {"category": "methods", "fields": ["LP/QP/MILP/MINLP", "DP/MPC", "robust/stochastic", "PSO/GA/DE", "NSGA-II/MOPSO", "Q-learning/DQN/DDPG/TD3/SAC/PPO", "LLM/tool-assisted"], "evidence_required": "model assumptions, complexity, baseline and guarantee"},
        ]
        return AgentResult(self.name, "completed", [artifact("power_grid_model_matrix", context.project, self.name, {"matrix": matrix, "comparison_rule": "do not rank methods without matching system, horizon, data, constraints and baselines"}, 0.8)], "Built a source-grounded modeling and method taxonomy.")


class PowerGridEvidenceAgent(Agent):
    name = "power-grid-evidence-critic"

    def run(self, context: AgentContext) -> AgentResult:
        literature = next((item for item in reversed(context.artifacts) if item.kind == "literature_search"), None)
        records = literature.payload.get("records", []) if literature else []
        required = ["definition", "modeling", "optimization", "learning", "agentic"]
        payload = {"coverage": {block: "needs_full_text_coding" for block in required}, "source_count": len(records), "checks": ["separate abstract evidence from full-text evidence", "do not infer prevalence from search ranking", "do not call penalty methods hard safety guarantees", "do not call LLM text a validated control action"], "blocked_claims": ["most common objective", "method superiority", "real-grid deployability"], "human_review_required": True}
        return AgentResult(self.name, "completed", [artifact("power_grid_evidence_review", context.project, self.name, payload, 0.75)], "Audited evidence coverage and blocked unsupported method rankings.")


class PowerGridBoundaryAgent(Agent):
    name = "power-grid-research-boundary"

    def run(self, context: AgentContext) -> AgentResult:
        return AgentResult(self.name, "completed", [artifact("research_boundary", context.project, self.name, {"mode": "literature_only", "experiments": "not_applicable", "simulation": "not_applicable", "code_execution": "not_applicable", "next_allowed_step": "human-approved full-text synthesis", "reason": "user request explicitly limits this task to literature review"}, 0.95)], "Marked implementation, simulation and algorithm execution as out of scope.")


class PowerGridSynthesisAgent(Agent):
    name = "power-grid-synthesis"

    def run(self, context: AgentContext) -> AgentResult:
        kinds = [item.kind for item in context.artifacts]
        payload = {"format": "literature-review-outline", "sections": ["problem definition", "system and mathematical model", "objectives and constraints", "method taxonomy", "comparison protocol", "LLM/agentic methods", "research gaps and recommended next step"], "available_artifacts": kinds, "claim_policy": "every prevalence/comparison statement requires coded paper rows and citations", "status": "outline-only", "human_review_required": True}
        return AgentResult(self.name, "completed", [artifact("power_grid_literature_synthesis", context.project, self.name, payload, 0.7)], "Prepared a literature-review outline without inventing rankings or experiments.")
