from __future__ import annotations

from typing import Any, Dict, List, Type, Union, get_args, get_origin

from pydantic import BaseModel, Field, create_model, field_validator


class ArgsBaseModel(BaseModel):
    """Base class for tool argument models with strict object schema."""

    model_config = {
        "extra": "forbid",
        "json_schema_extra": {"additionalProperties": False},
    }


_MODEL_CACHE: Dict[type[BaseModel], type[BaseModel]] = {}


def _convert_annotation(
    annotation: Any,
    field_name: str,
    validators: Dict[str, classmethod],
) -> Any:
    origin = get_origin(annotation)
    if origin is None:
        if isinstance(annotation, type) and issubclass(annotation, BaseModel):
            return get_args_model(annotation)
        if annotation is int:
            # Replace ints with floats and create validator to coerce to int
            @field_validator(field_name, mode="before")
            def _coerce(cls, v):
                return None if v is None else int(v)

            validators[f"coerce_{field_name}"] = _coerce
            return float
        return annotation
    if origin in (list, List):
        inner = _convert_annotation(get_args(annotation)[0], field_name, validators)
        return List[inner]
    if origin is Union:
        converted = [
            _convert_annotation(arg, field_name, validators) for arg in get_args(annotation)
        ]
        return Union[tuple(converted)]
    return annotation


def get_args_model(model_cls: Type[BaseModel]) -> Type[BaseModel]:
    """Create an Args model for the given request model."""
    if model_cls in _MODEL_CACHE:
        return _MODEL_CACHE[model_cls]

    fields: Dict[str, tuple[Any, Any]] = {}
    validators: Dict[str, classmethod] = {}

    for name, field in model_cls.model_fields.items():
        ann = _convert_annotation(field.annotation, name, validators)
        default = field.default if not field.is_required() else ...
        ge = le = None
        for meta in getattr(field, "metadata", []):
            if hasattr(meta, "ge"):
                ge = meta.ge
            if hasattr(meta, "le"):
                le = meta.le
        fields[name] = (
            ann,
            Field(
                default,
                description=getattr(field, "description", None),
                ge=ge,
                le=le,
            ),
        )

    ArgsModel = create_model(
        f"{model_cls.__name__}Args",
        __base__=ArgsBaseModel,
        __validators__=validators,
        **fields,
    )

    _MODEL_CACHE[model_cls] = ArgsModel
    return ArgsModel


from typing import Callable


def tool_with_args(
    mcp,
    request_model: Type[BaseModel] | None = None,
    **decorator_kwargs: Any,
) -> Callable:
    """Decorator to wrap MCP tools with generated Args models."""

    def decorator(func: Callable) -> Callable:
        if request_model is None:
            ArgsModel = ArgsBaseModel

            async def inner(args: ArgsModel):
                return await func()
        else:
            ArgsModel = get_args_model(request_model)

            async def inner(args: ArgsModel):
                model = request_model(**args.model_dump())
                return await func(model)

        inner.__name__ = func.__name__
        inner.__doc__ = func.__doc__
        inner.__annotations__ = {
            "args": ArgsModel,
            "return": func.__annotations__.get("return", Any),
        }
        return mcp.tool(**decorator_kwargs)(inner)

    return decorator
