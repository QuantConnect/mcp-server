from __future__ import annotations

from pydantic import BaseModel

from settings import get_settings


def add_code_source_id(model: BaseModel) -> BaseModel:
    """Attach the configured agent identifier to the request model."""

    agent_name = get_settings().agent_name
    # Using model_copy avoids mutating the caller's instance.
    return model.model_copy(update={"codeSourceId": agent_name})
