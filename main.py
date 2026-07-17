from fastapi import FastAPI, Depends, Request

from fastapi.staticfiles import StaticFiles

from database import create_db_and_tables

from contextlib import asynccontextmanager

from routers import tickets_router, owner_router, carwash_router, payment_type_router, vehicle_type_router, service_router, staff_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


# templates = Jinja2Templates(directory="templates")
@app.get("/")
def main(request: Request):
    return {"health": "ok"}

app.include_router(tickets_router.router)
app.include_router(owner_router.router)
app.include_router(carwash_router.router)
app.include_router(payment_type_router.router)
app.include_router(vehicle_type_router.router)
app.include_router(service_router.router)
app.include_router(staff_router.router)

app.mount("/static", StaticFiles(directory="."), name="static")
