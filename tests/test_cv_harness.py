import tempfile
import unittest
from pathlib import Path

from paper_harness.cv_harness import CVExperimentHarness
from paper_harness.run_manifest import verify_artifact_manifest, write_artifact_manifest


class CVHarnessTest(unittest.TestCase):
    def test_harness_rejects_non_finite_metrics_and_writes_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = CVExperimentHarness(Path(tmp), time_budget_seconds=10)
            self.assertTrue(harness.report_metric("mAP", 0.42, step=1))
            self.assertFalse(harness.report_metric("loss", float("nan"), step=1))
            result = harness.finalize()
            self.assertTrue(result.exists())
            self.assertIn("mAP", result.read_text(encoding="utf-8"))

    def test_manifest_detects_artifact_mutation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifacts = root / "artifacts"
            artifacts.mkdir()
            item = artifacts / "item.json"
            item.write_text('{"value": 1}\n', encoding="utf-8")
            write_artifact_manifest(root, artifacts, "project-1")
            self.assertEqual(verify_artifact_manifest(root, artifacts)["status"], "valid")
            item.write_text('{"value": 2}\n', encoding="utf-8")
            self.assertEqual(verify_artifact_manifest(root, artifacts)["status"], "changed")


if __name__ == "__main__":
    unittest.main()
