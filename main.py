from fastapi import FastAPI, Request, Depends, Form, HTTPException, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import ServiceTicket
from schemas import TicketRequestForm

from typing import Annotated
from contextlib import asynccontextmanager


SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")
@app.get("/")
def main(request: Request):
    return templates.TemplateResponse(request=request, name="main.html")

@app.get("/create-order")
def get_create_order(
        request: Request,
):
    return templates.TemplateResponse(request=request, name="create_order.html", ticket=None)

@app.post("/create-order")
def post_create_order(
        request: Request,
        session: SessionDep,
        ticket_form: Annotated[TicketRequestForm, Form()],
):
    # post handler to save a new ticket
    db_service_ticket = ServiceTicket(
        license_plate=ticket_form.license_plate,
        brand=ticket_form.brand,
        car_body=ticket_form.car_body,
        service_name=ticket_form.service_name,
        employee_name=ticket_form.employee_name,
        client_phone=ticket_form.client_phone,
        comment=ticket_form.comment,
    )
    session.add(db_service_ticket)
    session.commit()
    session.refresh(db_service_ticket)

    return RedirectResponse("/orders", status_code=302)

@app.get("/edit/{order_id}")
def get_order(request: Request, order_id: int, session: SessionDep):
    db_service_ticket = session.get(ServiceTicket, order_id)
    if db_service_ticket is None:
        raise HTTPException(status_code=404)
    return templates.TemplateResponse(request=request, name="create_order.html", ticket=db_service_ticket)

@app.post("/update-order/{order_id}")
def post_update_order(request: Request, order_id: int, session: SessionDep, ticket_form: Annotated[TicketRequestForm, Form()]):
    db_service_ticket = session.get(ServiceTicket, order_id)
    db_service_ticket.license_plate = ticket_form.license_plate
    db_service_ticket.brand= ticket_form.brand
    db_service_ticket.car_body= ticket_form.car_body
    db_service_ticket.service_name= ticket_form.service_name
    db_service_ticket.employee_name= ticket_form.employee_name
    db_service_ticket.client_phone= ticket_form.client_phone
    db_service_ticket.comment= ticket_form.comment
    session.commit()
    session.refresh(db_service_ticket)
    return Response(status_code=200)

@app.get("/orders")
def get_orders(request: Request, session: SessionDep):
    # view to list all tickets
    tickets = session.exec(select(ServiceTicket)).all()
    return templates.TemplateResponse(request=request, name="orders.html", context={"tickets": tickets})



app.mount("/static", StaticFiles(directory="."), name="static")
