"""Deterministic external-margin 10x10 cell to pixel and zoom. No I/O.

Pixel center of cell (col, row), 0-based:
    x_px = round_half_up((2 * col + 1) * width_px / 20)
    y_px = round_half_up((2 * row + 1) * height_px / 20)

Zoom follows the span crop in crime-scene-2k Task 145:
    zoom_axis = 8 / span_axis
    target_zoom = clamp(min(zoom_x, zoom_y), 1.6, 3.8)
Unclamped axis zooms are quantized to 4 decimal places (half up) before the min.
"""

from __future__ import annotations

import re
from decimal import Decimal, ROUND_HALF_UP
from typing import Any

_CELL = re.compile(r"^([A-J])([1-9]|10)$")
_ZOOM_MIN = Decimal("1.6")
_ZOOM_MAX = Decimal("3.8")
_Q = Decimal("0.0001")


def _round_half_up_div(numer: int, denom: int) -> int:
    if numer < 0 or denom <= 0:
        raise ValueError("pixel division requires a non-negative numerator")
    return (numer + denom // 2) // denom


def _quantize_zoom(span: float) -> float:
    if isinstance(span, bool) or not isinstance(span, (int, float)):
        raise ValueError("span must be a number")
    raw = Decimal(8) / Decimal(str(span))
    return float(raw.quantize(_Q, rounding=ROUND_HALF_UP))


def grid_cell_to_pixel_and_zoom(
    grid_cell: str,
    span_cols: float = 1.0,
    span_rows: float = 1.0,
    width_px: int = 2560,
    height_px: int = 1440,
) -> dict[str, Any]:
    """Map one A-J / 1-10 cell plus span onto clean-plate pixels and zoom."""
    if not isinstance(grid_cell, str):
        raise ValueError("grid_cell must be a string")
    match = _CELL.fullmatch(grid_cell)
    if match is None:
        raise ValueError("grid_cell must match [A-J][1-9] or [A-J]10")
    if isinstance(width_px, bool) or isinstance(height_px, bool):
        raise ValueError("plate dimensions must be positive integers")
    if not isinstance(width_px, int) or not isinstance(height_px, int):
        raise ValueError("plate dimensions must be positive integers")
    if width_px <= 0 or height_px <= 0:
        raise ValueError("plate dimensions must be positive")
    if isinstance(span_cols, bool) or isinstance(span_rows, bool):
        raise ValueError("span must be within (0, 10]")
    if not isinstance(span_cols, (int, float)) or not isinstance(span_rows, (int, float)):
        raise ValueError("span must be numeric")
    if not (0 < float(span_cols) <= 10) or not (0 < float(span_rows) <= 10):
        raise ValueError("span_cols and span_rows must be within (0, 10]")

    col_index = ord(match.group(1)) - ord("A")
    row_index = int(match.group(2)) - 1
    x_px = _round_half_up_div((2 * col_index + 1) * width_px, 20)
    y_px = _round_half_up_div((2 * row_index + 1) * height_px, 20)
    zoom_x = _quantize_zoom(float(span_cols))
    zoom_y = _quantize_zoom(float(span_rows))
    target = Decimal(str(min(zoom_x, zoom_y)))
    if target < _ZOOM_MIN:
        target = _ZOOM_MIN
    elif target > _ZOOM_MAX:
        target = _ZOOM_MAX
    target_zoom = float(target.quantize(_Q, rounding=ROUND_HALF_UP))
    return {
        "grid_cell": grid_cell,
        "col_index": col_index,
        "row_index": row_index,
        "x_px": x_px,
        "y_px": y_px,
        "span_cols": float(span_cols),
        "span_rows": float(span_rows),
        "zoom_x": zoom_x,
        "zoom_y": zoom_y,
        "target_zoom": target_zoom,
        "width_px": width_px,
        "height_px": height_px,
    }
