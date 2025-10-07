from pydantic import BaseModel, Field, ConfigDict
from datetime import date

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str

class MealBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    meal_type: str = Field(..., pattern="^(breakfast|lunch|dinner|snack)$")
    date: date
    calories: int | None = Field(default=None, ge=0, le=5000)
    notes: str | None = Field(default=None, max_length=2000)

class MealCreate(MealBase): ...
class MealUpdate(MealBase): ...

class MealOut(MealBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
