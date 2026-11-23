"""Pure 10x10 grid math."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from shared_contracts.grid import grid_cell_to_pixel_and_zoom

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "vectors.json"


def test_grid_cases_match_fixture() -> None:
    document = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert document["grid"]
    for case in document["grid"]:
        assert grid_cell_to_pixel_and_zoom(**case["args"]) == case["expect"]


def test_known_centers_and_zoom_caps() -> None:
    narrow = grid_cell_to_pixel_and_zoom("E5", 1, 1, 2560, 1440)
    assert (narrow["x_px"], narrow["y_px"]) == (1152, 648)
    assert narrow["target_zoom"] == 3.8
    wide = grid_cell_to_pixel_and_zoom("A1", 5, 3, 2560, 1440)
    assert wide["zoom_x"] == 1.6
    assert wide["target_zoom"] == 1.6
    tall = grid_cell_to_pixel_and_zoom("A1", 1, 4, 2560, 1440)
    assert tall["zoom_y"] == 2.0
    assert tall["target_zoom"] == 2.0
    corner = grid_cell_to_pixel_and_zoom("A1", 1, 1, 2048, 1152)
    assert (corner["x_px"], corner["y_px"]) == (102, 58)


def test_grid_is_deterministic_and_rejects_bad_cells() -> None:
    first = grid_cell_to_pixel_and_zoom("J10")
    second = grid_cell_to_pixel_and_zoom("J10")
    assert first == second
    with pytest.raises(ValueError):
        grid_cell_to_pixel_and_zoom("K1")
    with pytest.raises(ValueError):
        grid_cell_to_pixel_and_zoom("A0")
    with pytest.raises(ValueError):
        grid_cell_to_pixel_and_zoom("A1", span_cols=0)
