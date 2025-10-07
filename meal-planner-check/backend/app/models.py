from sqlalchemy import Integer, String, Date, ForeignKey, Text, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .db import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[str] = mapped_column(server_default=func.now())
    meals = relationship("Meal", back_populates="user", cascade="all,delete")

class Meal(Base):
    __tablename__ = "meals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    meal_type: Mapped[str] = mapped_column(String(20), nullable=False)  # breakfast|lunch|dinner|snack
    date: Mapped[str] = mapped_column(Date, index=True, nullable=False)
    calories: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[str] = mapped_column(server_default=func.now())
    user = relationship("User", back_populates="meals")
