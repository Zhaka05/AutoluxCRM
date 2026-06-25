from sqlmodel import Relationship, SQLModel, Field, Column, DateTime
from datetime import datetime

class ServiceTicketBase(SQLModel):
    license_plate: str
    brand: str
    car_body: str
    service_name: str
    employee_name: str
    client_phone: str | None = None
    comment: str | None = Field(default=None, max_length=500)

class ServiceTicket(ServiceTicketBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_datetime: datetime = Field(
        default_factory=datetime.now,
        sa_column=Column(DateTime)
    )

class ServiceTicketCreate(ServiceTicketBase):
    pass

class ServiceTicketUpdate(SQLModel):
    license_plate: str | None = None
    brand: str | None = None
    car_body: str | None = None
    service_name: str | None = None
    employee_name: str | None = None
    client_phone: str | None = None

class ServiceTicketPublic(ServiceTicketBase):
    id: int
    created_datetime: datetime

class ServiceTicketReplace(ServiceTicketBase):
    pass