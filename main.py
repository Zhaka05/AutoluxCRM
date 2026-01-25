from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Session
from database import create_db_and_tables, get_session

from typing import Annotated, Any
from contextlib import asynccontextmanager

SessionDep = Annotated[Session, Depends(get_session())]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")
@app.get("/")
def main(request: Request):
    return templates.TemplateResponse(request=request, name="main.html")

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"Hello {name}"}
