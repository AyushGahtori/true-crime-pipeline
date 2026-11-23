"""YAML/dict loaders. Prices are whatever the source document contains."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml

from shared_contracts.models import CraftRubric, ProviderRegistry

CRAFT_RUBRIC_MAX_LINES = 150


class RegistrySourceError(ValueError):
    """The registry or rubric source was missing or not a mapping."""


def _read_mapping(source: str | Path | Mapping[str, Any], *, line_cap: int | None) -> dict[str, Any]:
    if isinstance(source, Mapping):
        return dict(source)
    path = Path(source)
    if not path.is_file():
        raise RegistrySourceError(f"registry source not found: {path}")
    text = path.read_text(encoding="utf-8")
    if line_cap is not None and len(text.splitlines()) > line_cap:
        raise RegistrySourceError(f"rubric exceeds {line_cap} lines: {path}")
    loaded = yaml.safe_load(text)
    if not isinstance(loaded, dict):
        raise RegistrySourceError(f"registry source must be a mapping: {path}")
    return loaded


class YamlProviderRegistryLoader:
    def load(self, source: str | Path | Mapping[str, Any]) -> ProviderRegistry:
        return ProviderRegistry.model_validate(_read_mapping(source, line_cap=None))


class YamlCraftRubricLoader:
    def load(self, source: str | Path | Mapping[str, Any]) -> CraftRubric:
        return CraftRubric.model_validate(
            _read_mapping(source, line_cap=CRAFT_RUBRIC_MAX_LINES if not isinstance(source, Mapping) else None)
        )
