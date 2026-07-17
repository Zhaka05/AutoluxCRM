from sqlmodel import Relationship, SQLModel, Field, Column, DateTime

from .owner import Owner

class CarWash(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    address: str
    manager_code_hash: str
    employee_code_hash: str

    owner_id: int = Field(foreign_key="owner.id")

    # owner: "Owner" = Relationship(
    #     back_populates="car_washes"
    # )

class CarWashCreate(SQLModel):
    name: str
    address: str
    manager_code_hash: str
    employee_code_hash: str
    owner_id: int

class CarWashPublic(SQLModel):
    name: str
    address: str
    owner_id: int