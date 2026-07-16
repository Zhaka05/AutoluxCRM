from sqlmodel import Relationship, SQLModel, Field, Column, DateTime
from enum import Enum
from .owner import Owner

from .carwash import CarWash

class StaffRole(str, Enum):
    MANAGER = "manager"
    EMPLOYEE = "employee"

class Staff(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    phone: str
    role: StaffRole

    carwash_id: int = Field(foreign_key="carwash.id")

    # owner: "Owner" = Relationship(
    #     back_populates="managers"
    # )