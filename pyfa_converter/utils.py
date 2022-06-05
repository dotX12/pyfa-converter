import inspect
from typing import Any
from typing import Callable
from typing import List
from typing import Type
from typing import Union

from fastapi import Body
from fastapi import Depends
from fastapi import Form
from fastapi import Query
from pydantic import BaseModel
from pydantic.fields import ModelField


class PydanticConverterUtils:
    @classmethod
    def form(cls, field: ModelField) -> Body:
        if field.required is True:
            return cls.__fill_params(param=Form, model_field=field, default=...)
        return cls.__fill_params(param=Form, model_field=field, default=field.default)

    @classmethod
    def query(cls, field: ModelField) -> Body:
        if field.required is True:
            return cls.__fill_params(param=Query, model_field=field, default=...)
        return cls.__fill_params(param=Query, model_field=field, default=field.default)

    @classmethod
    def __fill_params(
        cls, param: Union[Form, Query], model_field: ModelField, default: Any
    ):
        return param(
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

    @classmethod
    def override_signature_parameters(
        cls, model: Type[BaseModel], param_maker: Callable[[ModelField], Any]
    ):
        return [
            inspect.Parameter(
                field.alias,
                inspect.Parameter.POSITIONAL_ONLY,
                default=param_maker(field),
                annotation=field.outer_type_,
            )
            for field in model.__fields__.values()
        ]


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
                return Depends(field.type_.body)  # noqa
            else:
                return PydanticConverterUtils.form(field=field)

        new_params = PydanticConverterUtils.override_signature_parameters(
            model=cls, param_maker=make_form_parameter
        )

        async def _as_form(**data):
            return cls(**data)

        sig = inspect.signature(_as_form)
        sig = sig.replace(parameters=new_params)
        _as_form.__signature__ = sig
        setattr(cls, "body", _as_form)
        return cls

    @staticmethod
    def query(cls: Type[BaseModel]) -> Type[BaseModel]:
        """
        Adds an `query` class method to decorated models. The `query` class
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
                Either the result of `Query`, if the field is not a sub-model, or
                the result of `Depends` if it is.

            """
            if issubclass(field.type_, BaseModel):
                # This is a sub-model.
                assert hasattr(field.type_, "query"), (
                    f"Sub-model class for {field.name} field must be decorated with"
                    f" `as_form` too."
                )
                return Depends(field.type_.query)  # noqa
            else:
                return PydanticConverterUtils.query(field=field)

        new_params = PydanticConverterUtils.override_signature_parameters(
            model=cls, param_maker=make_form_parameter
        )

        async def _as_form(**data):
            return cls(**data)

        sig = inspect.signature(_as_form)
        sig = sig.replace(parameters=new_params)
        _as_form.__signature__ = sig
        setattr(cls, "query", _as_form)
        return cls
