from sqlmodel import Relationship, SQLModel, Field, Column, DateTime
from typing import Optional
from datetime import datetime

class ServiceTicket(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    license_plate: str
    brand: str
    car_body: str
    service_name: str
    employee_name: str
    client_phone: str | None = None
    created_datetime: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime)
    )
    comment: Optional[str] = Field(default=None, max_length=500)

    @property
    def created_time(self):
        return self.created_datetime.strftime("%H:%M")

class Owner(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    phone: str
    email: str
    password: str

    car_washes: list["CarWash"] = Relationship(
        back_populates="owner"
    )

    managers: list["Manager"] = Relationship(
        back_populates="owner"
    )

#

# owner.car_washes.append(wash)

# will automatically set:

# wash.owner

# to that owner.
class CarWash(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    owner_id: int = Field(foreign_key="owner.id")

    owner: "Owner" = Relationship(
        back_populates="car_washes"
    )

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

