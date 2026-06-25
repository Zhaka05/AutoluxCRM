from sqlmodel import Relationship, SQLModel, Field, Column, DateTime

from .manager import Manager
from .carwash import CarWash

class Owner(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    phone: str
    email: str
    password_hash: str

    car_washes: list["CarWash"] = Relationship(
        back_populates="owner"
    )

    managers: list["Manager"] = Relationship(
        back_populates="owner"
    )
