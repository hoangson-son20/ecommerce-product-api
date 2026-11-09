
from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)


class ProductCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    price: Decimal = Field(gt=0, max_digits=12, decimal_places=2)
    stock_quantity: int = Field(ge=0)
    category_id: int = Field(gt=0)
    seller_id: int = Field(gt=0)
    is_active: bool = True

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Product name cannot be empty.")

        return value


    @field_validator("description")
    @classmethod
    def strip_description(cls, value: str | None) -> str | None:
        if value is not None:
            return value.strip()

        return value


class ProductUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=2000)
    price: Decimal | None = Field(default=None, gt=0, max_digits=12, decimal_places=2,)
    stock_quantity: int | None = Field(default=None, ge=0)
    category_id: int | None = Field(default=None, gt=0)
    seller_id: int | None = Field(default=None, gt=0)
    is_active: bool | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_patch_body(cls, data: object) -> object:
        if isinstance(data, dict):
            if not data:
                raise ValueError("At least one field must be provided.")

            for field in ("name", "price", "stock_quantity", "category_id", "seller_id", "is_active",):
                if field in data and data[field] is None:
                    raise ValueError(f"{field} cannot be null.")

        return data

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Product name cannot be empty.")

        return value


    @field_validator("description")
    @classmethod
    def strip_description(cls, value: str | None) -> str | None:
        if value is not None:
            return value.strip()

        return value


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    stock_quantity: int
    category_id: int
    seller_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductListResponse(BaseModel):
    items: list[ProductResponse]
    total_items: int
    page: int
    page_size: int
