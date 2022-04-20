import inspect
from typing import Any
from typing import Type

from fastapi import Body
from fastapi import Form
from pydantic import BaseModel
from pydantic.fields import ModelField


class PydanticConverter:

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

    @classmethod
    def body(cls, parent_cls: Type[BaseModel]):
        new_parameters = []

        for field_name, model_field in parent_cls.__fields__.items():
            model_field: ModelField

            new_parameters.append(
                inspect.Parameter(
                    field_name,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=cls.form(field=model_field),
                    annotation=model_field.outer_type_,
                )
            )

        async def as_form_func(*args, **kwargs):
            return parent_cls(*args, **kwargs)  # noqa

        sig = inspect.signature(as_form_func)
        sig = sig.replace(parameters=new_parameters)
        as_form_func.__signature__ = sig
        setattr(cls, 'body', as_form_func)
        return cls

