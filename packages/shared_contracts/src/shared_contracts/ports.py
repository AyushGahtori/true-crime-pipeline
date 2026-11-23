"""Runtime ports. Implementations must not call provider APIs."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Mapping, Protocol, runtime_checkable

from shared_contracts.models import CraftRubric, ProviderRegistry, RenderReceipt, TimelineSpec


@runtime_checkable
class RenderBackendPort(Protocol):
    def render(self, spec: TimelineSpec) -> RenderReceipt:
        """Render one timeline spec and return a receipt. No network."""


@runtime_checkable
class ProviderRegistryLoader(Protocol):
    def load(self, source: str | Path | Mapping[str, object]) -> ProviderRegistry:
        """Load a registry from a mapping or a YAML path. Do not invent prices."""


@runtime_checkable
class CraftRubricLoader(Protocol):
    def load(self, source: str | Path | Mapping[str, object]) -> CraftRubric:
        """Load a craft rubric from a mapping or a YAML path."""


class InMemoryRenderBackend:
    """Deterministic receipt stub. Hashes the spec in memory and writes nothing."""

    def __init__(self, backend_name: str = "in-memory-stub") -> None:
        self.backend_name = backend_name

    def render(self, spec: TimelineSpec) -> RenderReceipt:
        digest = hashlib.sha256(spec.model_dump_json().encode("utf-8")).hexdigest()
        return RenderReceipt(
            backend_name=self.backend_name,
            output_relpath=f"memory/{spec.episode_id}/{spec.scene_id}.mp4",
            sha256=digest,
        )
