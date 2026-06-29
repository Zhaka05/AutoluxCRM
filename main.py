from fastapi import FastAPI, Depends

from fastapi.staticfiles import StaticFiles

from database import create_db_and_tables

from contextlib import asynccontextmanager

from routers import tickets_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(tickets_router.router)

# templates = Jinja2Templates(directory="templates")
# @app.get("/")
# def main(request: Request):
#     return templates.TemplateResponse(request=request, name="main.html")


app.mount("/static", StaticFiles(directory="."), name="static")
