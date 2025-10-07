from datetime import date
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import User, Meal
from .schemas import UserOut, MealOut, MealCreate, MealUpdate
from .auth import get_current_user, create_access_token, hash_pw, verify_pw

# Kreiraj tablice ako ne postoje
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meal Planner API")

# CORS – konkretni origini (bez regexa)
ALLOWED_ORIGINS = ["http://localhost:4200", "http://127.0.0.1:4200"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    return {"ok": True}

# ---------- AUTH ----------
@app.post("/auth/register", status_code=201)
def register(payload: dict, db: Session = Depends(get_db)):
    email = payload.get("email")
    password = payload.get("password")
    if not email or not password:
        raise HTTPException(400, "Email i lozinka su obavezni")

    if db.query(User).filter_by(email=email).first():
        raise HTTPException(400, "Korisnik već postoji")

    user = User(email=email, password_hash=hash_pw(password))
    db.add(user)
    db.commit()
    return {"message": "OK"}

@app.post("/auth/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter_by(email=form.username).first()
    if not user or not verify_pw(form.password, user.password_hash):
        raise HTTPException(400, "Pogrešan email ili lozinka")

    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me", response_model=UserOut)
def me(current=Depends(get_current_user)):
    return current

# ---------- MEALS ----------

def _parse_iso(d: str | None) -> date | None:
    if not d:
        return None
    try:
        return date.fromisoformat(d)
    except ValueError:
        raise HTTPException(400, "Neispravan format datuma. Očekivano YYYY-MM-DD")

@app.get("/meals", response_model=list[MealOut])
def list_meals(
    from_: str | None = Query(None, alias="from_"),
    to: str | None = None,
    db: Session = Depends(get_db),
    current=Depends(get_current_user),
):
    start = _parse_iso(from_)
    end = _parse_iso(to)

    q = db.query(Meal).filter(Meal.user_id == current.id)
    if start:
        q = q.filter(Meal.date >= start)
    if end:
        q = q.filter(Meal.date <= end)
    return q.order_by(Meal.date.asc()).all()

@app.post("/meals", response_model=MealOut, status_code=201)
def create_meal(
    data: MealCreate,
    db: Session = Depends(get_db),
    current=Depends(get_current_user),
):
    meal = Meal(user_id=current.id, **data.model_dump())
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return meal

def _get_owned_meal(db: Session, meal_id: int, user_id: int) -> Meal:
    meal = (
        db.query(Meal)
        .filter(Meal.id == meal_id, Meal.user_id == user_id)
        .first()
    )
    if not meal:
        raise HTTPException(status_code=404, detail="Nije pronađeno")
    return meal

@app.get("/meals/{meal_id}", response_model=MealOut)
def get_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    current=Depends(get_current_user),
):
    return _get_owned_meal(db, meal_id, current.id)

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


@app.delete("/meals/{meal_id}", status_code=204)
def delete_meal(
    meal_id: int,
    db: Session = Depends(get_db),
    current=Depends(get_current_user),
):
    meal = _get_owned_meal(db, meal_id, current.id)
    db.delete(meal)
    db.commit()
    return
