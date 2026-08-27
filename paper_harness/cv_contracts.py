"""Explicit CV stage contracts, kept smaller than a general research pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class CVStageContract:
    name: str
    inputs: Tuple[str, ...]
    outputs: Tuple[str, ...]
    definition_of_done: str
    approval_required: bool


CONTRACTS: Dict[str, CVStageContract] = {
    "knowledge": CVStageContract("knowledge", ("local papers/notes",), ("knowledge/index.json",), "Each source has bounded chunks and provenance.", False),
    "combinations": CVStageContract("combinations", ("knowledge index",), ("innovation_combinations",), "A, B, C and selected combinations are explicit.", True),
    "experiments": CVStageContract("experiments", ("approved combinations", "baseline repository", "dataset manifest"), ("gpu_experiment", "results.json"), "Every run has config, device, logs and finite metrics.", True),
    "evaluation": CVStageContract("evaluation", ("results.json", "reference metrics"), ("cv_evaluation",), "Metrics use the same split and protocol as references.", True),
    "composition": CVStageContract("composition", ("literature", "experiments", "evaluation"), ("cv_composition", "draft"), "Each numerical claim points to an artifact.", True),
}
