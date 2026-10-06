"""Utilities for running SUMO simulations through the integration layer."""

from __future__ import annotations

from pathlib import Path

from src.integration.sumo_interface import SumoInterface


def run_simulation(
    config_path: str | Path,
    *,
    sumo_binary: str = "sumo",
    max_steps: int | None = None,
) -> int:
    """Run a SUMO simulation until no vehicles are expected.

    Returns the number of timesteps advanced. `max_steps` is a defensive guard
    for tests and early experiments.
    """
    interface = SumoInterface(config_path, sumo_binary=sumo_binary)
    steps = 0

    try:
        interface.start()
        while interface.get_min_expected_number() > 0:
            if max_steps is not None and steps >= max_steps:
                raise RuntimeError(f"Simulation exceeded max_steps={max_steps}.")

            interface.step()
            steps += 1
    finally:
        interface.close()

    return steps
