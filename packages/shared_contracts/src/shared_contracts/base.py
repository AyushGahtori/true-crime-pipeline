"""Shared Pydantic v2 base. extra fields and retired identifiers are rejected."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator

from shared_contracts.deprecated import reject_deprecated


class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="before")
    @classmethod
    def _reject_retired_identifiers(cls, data: Any) -> Any:
        if isinstance(data, dict):
            reject_deprecated(data)
        return data
