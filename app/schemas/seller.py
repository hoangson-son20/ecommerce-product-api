from datetime import datetime
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator, model_validator


class SellerCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=100)
    email: EmailStr

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Seller name cannot be empty")

        return value
    


class SellerUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_not_null(cls, data: object) -> object:
        if isinstance(data, dict):
            for field in ("name", "email"):
                if field in data and data[field] is None:
                    raise ValueError(f"{field} cannot be null")

            if not data:
                raise ValueError("At least on field must be provided")

        return data

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()

            if not value: 
                raise ValueError("Seller name cannot be empty")

        return value

    
class SellerResponse(BaseModel):
    id: int
    name: str 
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)