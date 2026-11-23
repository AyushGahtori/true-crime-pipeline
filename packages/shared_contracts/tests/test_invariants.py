"""Registry shape, retired identifiers, and the absence of hardcoded prices."""

from __future__ import annotations

from pathlib import Path

from shared_contracts.deprecated import DEPRECATED_IDENTIFIERS
from shared_contracts.models import FlowJobCard, ScenePlan, TimelineSpec
from shared_contracts.motifs import CATALOG_MOTIF_NAMES, MOTIF_REGISTRY_V1, MVP_MOTIF_NAMES, motif_owner
from shared_contracts.schema_export import export_contract_schemas
from shared_contracts.version import CONTRACT_VERSION

SRC = Path(__file__).resolve().parents[1] / "src"


def test_mvp_registry_is_exactly_four_remotion_motifs() -> None:
    assert CONTRACT_VERSION == "v4"
    assert MVP_MOTIF_NAMES == (
        "StickmanStage",
        "AudioEvidenceCard",
        "RedactedDocReveal",
        "FoiaFootageFrame",
    )
    assert len(MOTIF_REGISTRY_V1) == 4
    assert "Illustrative2KPanZoom" not in MVP_MOTIF_NAMES
    assert "CrimeScenePanZoom" not in CATALOG_MOTIF_NAMES
    assert motif_owner("Illustrative2KPanZoom") == "crime_scene_2k"
    assert motif_owner("StickmanStage") == "render_catalog"
    assert "Illustrative2KPanZoom" in CATALOG_MOTIF_NAMES


def test_deprecated_identifiers_are_not_current_enums() -> None:
    banned = set(DEPRECATED_IDENTIFIERS)
    scene_modes = set(ScenePlan.model_fields["prompt_mode"].annotation.__args__)
    video_modes = set(TimelineSpec.model_fields["prompt_mode"].annotation.__args__)
    engines = set(FlowJobCard.model_fields["engine_model"].annotation.__args__)
    assert "NONE" in scene_modes
    assert video_modes == {"TEXT_TO_VIDEO", "FIRST_FRAME", "FIRST_AND_LAST_FRAME"}
    assert banned.isdisjoint(scene_modes)
    assert banned.isdisjoint(video_modes)
    assert banned.isdisjoint(engines)
    assert banned.isdisjoint(set(CATALOG_MOTIF_NAMES))
    schema_text = str(export_contract_schemas())
    for token in banned:
        assert token not in schema_text


def test_runtime_sources_do_not_hardcode_prices() -> None:
    banned_snippets = ("usd_per_second", "0.10", "800000", "10400000", "135000000")
    for path in SRC.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for snippet in banned_snippets:
            assert snippet not in text, f"{snippet} found in {path.name}"
