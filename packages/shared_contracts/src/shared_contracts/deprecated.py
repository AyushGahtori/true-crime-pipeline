"""Retired v2 identifiers that must never validate as current v4 values."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

DEPRECATED_IDENTIFIERS: frozenset[str] = frozenset(
    {
        "FRAMES_MOTION_ONLY",
        "VEO_3_1_LITE",
        "CrimeScenePanZoom",
    }
)


class DeprecatedIdentifierError(ValueError):
    """Raised when a retired identifier appears anywhere in a payload."""


def find_deprecated(value: Any, *, where: str = "$") -> str | None:
    if isinstance(value, str):
        for token in DEPRECATED_IDENTIFIERS:
            if token in value:
                return f"{token} at {where}"
        return None
    if isinstance(value, Mapping):
        for key, item in value.items():
            key_text = str(key)
            for token in DEPRECATED_IDENTIFIERS:
                if token in key_text:
                    return f"{token} at {where}.{key_text}"
            found = find_deprecated(item, where=f"{where}.{key_text}")
            if found:
                return found
        return None
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            found = find_deprecated(item, where=f"{where}[{index}]")
            if found:
                return found
        return None
    return None


def reject_deprecated(value: Any) -> None:
    found = find_deprecated(value)
    if found:
        raise DeprecatedIdentifierError(f"deprecated identifier rejected: {found}")
