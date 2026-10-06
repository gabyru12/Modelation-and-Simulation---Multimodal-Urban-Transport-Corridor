"""Small TraCI wrapper used to control a SUMO simulation."""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Sequence

_traci_module: ModuleType | None = None


def _get_traci() -> ModuleType:
    """Import TraCI only when SUMO is actually started or queried."""
    global _traci_module
    if _traci_module is None:
        try:
            _traci_module = import_module("traci")
        except ImportError as exc:
            raise RuntimeError(
                "TraCI is not installed. Install dependencies with "
                "`python -m pip install -r requirements.txt`."
            ) from exc
    return _traci_module


class SumoInterface:
    """Encapsulate direct TraCI calls for a single SUMO simulation."""

    def __init__(
        self,
        config_path: str | Path,
        *,
        sumo_binary: str = "sumo",
        extra_args: Sequence[str] | None = None,
    ) -> None:
        self.config_path = Path(config_path)
        self.sumo_binary = sumo_binary
        self.extra_args = list(extra_args or [])
        self._running = False

    def start(self) -> None:
        """Start SUMO with the configured `.sumocfg` file."""
        if self._running:
            return

        command = [
            self.sumo_binary,
            "-c",
            str(self.config_path),
            "--no-step-log",
            "true",
            "--quit-on-end",
            "true",
            *self.extra_args,
        ]
        traci = _get_traci()
        traci.start(command)
        self._running = True

    def step(self) -> None:
        """Advance the simulation by one SUMO timestep."""
        self._ensure_running()
        traci = _get_traci()
        traci.simulationStep()

    def get_time(self) -> float:
        """Return the current SUMO simulation time in seconds."""
        self._ensure_running()
        traci = _get_traci()
        return float(traci.simulation.getTime())

    def get_vehicle_ids(self) -> list[str]:
        """Return the IDs of vehicles currently loaded in the network."""
        self._ensure_running()
        traci = _get_traci()
        return list(traci.vehicle.getIDList())

    def get_traffic_light_ids(self) -> list[str]:
        """Return the IDs of traffic lights present in the loaded network."""
        self._ensure_running()
        traci = _get_traci()
        return list(traci.trafficlight.getIDList())

    def get_min_expected_number(self) -> int:
        """Return vehicles still expected by SUMO, including pending departures."""
        self._ensure_running()
        traci = _get_traci()
        return int(traci.simulation.getMinExpectedNumber())

    def is_running(self) -> bool:
        """Return whether this interface currently owns an active TraCI session."""
        return self._running

    def close(self) -> None:
        """Close the active TraCI session if one is running."""
        if not self._running:
            return

        try:
            traci = _get_traci()
            traci.close()
        finally:
            self._running = False

    def _ensure_running(self) -> None:
        if not self._running:
            raise RuntimeError("SUMO simulation has not been started.")
