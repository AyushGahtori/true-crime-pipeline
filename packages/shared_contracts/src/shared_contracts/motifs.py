"""Authoritative motif catalog. MOTIF_REGISTRY_V1 is the 4-motif Remotion MVP only."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from shared_contracts.base import ContractModel

OwnerPackage = Literal["render_catalog", "crime_scene_2k", "flow_adapter"]

# SQL motif_registry insert order. Illustrative2KPanZoom is crime_scene_2k, not Remotion.
_CATALOG_ROWS: tuple[tuple[str, OwnerPackage, bool], ...] = (
    ("StickmanStage", "render_catalog", True),
    ("AudioEvidenceCard", "render_catalog", True),
    ("RedactedDocReveal", "render_catalog", True),
    ("FoiaFootageFrame", "render_catalog", True),
    ("TimelineScrubber", "render_catalog", False),
    ("AnimatedMapRoute", "render_catalog", False),
    ("CellTowerTriangulation", "render_catalog", False),
    ("SplitScreenComparison", "render_catalog", False),
    ("CaseBoardSpine", "render_catalog", False),
    ("QuotePullout", "render_catalog", False),
    ("EvidenceGridMatrix", "render_catalog", False),
    ("ChapterSlateTransition", "render_catalog", False),
    ("Illustrative2KPanZoom", "crime_scene_2k", False),
    ("HeroVideoBridge", "flow_adapter", False),
)

MvpMotif = Literal[
    "StickmanStage",
    "AudioEvidenceCard",
    "RedactedDocReveal",
    "FoiaFootageFrame",
]

CatalogMotif = Literal[
    "StickmanStage",
    "AudioEvidenceCard",
    "RedactedDocReveal",
    "FoiaFootageFrame",
    "TimelineScrubber",
    "AnimatedMapRoute",
    "CellTowerTriangulation",
    "SplitScreenComparison",
    "CaseBoardSpine",
    "QuotePullout",
    "EvidenceGridMatrix",
    "ChapterSlateTransition",
    "Illustrative2KPanZoom",
    "HeroVideoBridge",
]


class MotifRegistryEntry(ContractModel):
    motif_component: str = Field(min_length=1)
    owner_package: OwnerPackage
    is_mvp_4: bool


MOTIF_CATALOG: tuple[MotifRegistryEntry, ...] = tuple(
    MotifRegistryEntry(
        motif_component=name,
        owner_package=owner,
        is_mvp_4=is_mvp,
    )
    for name, owner, is_mvp in _CATALOG_ROWS
)

MOTIF_REGISTRY_V1: tuple[MotifRegistryEntry, ...] = tuple(
    entry for entry in MOTIF_CATALOG if entry.is_mvp_4
)

MVP_MOTIF_NAMES: tuple[str, ...] = tuple(entry.motif_component for entry in MOTIF_REGISTRY_V1)
CATALOG_MOTIF_NAMES: tuple[str, ...] = tuple(entry.motif_component for entry in MOTIF_CATALOG)


def _assert_registry() -> None:
    expected = (
        "StickmanStage",
        "AudioEvidenceCard",
        "RedactedDocReveal",
        "FoiaFootageFrame",
    )
    if MVP_MOTIF_NAMES != expected or len(MOTIF_REGISTRY_V1) != 4:
        raise RuntimeError("MOTIF_REGISTRY_V1 must be exactly the four Remotion MVP motifs")
    if any(entry.owner_package != "render_catalog" for entry in MOTIF_REGISTRY_V1):
        raise RuntimeError("MOTIF_REGISTRY_V1 motifs are owned by render_catalog")
    if "Illustrative2KPanZoom" in MVP_MOTIF_NAMES:
        raise RuntimeError("Illustrative2KPanZoom is not a Remotion motif")
    if "CrimeScenePanZoom" in CATALOG_MOTIF_NAMES:
        raise RuntimeError("CrimeScenePanZoom is a retired identifier")


_assert_registry()


def motif_owner(motif_component: str) -> OwnerPackage:
    for entry in MOTIF_CATALOG:
        if entry.motif_component == motif_component:
            return entry.owner_package
    raise KeyError(motif_component)
