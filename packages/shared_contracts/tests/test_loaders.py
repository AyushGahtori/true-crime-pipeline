"""Provider and craft loaders accept a dict or a path. No root file is required."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from shared_contracts.loaders import RegistrySourceError, YamlCraftRubricLoader, YamlProviderRegistryLoader
from shared_contracts.models import TimelineSpec
from shared_contracts.ports import CraftRubricLoader, InMemoryRenderBackend, ProviderRegistryLoader, RenderBackendPort

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_provider_loader_path_and_dict_roundtrip() -> None:
    loader = YamlProviderRegistryLoader()
    assert isinstance(loader, ProviderRegistryLoader)
    path = FIXTURES / "providers.yaml"
    from_path = loader.load(path)
    from_dict = loader.load(yaml.safe_load(path.read_text(encoding="utf-8")))
    assert from_path.model_dump() == from_dict.model_dump()
    assert from_path.providers["fixture_video"].model_id == "fixture-video-model"
    assert from_path.providers["fixture_video"].pricing["usd_per_second"] == pytest.approx(0.01)
    missing = path.parent / "does-not-exist.yaml"
    with pytest.raises(RegistrySourceError):
        loader.load(missing)


def test_provider_loader_rejects_extra_fields() -> None:
    payload = yaml.safe_load((FIXTURES / "providers.yaml").read_text(encoding="utf-8"))
    payload["providers"]["fixture_video"]["hardcoded_price_table"] = True
    with pytest.raises(Exception):
        YamlProviderRegistryLoader().load(payload)


def test_craft_rubric_loader_and_line_cap(tmp_path: Path) -> None:
    loader = YamlCraftRubricLoader()
    assert isinstance(loader, CraftRubricLoader)
    rubric = loader.load(FIXTURES / "craft_rubric.yaml")
    assert rubric.rubric_id == "craft_rubric_v4"
    assert len(rubric.principles) == 4
    too_long = tmp_path / "craft_rubric.yaml"
    body = (FIXTURES / "craft_rubric.yaml").read_text(encoding="utf-8").splitlines()
    body.extend(["# pad"] * 200)
    too_long.write_text("\n".join(body) + "\n", encoding="utf-8")
    assert len(too_long.read_text(encoding="utf-8").splitlines()) > 150
    with pytest.raises(RegistrySourceError):
        loader.load(too_long)


def test_render_backend_is_in_memory() -> None:
    spec = TimelineSpec.model_validate(
        {
            "episode_id": "ep_1",
            "scene_id": "scene_1",
            "scene_plan_id": "plan_1",
            "motif_component": "StickmanStage",
            "prompt_mode": "TEXT_TO_VIDEO",
            "duration_ms": 4000,
        }
    )
    backend = InMemoryRenderBackend()
    assert isinstance(backend, RenderBackendPort)
    receipt = backend.render(spec)
    assert receipt.fps == 30
    assert receipt.sha256
    assert receipt.output_relpath.startswith("memory/")
