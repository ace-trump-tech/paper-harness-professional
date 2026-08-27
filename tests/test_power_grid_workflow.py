import json
import tempfile
import unittest
from pathlib import Path

from paper_harness.agents.base import AgentContext
from paper_harness.agents.power_grid import PowerGridBoundaryAgent, PowerGridScopeAgent, PowerGridTaxonomyAgent
from paper_harness.domain_packs import POWER_GRID
from paper_harness.models import Project
from paper_harness.orchestrator import ResearchOrchestrator


class PowerGridWorkflowTest(unittest.TestCase):
    def test_specialized_agents_emit_research_artifacts(self):
        project = Project("grid", domain="power_grid", objective="园区源网荷储经济调度")
        context = AgentContext(project, POWER_GRID, [])
        self.assertEqual(PowerGridScopeAgent().run(context).artifacts[0].kind, "power_grid_scope")
        self.assertEqual(PowerGridTaxonomyAgent().run(context).artifacts[0].kind, "power_grid_model_matrix")
        boundary = PowerGridBoundaryAgent().run(context).artifacts[0].payload
        self.assertEqual(boundary["experiments"], "not_applicable")

    def test_literature_only_mode_does_not_emit_gpu_or_cv_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = Project("grid", domain="power_grid", objective="园区源网荷储经济调度", root=str(root), settings={"research_mode": "power_grid_literature_only", "require_human_approval": False, "online": False})
            result = ResearchOrchestrator(root).run_round(project)
            kinds = {item["kind"] for item in result["artifacts"]}
            self.assertIn("power_grid_scope", kinds)
            self.assertIn("power_grid_model_matrix", kinds)
            self.assertIn("research_boundary", kinds)
            self.assertNotIn("gpu_experiment", kinds)
            self.assertNotIn("innovation_combinations", kinds)


if __name__ == "__main__":
    unittest.main()
