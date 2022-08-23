from typing import Callable
from typing import Type
from fastapi import Form, Query, Body, Depends
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from pyfa_converter import PydanticConverter


class PyFaDepends:
    def __new__(
        cls,
        model: Type[BaseModel | PydanticConverter],
        _type: Callable[..., FieldInfo],
    ):
        return cls.generate(model=model, _type=_type)

    @classmethod
    def generate(
        cls,
        model: Type[BaseModel | PydanticConverter],
        _type: Callable[..., FieldInfo],
    ):
        obj = PydanticConverter.reformat_model_signature(
            model_cls=model, _type=_type
        )
        attr = getattr(obj, str(_type.__name__).lower())
        return Depends(attr)


class BodyDepends(PyFaDepends):
    _TYPE = Body

    def __new__(cls, model_type: Type[BaseModel | PydanticConverter]):
        return super().generate(model=model_type, _type=cls._TYPE)


class FormDepends(PyFaDepends):
    _TYPE = Form

    def __new__(cls, model_type: Type[BaseModel | PydanticConverter]):
        return super().generate(model=model_type, _type=cls._TYPE)


class QueryDepends(PyFaDepends):
    _TYPE = Query

    def __new__(cls, model_type: Type[BaseModel | PydanticConverter]):
        return super().generate(model=model_type, _type=cls._TYPE)
