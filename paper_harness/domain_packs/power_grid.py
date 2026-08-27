from .base import DomainPack


POWER_GRID = DomainPack(
    name="power_grid",
    evidence_types=["paper", "dataset", "code", "simulator", "optimization_model", "safety_constraint", "statistic"],
    review_questions=[
        "Does the source define the grid boundary, time scale and controllable devices?",
        "Are objective terms, power balance and device/network constraints explicit?",
        "Are baselines, forecasts, uncertainty and safety violations reported separately?",
        "Is an LLM used only as an interface/planner while a solver or simulator validates actions?",
    ],
    experiment_modes=["power-flow-simulation", "optimization", "hardware-in-the-loop"],
    visual_mode="modular",
    visual_constraints=["separate source-grid-load-storage layers", "label time scale and constraints", "bind every claim to a source or run artifact"],
    research_modes=["literature_only", "full"],
)
