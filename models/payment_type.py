from sqlmodel import SQLModel, Field

from .carwash import CarWash

class PaymentType(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    carwash_id: int = Field(foreign_key="carwash.id")

class PaymentTypeCreate(SQLModel):
    name: str
    carwash_id: int

class PaymentTypePublic(SQLModel):
    id: int
    name: str
    carwash_id: int