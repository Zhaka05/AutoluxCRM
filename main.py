from fastapi import FastAPI, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from models import ServiceTicket

from typing import Annotated, Any
from contextlib import asynccontextmanager

SessionDep = Annotated[Session, Depends(get_session)]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")
@app.get("/")
def main(request: Request, session: SessionDep):
    tickets = session.exec(select(ServiceTicket)).all()
    return templates.TemplateResponse(request=request, name="main.html", context={"tickets": tickets})

@app.get("/create-order")
def get_create_order(
        request: Request,
):
    return templates.TemplateResponse(request=request, name="create_order.html")

@app.post("/create-order")
def post_create_order(
        request: Request,
        session: SessionDep,
        license_plate: str = Form(...),
        brand: str = Form(...),
        employee_name: str = Form(...),
        service_name: str = Form(...),
        client_phone: str = Form(...),
        comment: str = Form(...),
):
    db_service_ticket = ServiceTicket(
        license_plate=license_plate,
        brand=brand,
        service_name=service_name,
        employee_name=employee_name,
        client_phone=client_phone,
        comment=comment,
    )
    session.add(db_service_ticket)
    session.commit()
    session.refresh(db_service_ticket)

    return RedirectResponse("/orders", status_code=302)


@app.get("/orders")
def get_orders(request: Request, session: SessionDep):
    tickets = session.exec(select(ServiceTicket)).all()
    return templates.TemplateResponse(request=request, name="orders.html", context={"tickets": tickets})