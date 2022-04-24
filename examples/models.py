from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

from pyfa_converter import PydanticConverter


class PostContractJSONSchema(BaseModel):
    title: str = Field(..., description="Description title")
    date: Optional[datetime] = Field(
        None, description="Example: 2021-12-14T09:56:31.056Z"
    )
    amount: Optional[Decimal] = Field(None, description="Description amount")
    unit_price: Optional[Decimal] = Field(None, description="Description unit_price")

    @validator('date', each_item=True)
    def date_validator(cls, v: datetime):
        return v.date()


class PostContractSmallJSONSchema(BaseModel):
    title: str = Field(..., description="Description title")
    date: Optional[datetime] = Field(
        None, description="Example: 2021-12-14T09:56:31.056Z"
    )


@PydanticConverter.body
class PostContractBodySchema(PostContractJSONSchema):
    pass


@PydanticConverter.body
class PostContractSmallBodySchema(PostContractSmallJSONSchema):
    pass


@PydanticConverter.body
class PostContractSmallDoubleBodySchema(BaseModel):
    id: Optional[int] = Field(None, description='gwa')
    title: Optional[str] = Field(None)
