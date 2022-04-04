from fastapi import Depends
from pyfa_converter import PydanticConverter


class FormBody:
    def __new__(cls):
        return Depends(PydanticConverter.body)
