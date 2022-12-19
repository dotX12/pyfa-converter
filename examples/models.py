from datetime import datetime
from decimal import Decimal
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator


class PostContractJSONSchema(BaseModel):
    title: str = Field(..., description="Description title")
    date: Optional[datetime] = Field(
        None, description="Example: 2021-12-14T09:56:31.056Z"
    )
    amount: Optional[Decimal] = Field(None, description="Description amount")
    unit_price: Optional[Decimal] = Field(None, description="Description unit_price")

    @validator("date", each_item=True)
    def date_validator(cls, v: datetime):
        return v.date()


class PostContractSmallJSONSchema(BaseModel):
    title: str = Field(..., description="Description title")
    date: Optional[datetime] = Field(
        None, description="Example: 2021-12-14T09:56:31.056Z"
    )


class PostContractBodySchema(PostContractJSONSchema):
    pass


class PostContractSmallBodySchema(PostContractSmallJSONSchema):
    pass


class PostContractSmallDoubleBodySchema(BaseModel):
    id: Optional[int] = Field(None, description="gwa")
    title: Optional[str] = Field(None)
    data: Optional[List[int]]


class PostContractSmallDoubleQuerySchema(BaseModel):
    id: Optional[int] = Field(None, description="gwa")
    title: Optional[str] = Field(None)
    data: Optional[List[int]] = Field(default=[1, 2, 3])


class ExampleSchemaForHeader(BaseModel):
    strange_header: Optional[str] = Field(None, convert_underscores=True)
    query: str = Field(...)
    form: str = Field(...)
    body: str = Field(...)


class PostSchemaIntegerGE(BaseModel):
    id: int = Field(..., description="gwa", ge=10)
    title: Optional[str] = Field(None)
    data: Optional[List[int]]
