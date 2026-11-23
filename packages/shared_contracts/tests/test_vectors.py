"""Offline parity vectors: 60 valid round-trips and 60 adversarial rejects."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from shared_contracts.models import TOP_LEVEL_MODELS
from vector_factory import PARITY_MODELS, build_document

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "vectors.json"
SCHEMA = Path(__file__).resolve().parents[1] / "schema" / "contracts-v4.json"


def _load() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_fixture_matches_builder() -> None:
    assert json.loads(FIXTURE.read_text(encoding="utf-8")) == build_document()


def test_schema_file_matches_export() -> None:
    from shared_contracts.schema_export import export_contract_schemas

    assert json.loads(SCHEMA.read_text(encoding="utf-8")) == export_contract_schemas()


def test_vector_counts() -> None:
    document = _load()
    assert len(document["valid"]) == 60
    assert len(document["adversarial"]) == 60
    assert {row["model"] for row in document["valid"]} == set(PARITY_MODELS)
    assert {row["model"] for row in document["adversarial"]} == set(PARITY_MODELS)


@pytest.mark.parametrize("vector_id", [f"v{index:03d}" for index in range(1, 61)])
def test_valid_roundtrip(vector_id: str) -> None:
    vector = next(row for row in _load()["valid"] if row["id"] == vector_id)
    model = TOP_LEVEL_MODELS[vector["model"]]
    parsed = model.model_validate(vector["payload"])
    dumped = json.loads(parsed.model_dump_json())
    assert dumped == vector["canonical"]
    assert json.loads(model.model_validate(dumped).model_dump_json()) == dumped


@pytest.mark.parametrize("vector_id", [f"a{index:03d}" for index in range(1, 61)])
def test_adversarial_rejected(vector_id: str) -> None:
    vector = next(row for row in _load()["adversarial"] if row["id"] == vector_id)
    model = TOP_LEVEL_MODELS[vector["model"]]
    with pytest.raises(ValidationError):
        model.model_validate(vector["payload"])
