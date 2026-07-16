from sqlmodel import SQLModel, Field

from .carwash import CarWash

class VehicleType(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    carwash_id: int = Field(foreign_key="carwash.id")
    