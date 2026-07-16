from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime

from .carwash import CarWash
from .staff import Staff

class ServiceTicketBase(SQLModel):
    license_plate: str
    brand: str
    car_body: str | None = None # these became None because scheduled does not require them
    service_name: str | None = None
    employee_name: str | None = None
    client_phone: str | None = None
    comment: str | None = Field(default=None, max_length=500)
    scheduled_at: datetime | None = Field(default=None, index=True)
    
class ServiceTicket(ServiceTicketBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_datetime: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )
    carwash_id: int = Field(foreign_key="carwash.id")
    created_by_staff_id: int = Field(foreign_key="staff.id")

class ServiceTicketCreate(ServiceTicketBase):
    pass


class ScheduledTicketCreate(SQLModel):
    license_plate: str
    brand: str
    scheduled_at: datetime
    comment: str | None = Field(default=None, max_length=500)

class ServiceTicketUpdate(SQLModel):
    license_plate: str | None = None
    brand: str | None = None
    car_body: str | None = None
    service_name: str | None = None
    employee_name: str | None = None
    client_phone: str | None = None
    scheduled_at: datetime | None = None

class ServiceTicketPublic(ServiceTicketBase):
    id: int
    created_datetime: datetime

class ServiceTicketReplace(ServiceTicketBase):
    pass