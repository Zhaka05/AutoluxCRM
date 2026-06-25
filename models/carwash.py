from sqlmodel import Relationship, SQLModel, Field, Column, DateTime

from .owner import Owner

class CarWash(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    owner_id: int = Field(foreign_key="owner.id")

    owner: "Owner" = Relationship(
        back_populates="car_washes"
    )
