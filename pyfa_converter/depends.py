from typing import Type
from fastapi import Depends
from pydantic import BaseModel

from pyfa_converter import PydanticConverter


class FormBody:
    def __new__(cls, model_type: Type[BaseModel | PydanticConverter]):
        return Depends(model_type.body)


class QueryBody:
    def __new__(cls, model_type: Type[BaseModel | PydanticConverter]):
        return Depends(model_type.query)
