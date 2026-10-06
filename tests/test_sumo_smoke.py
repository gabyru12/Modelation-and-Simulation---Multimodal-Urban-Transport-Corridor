from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

from src.integration.sumo_interface import SumoInterface
from src.simulation.runner import run_simulation


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "sumo_smoke"


def _require_python_dependencies() -> None:
    pytest.importorskip("mesa", reason="Mesa is not installed.")
    pytest.importorskip("traci", reason="TraCI is not installed.")
    pytest.importorskip("sumolib", reason="sumolib is not installed.")


def _require_sumo_binary(name: str) -> str:
    binary_path = shutil.which(name)
    if binary_path is None:
        pytest.skip(f"{name!r} binary is not available on PATH.")
    return binary_path


def _prepare_sumo_fixture(tmp_path: Path) -> Path:
    for fixture_file in FIXTURE_DIR.iterdir():
        shutil.copy2(fixture_file, tmp_path / fixture_file.name)

    netconvert = _require_sumo_binary("netconvert")
    subprocess.run(
        [
            netconvert,
            "--node-files",
            str(tmp_path / "smoke.nod.xml"),
            "--edge-files",
            str(tmp_path / "smoke.edg.xml"),
            "--output-file",
            str(tmp_path / "smoke.net.xml"),
            "--no-turnarounds",
            "true",
        ],
        check=True,
        cwd=tmp_path,
    )
    return tmp_path / "smoke.sumocfg"


def test_python_can_control_minimal_sumo_simulation(tmp_path: Path) -> None:
    _require_python_dependencies()
    sumo = _require_sumo_binary("sumo")
    config_path = _prepare_sumo_fixture(tmp_path)

    interface = SumoInterface(config_path, sumo_binary=sumo)
    observed_vehicle_ids: set[str] = set()

    try:
        interface.start()
        assert interface.is_running()

        while interface.get_min_expected_number() > 0:
            interface.step()
            observed_vehicle_ids.update(interface.get_vehicle_ids())
    finally:
        interface.close()

    assert "veh0" in observed_vehicle_ids
    assert not interface.is_running()

    completed_steps = run_simulation(config_path, sumo_binary=sumo, max_steps=100)
    assert completed_steps > 0
