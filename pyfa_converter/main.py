import inspect
from typing import Any, List
from typing import Callable
from typing import Type
from typing import Union
from warnings import warn

from fastapi import Body, Query
from fastapi import Depends
from pydantic import BaseModel
from pydantic.fields import ModelField, FieldInfo
from pyfa_converter.utils.deprecation import deprecated
from pyfa_converter.utils.deprecation_message import DEPRECATION_MESSAGE


class PydanticConverterUtils:
    @classmethod
    def param_maker(
        cls, field: ModelField, _type: Callable[..., FieldInfo]
    ) -> FieldInfo:
        if field.required is True:
            return cls.__fill_params(param=_type, model_field=field, default=...)
        return cls.__fill_params(param=_type, model_field=field, default=field.default)

    @classmethod
    def __fill_params(
        cls, param: Callable[..., FieldInfo], model_field: ModelField, default: Any
    ) -> FieldInfo:
        return param(
            default=default or None,
            alias=model_field.field_info.alias or None,
            title=model_field.field_info.title or None,
            description=model_field.field_info.description or None,
            gt=model_field.field_info.gt or None,
            ge=model_field.field_info.ge or None,
            lt=model_field.field_info.lt or None,
            le=model_field.field_info.le or None,
            min_length=model_field.field_info.min_length or None,
            max_length=model_field.field_info.max_length or None,
            regex=model_field.field_info.regex or None,
            **model_field.field_info.extra,
        )

    @classmethod
    def override_signature_parameters(
        cls,
        model: Union[Type[BaseModel], Type["PydanticConverter"]],
        param_maker: Callable[[ModelField], Any],
    ) -> List[inspect.Parameter]:
        return [
            inspect.Parameter(
                name=field.alias,
                kind=inspect.Parameter.POSITIONAL_ONLY,
                default=param_maker(field),
                annotation=field.outer_type_,
            )
            for field in model.__fields__.values()
        ]


class PydanticConverter(PydanticConverterUtils):
    @classmethod
    def reformat_model_signature(
        cls,
        model_cls: Union[Type[BaseModel], Type["PydanticConverter"]],
        _type: Any,
    ) -> Union[Type[BaseModel], Type["PydanticConverter"]]:
        """
        Adds an `query` class method to decorated models. The `query` class
        method can be used with `FastAPI` endpoints.

        Args:
            model_cls: The model class to decorate.
            _type: literal query, form, body, etc...

        Returns:
            The decorated class.
        """
        _type_var_name = str(_type.__name__).lower()

        def make_form_parameter(field: ModelField) -> Any:
            """
            Converts a field from a `Pydantic` model to the appropriate `FastAPI`
            parameter type.

            Args:
                field: The field to convert.

            Returns:
                Either the result of `Query`, if the field is not a sub-model, or
                the result of `Depends on` if it is.

            """
            if issubclass(field.type_, BaseModel):
                # This is a sub-model.
                assert hasattr(field.type_, _type_var_name), (
                    f"Sub-model class for {field.name} field must be decorated with"
                    f" `as_form` too."
                )
                attr = getattr(field.type_, _type_var_name)
                return Depends(attr)  # noqa
            else:
                return cls.param_maker(field=field, _type=_type)

        new_params = PydanticConverterUtils.override_signature_parameters(
            model=model_cls, param_maker=make_form_parameter
        )

        def _as_form(**data) -> Union[BaseModel, PydanticConverter]:
            return model_cls(**data)

        sig = inspect.signature(_as_form)
        sig = sig.replace(parameters=new_params)
        _as_form.__signature__ = sig
        setattr(model_cls, _type_var_name, _as_form)
        return model_cls

    @classmethod
    @deprecated(DEPRECATION_MESSAGE)
    def body(
        cls, model_cls: Union[Type[BaseModel], Type["PydanticConverter"]]
    ) -> Union[Type[BaseModel], Type["PydanticConverter"]]:
        warn(
            "This decorator is deprecated.\n"
            "The decorator above the model is no longer required and will be removed in the next version!\n"
            "Use:\n"
            "data: MyCustomModel = PyFaDepends(MyCustomModel, _type=Header)\n"
            "data: MyCustomModel = PyFaDepends(MyCustomModel, _type=Form)\n"
            "or\n\n"
            "data: MyCustomModel = FormDepends(MyCustomModel)\n"
            "data: MyCustomModel = QueryDepends(MyCustomModel)",
            DeprecationWarning,
            stacklevel=2,
        )

        return cls.reformat_model_signature(model_cls=model_cls, _type=Body)

    @classmethod
    @deprecated(DEPRECATION_MESSAGE)
    def query(
        cls, model_cls: Union[Type[BaseModel], Type["PydanticConverter"]]
    ) -> Union[Type[BaseModel], Type["PydanticConverter"]]:
        warn(
            "This decorator is deprecated.\n"
            "The decorator above the model is no longer required and will be removed in the next version!\n"
            "Use:\n"
            "data: MyCustomModel = PyFaDepends(MyCustomModel, _type=Header)\n"
            "data: MyCustomModel = PyFaDepends(MyCustomModel, _type=Form)\n"
            "or\n\n"
            "data: MyCustomModel = FormDepends(MyCustomModel)\n"
            "data: MyCustomModel = QueryDepends(MyCustomModel)",
            DeprecationWarning,
            stacklevel=2,
        )

        return cls.reformat_model_signature(model_cls=model_cls, _type=Query)
