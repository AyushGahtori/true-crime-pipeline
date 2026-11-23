"""JSON Schema export for the frozen v4 models."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from shared_contracts.models import TOP_LEVEL_MODELS
from shared_contracts.version import CONTRACT_VERSION


def export_contract_schemas() -> dict[str, Any]:
    return {
        "contract_version": CONTRACT_VERSION,
        "schemas": {name: model.model_json_schema() for name, model in TOP_LEVEL_MODELS.items()},
    }


def write_contract_schemas(path: str | Path) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(export_contract_schemas(), indent=2) + "\n", encoding="utf-8")
