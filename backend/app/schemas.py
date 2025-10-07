from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, EmailStr


# =========================
#  USER
# =========================
class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr


# =========================
#  MEAL
# =========================
class MealBase(BaseModel):
    date: date
    title: str = Field(min_length=1, max_length=200)
    calories: int = Field(ge=0)

class MealCreate(MealBase):
    """Payload za kreiranje obroka."""
    pass

class MealUpdate(BaseModel):
    """Partial update — sva polja opcionalna."""
    date: Optional[date] = None
    title: Optional[str] = None
    calories: Optional[int] = Field(default=None, ge=0)

class MealOut(MealBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
