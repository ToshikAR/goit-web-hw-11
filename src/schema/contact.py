import re
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


class ContactSchema(BaseModel):
    first_name: str = Field(min_length=3, max_length=120)
    last_name: str = Field(min_length=3, max_length=120)
    email: EmailStr
    phone: Optional[str] = Field(
        None,
        min_length=3,
        max_length=15,
        description="Format +14445556677",
        example="+14445556677",
    )
    description: Optional[str] = Field(None, max_length=250)
    date_birth: Optional[date] = Field(None, description="Format YYYY-MM-DD")

    @field_validator("phone")
    def validate_phone(cls, value):
        if value:
            pattern = r"^\+?[1-9]\d{1,14}$"
            if not re.match(pattern, value):
                raise ValueError(f"Incorrect phone number {value}")
        return value


class ContactUpdateSchema(ContactSchema):
    pass


class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    description: Optional[str] = None
    date_birth: date
    last_visit: datetime
    created_at: datetime

    class Config:
        from_attributes = True
