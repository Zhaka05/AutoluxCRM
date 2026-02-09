from sqlmodel import SQLModel, Field
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
    time: datetime = Field(default_factory=datetime.now)
    comment: Optional[str] = Field(default=None, max_length=500)

class TicketRequestForm(BaseModel):
    license_plate: str
    brand: str
    car_body: str
    employee_name: str
    service_name: str
    client_phone: str
    comment: str
