from fastapi import HTTPException, APIRouter, Response, status
from sqlmodel import select

from typing import List

from models import service_ticket
from dependencies import SessionDep

router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"],
)


@router.get("/", response_model=List[service_ticket.ServiceTicketPublic])
def get_tickets(session: SessionDep):
    # view to list all tickets
    statement = select(service_ticket.ServiceTicket)
    tickets = session.exec(statement).all()
    return tickets


@router.get("/{ticket_id}", response_model=service_ticket.ServiceTicketPublic)
def get_ticket(ticket_id: int, session: SessionDep):

    ticket = session.get(service_ticket.ServiceTicket, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=404, detail=f"ticket with id {ticket_id} was not found"
        )

    return ticket

@router.post("/scheduled", response_model=service_ticket.ScheduledTicketCreate)
def schedule_ticket(session: SessionDep, ticket_form: service_ticket.ServiceTicketCreate):
    ticket = service_ticket.ServiceTicket(**ticket_form.model_dump())

    session.add(ticket)
    session.commit()
    session.refresh(ticket)

    return ticket

@router.post("/", response_model=service_ticket.ServiceTicketPublic, status_code=201)
def post_ticket(
    session: SessionDep,
    ticket_form: service_ticket.ServiceTicketCreate,
):
    # post handler to save a new ticket

    ticket = service_ticket.ServiceTicket(**ticket_form.model_dump())

    session.add(ticket)
    session.commit()
    session.refresh(ticket)

    return ticket


@router.patch(
    "/{ticket_id}", response_model=service_ticket.ServiceTicketPublic, status_code=201
)
def edit_ticket(
    ticket_id: int, session: SessionDep, ticket_form: service_ticket.ServiceTicketUpdate
):
    ticket = session.get(service_ticket.ServiceTicket, ticket_id)

    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service Ticket was not found"
        )

    ticket_data = ticket_form.model_dump(exclude_unset=True)
    ticket.sqlmodel_update(ticket_data)  # expects dictionary

    session.add(ticket)
    session.commit()
    session.refresh(ticket)

    return ticket


@router.put(
    "/{ticket_id}", response_model=service_ticket.ServiceTicketPublic, status_code=200
)
def update_ticket(
    ticket_id: int,
    session: SessionDep,
    ticket_form: service_ticket.ServiceTicketReplace,
):
    ticket = session.get(service_ticket.ServiceTicket, ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service Ticket was not found"
        )

    ticket_data = ticket_form.model_dump()
    ticket.sqlmodel_update(ticket_data)  # update

    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket


@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int, session: SessionDep):
    ticket = session.get(service_ticket.ServiceTicket, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Not Found")

    session.delete(ticket)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
