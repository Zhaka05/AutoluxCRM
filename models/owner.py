from sqlmodel import Relationship, SQLModel, Field, Column, DateTime

# from .manager import Manager

class Owner(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    phone: str
    password_hash: str

    # car_washes: list["CarWash"] = Relationship(
    #     back_populates="owner"
    # )

    # managers: list["Manager"] = Relationship(
    #     back_populates="owner"
    # )

class OwnerCreate(SQLModel):
    name: str
    phone: str
    password_hash: str

class OwnerPublic(SQLModel):
    name: str
    phone: str