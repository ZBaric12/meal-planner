# backend/app/auth.py
from datetime import datetime, timedelta, timezone
from typing import Generator

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .db import SessionLocal
from .models import User

# ------------------------------------------------------
# KONFIGURACIJA JWT-a
# ------------------------------------------------------
# ⚠️ U produkciji promijeni SECRET_KEY na neku random dugačku vrijednost
SECRET_KEY = "replace-this-with-a-long-random-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 dana

# OAuth2 shema – FastAPI će znati da je token endpoint na /auth/login
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ------------------------------------------------------
# HASHIRANJE LOZINKI: pbkdf2_sha256 (nema 72-byte limita)
# ------------------------------------------------------
pwd_ctx = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_pw(pw: str) -> str:
    """Vrati hash lozinke."""
    return pwd_ctx.hash(pw)


def verify_pw(pw: str, hashed: str) -> bool:
    """Provjeri lozinku u odnosu na spremljeni hash."""
    return pwd_ctx.verify(pw, hashed)


# ------------------------------------------------------
# DB session dependency
# ------------------------------------------------------
def get_db() -> Generator[Session, None, None]:
    """Daj SQLAlchemy session, zatvori nakon korištenja."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ------------------------------------------------------
# JWT helperi
# ------------------------------------------------------
def create_access_token(email: str) -> str:
    """Kreiraj JWT s 'sub' = email i rokom isteka."""
    to_encode = {
        "sub": email,
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.now(tz=timezone.utc),
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2),
) -> User:
    """Vrati trenutno prijavljenog korisnika iz JWT-a ili 401."""
    cred_exc = HTTPException(status_code=401, detail="Neispravan token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str | None = payload.get("sub")
        if not email:
            raise cred_exc
    except JWTError:
        raise cred_exc

    user = db.query(User).filter_by(email=email).first()
    if not user:
        raise cred_exc
    return user
