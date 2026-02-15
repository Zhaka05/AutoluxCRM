from pydantic import BaseModel
class TicketRequestForm(BaseModel):
    license_plate: str
    brand: str
    car_body: str
    employee_name: str
    service_name: str
    client_phone: str
    comment: str
