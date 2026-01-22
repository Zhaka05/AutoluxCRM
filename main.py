from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Session
from .database import engine

from typing import Annotated
from contextlib import asynccontextmanager


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


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
