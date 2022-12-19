from typing import Callable
from typing import Type
from typing import Union

from fastapi import Form, Query, Body, Depends
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from pyfa_converter import PydanticConverter


class PyFaDepends:
    def __new__(
        cls,
        model: Type[Union[BaseModel, PydanticConverter]],
        _type: Callable[..., FieldInfo],
    ):
        return cls.generate(model=model, _type=_type)

    @classmethod
    def generate(
        cls,
        model: Type[Union[BaseModel, PydanticConverter]],
        _type: Callable[..., FieldInfo],
    ):
        obj = PydanticConverter.reformat_model_signature(model_cls=model, _type=_type)
        attr = getattr(obj, str(_type.__name__).lower())
        return Depends(attr)


class BasePyFaDepends(PyFaDepends):
    _TYPE: ...

    def __new__(cls, model_type: Type[Union[BaseModel, PydanticConverter]]):
        return super().generate(model=model_type, _type=cls._TYPE)


class BodyDepends(BasePyFaDepends):
    _TYPE = Body


class FormDepends(BasePyFaDepends):
    _TYPE = Form


class QueryDepends(BasePyFaDepends):
    _TYPE = Query
