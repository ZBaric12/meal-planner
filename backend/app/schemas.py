from datetime import date
from pydantic import BaseModel, Field, ConfigDict, EmailStr

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr

class MealBase(BaseModel):
    date: date
    title: str = Field(min_length=1, max_length=200)
    calories: int = Field(ge=0)

class MealCreate(MealBase):
    pass

class MealUpdate(BaseModel):
    # sva polja su opcionalna; ništa nije obavezno kod PUT-a
    date: date | None = None
    title: str | None = None
    calories: int | None = Field(default=None, ge=0)

class MealOut(MealBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
