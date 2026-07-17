from sqlmodel import SQLModel, Field

from .carwash import CarWash

class Service(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: float
    carwash_id: int = Field(foreign_key="carwash.id")

class ServiceCreate(SQLModel):
    name: str
    price: float
    carwash_id: int

class ServicePublic(SQLModel):
    id: int
    name: str
    price: float
    carwash_id: int