"""
Mock Tickets Generation and Add to Database for quick and easy testing purposes
Uses real prod database for now

Command Line Receives two inputs, lowercase:
- add
- remove: deletes all entries from table ServiceTicket

If "add" chosen, specify how much in integer value
"""


from faker_vehicle import VehicleProvider
from fastapi import Depends
from typing import Annotated

from faker import Faker

from main import get_session
from database import Session
from schemas import TicketRequestForm
from models import ServiceTicket

SessionDep = Annotated[Session, Depends(get_session)]

faker_obj = Faker()
faker_obj.add_provider(VehicleProvider)


def generate_mock_ticket() -> dict:
    return {
        'license_plate': faker_obj.license_plate(),
        'brand': faker_obj.vehicle_make(),
        'car_body': faker_obj.vehicle_category(),
        'employee_name': faker_obj.name(),
        'service_name': faker_obj.word().title() + ' Service',
        'client_phone': faker_obj.phone_number(),
        'comment': faker_obj.sentence()
    }


def generate_tickets(num: int) -> list[TicketRequestForm]:
    res = []
    for i in range(num):
        ticket_data = generate_mock_ticket()

        ticket = TicketRequestForm(**ticket_data)
        res.append(ticket)
    return res


def add_mock_tickets_to_db(tickets: list[TicketRequestForm]):
    session = next(get_session())

    try:
        for ticket in tickets:
            db_ticket = ServiceTicket(**ticket.model_dump())
            session.add(db_ticket)
        session.commit()
        print(f"✓ Successfully added {len(tickets)} tickets to the database")
    except Exception as e:
        session.rollback()
        print(f"✗ Error adding tickets: {e}")
    finally:
        session.close()


def remove_mock_tickets_from_db():
    session = next(get_session())

    try:
        deleted_count = session.execute(ServiceTicket).delete()
        session.commit()
        print(f"✓ Successfully removed {deleted_count} tickets from the database")
    except Exception as e:
        session.rollback()
        print(f"✗ Error removing tickets: {e}")
    finally:
        session.close()

action_input = input().strip()

if action_input == "add":
    number_input = int(input().strip())
    tickets = generate_tickets(number_input)
    add_mock_tickets_to_db(tickets)

elif action_input == "remove":
    remove_mock_tickets_from_db()