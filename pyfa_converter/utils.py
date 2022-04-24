import inspect
from typing import Any
from typing import Type

from fastapi import Body
from fastapi import Depends
from fastapi import Form
from pydantic import BaseModel
from pydantic.fields import ModelField


class PydanticConverterUtils:
    @classmethod
    def form(cls, field: ModelField) -> Body:
        if field.required is True:
            return cls.__form(model_field=field, default=...)
        return cls.__form(model_field=field, default=field.default)

    @classmethod
    def __form(cls, model_field: ModelField, default: Any):
        return Form(
            default=default or None,
            alias=model_field.alias or None,
            title=model_field.field_info.title or None,
            description=model_field.field_info.description or None,
            gt=model_field.field_info.gt or None,
            ge=model_field.field_info.ge or None,
            lt=model_field.field_info.lt or None,
            le=model_field.field_info.le or None,
            min_length=model_field.field_info.min_length or None,
            max_length=model_field.field_info.max_length or None,
            regex=model_field.field_info.regex or None,
        )


class PydanticConverter:

    @staticmethod
    def body(cls: Type[BaseModel]) -> Type[BaseModel]:
        """
        Adds an `body` class method to decorated models. The `body` class
        method can be used with `FastAPI` endpoints.

        Args:
            cls: The model class to decorate.

        Returns:
            The decorated class.
        """

        def make_form_parameter(field: ModelField) -> Any:
            """
            Converts a field from a `Pydantic` model to the appropriate `FastAPI`
            parameter type.

            Args:
                field: The field to convert.

            Returns:
                Either the result of `Form`, if the field is not a sub-model, or
                the result of `Depends` if it is.

            """
            if issubclass(field.type_, BaseModel):
                # This is a sub-model.
                assert hasattr(field.type_, "body"), (
                    f"Sub-model class for {field.name} field must be decorated with"
                    f" `as_form` too."
                )
                return Depends(field.type_.body) # noqa
            else:
                return PydanticConverterUtils.form(field=field)

        new_params = [
            inspect.Parameter(
                field.alias,
                inspect.Parameter.POSITIONAL_ONLY,
                default=make_form_parameter(field),
            )
            for field in cls.__fields__.values()
        ]

        async def _as_form(**data):
            return cls(**data)

        sig = inspect.signature(_as_form)
        sig = sig.replace(parameters=new_params)
        _as_form.__signature__ = sig
        setattr(cls, "body", _as_form)
        return cls

