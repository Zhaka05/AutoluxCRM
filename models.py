from sqlmodel import SQLModel, Field, Column, DateTime
from typing import Optional
from datetime import datetime

from pydantic import BaseModel

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

class TicketRequestForm(BaseModel):
    license_plate: str
    brand: str
    car_body: str
    employee_name: str
    service_name: str
    client_phone: str
    comment: str
