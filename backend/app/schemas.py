# app/schemas.py
from __future__ import annotations  # nije nužno s Optional, ali ne smeta

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, EmailStr


# -------- User --------
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr


# -------- Meals --------
class MealBase(BaseModel):
    date: date
    title: str = Field(min_length=1, max_length=200)
    calories: int = Field(ge=0)


class MealCreate(MealBase):
    pass


class MealUpdate(BaseModel):
    # koristimo Optional umjesto "date | None" da izbjegnemo probleme s evaluacijom tipova
    date: Optional[date] = None
    title: Optional[str] = None
    calories: Optional[int] = Field(default=None, ge=0)


class MealOut(MealBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
