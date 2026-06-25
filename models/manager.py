from sqlmodel import Relationship, SQLModel, Field, Column, DateTime

from .owner import Owner
from .carwash import CarWash

class Manager(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    phone: str

    owner_id: int = Field(foreign_key="owner.id")
    car_wash_id: int = Field(foreign_key="carwash.id")

    owner: "Owner" = Relationship(
        back_populates="managers"
    )
    
    car_wash: "CarWash" = Relationship( # forward reference, hence the "CarWash" is in strings
        back_populates="managers"
    )
