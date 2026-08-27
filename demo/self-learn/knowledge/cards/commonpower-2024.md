# CommonPower (2024)

- **Source:** [arXiv:2406.03231](https://arxiv.org/abs/2406.03231), [code](https://github.com/TUMcps/commonpower)
- **Control task:** A symbolic modelling framework for comparing single-agent RL, multi-agent RL and optimal control with forecasts and safety mechanisms.
- **Core insight:** Vanilla RL does not itself guarantee power-system constraint satisfaction. The framework uses model-based safeguarding to study stronger protection of constraints.
- **Embodied loop contribution:** This is the required safety layer between an AI proposal and an actuator. A generated action should pass a feasibility/safety filter, be replaced or rejected when necessary, and log the intervention.
- **Use in this project:** Make shield intervention rate a first-class metric beside reward, loss and voltage quality. Compare unshielded RL, projection/shielded RL and MPC.
- **Limitation:** Formal guarantees depend on the fidelity and assumptions of the symbolic model. The safety case must state what faults, delays and uncertainty are outside the model.
