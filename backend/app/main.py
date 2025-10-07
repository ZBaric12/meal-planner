from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import User, Meal
from .schemas import UserOut, MealOut, MealCreate, MealUpdate
from .auth import get_current_user, create_access_token, hash_pw, verify_pw

# kreiraj tablice ako ne postoje
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Meal Planner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[r"http://localhost:4200", r"http://127\.0\.0\.1:4200"],
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
    email = payload.get("email"); password = payload.get("password")
    if not email or not password:
        raise HTTPException(400, "Email i lozinka su obavezni")
    if db.query(User).filter_by(email=email).first():
        raise HTTPException(400, "Korisnik već postoji")
    user = User(email=email, password_hash=hash_pw(password))
    db.add(user); db.commit()
    return {"message": "OK"}

@app.post("/auth/login")
def login(form: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=form.username).first()
    if not user or not verify_pw(form.password, user.password_hash):
        raise HTTPException(400, "Pogrešan email ili lozinka")
    token = create_access_token(user.email)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/me", response_model=UserOut)
def me(current=Depends(get_current_user)):
    return current

# ---------- MEALS ----------
@app.get("/meals", response_model=list[MealOut])
def list_meals(from_: str | None = None, to: str | None = None,
               db: Session = Depends(get_db), current=Depends(get_current_user)):
    q = db.query(Meal).filter(Meal.user_id == current.id)
    if from_:
        q = q.filter(Meal.date >= from_)
    if to:
        q = q.filter(Meal.date <= to)
    return q.order_by(Meal.date.asc()).all()

@app.post("/meals", response_model=MealOut, status_code=201)
def create_meal(data: MealCreate, db: Session = Depends(get_db),
                current=Depends(get_current_user)):
    meal = Meal(user_id=current.id, **data.model_dump())
    db.add(meal); db.commit(); db.refresh(meal)
    return meal

def _get_owned_meal(db: Session, meal_id: int, user_id: int) -> Meal:
    meal = db.query(Meal).filter(Meal.id == meal_id, Meal.user_id == user_id).first()
    if not meal:
        raise HTTPException(status_code=404, detail="Nije pronađeno")
    return meal

@app.get("/meals/{meal_id}", response_model=MealOut)
def get_meal(meal_id: int, db: Session = Depends(get_db),
             current=Depends(get_current_user)):
    return _get_owned_meal(db, meal_id, current.id)

@app.put("/meals/{meal_id}", response_model=MealOut)
def update_meal(meal_id: int, data: MealUpdate, db: Session = Depends(get_db),
                current=Depends(get_current_user)):
    meal = _get_owned_meal(db, meal_id, current.id)
    for k, v in data.model_dump().items():
        setattr(meal, k, v)
    db.commit(); db.refresh(meal)
    return meal

@app.delete("/meals/{meal_id}", status_code=204)
def delete_meal(meal_id: int, db: Session = Depends(get_db),
                current=Depends(get_current_user)):
    meal = _get_owned_meal(db, meal_id, current.id)
    db.delete(meal); db.commit()
    return
