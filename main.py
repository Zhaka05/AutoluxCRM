from fastapi import FastAPI, Request, Depends, Form, HTTPException, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models.service_ticket import ServiceTicket, ServiceTicketPublic, ServiceTicketCreate, ServiceTicketUpdate, ServiceTicketReplace

from typing import Annotated
from contextlib import asynccontextmanager


SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# templates = Jinja2Templates(directory="templates")
# @app.get("/")
# def main(request: Request):
#     return templates.TemplateResponse(request=request, name="main.html")

@app.post("/create-order", response_model=ServiceTicketPublic, status_code=201)
def post_create_order(
        session: SessionDep,
        ticket_form: ServiceTicketCreate,

):
    # post handler to save a new ticket

    db_service_ticket = ServiceTicket(**ticket_form.model_dump())

    session.add(db_service_ticket)
    session.commit()
    session.refresh(db_service_ticket)

    return db_service_ticket

@app.patch("/edit/{order_id}")
def edit_order(order_id: int, session: SessionDep, ticket_form: ServiceTicketUpdate):
    db_service_ticket = session.get(ServiceTicket, order_id)

    if db_service_ticket is None:
        raise HTTPException(status_code=404, detail="Service Ticket was not found")
    
    ticket_data = ticket_form.model_dump(exclude_unset=True)
    db_service_ticket.sqlmodel_update(ticket_data) # expects dictionary

    session.add(db_service_ticket)
    session.commit()
    session.refresh(db_service_ticket)

    return db_service_ticket

@app.put("/update-order/{order_id}")
def update_order(order_id: int, session: SessionDep, ticket_form: ServiceTicketReplace):
    db_service_ticket = session.get(ServiceTicket, order_id)

    if not db_service_ticket:
        raise HTTPException(status_code=404, detail="Service Ticket was not found")

    ticket_data = ticket_form.model_dump()
    db_service_ticket.sqlmodel_update(ticket_data) # update


    session.add(ticket_data)
    session.commit()
    session.refresh(db_service_ticket)
    return db_service_ticket

@app.get("/orders")
def get_orders(session: SessionDep):
    # view to list all tickets
    tickets = session.exec(select(ServiceTicket)).all()
    return tickets

app.mount("/static", StaticFiles(directory="."), name="static")
