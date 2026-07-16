from sqlmodel import SQLModel, Session, create_engine
import models.service_ticket as service_ticket
from models import carwash, service, owner, staff, vehicle_type, payment_type

postgres_url = "postgresql+psycopg://postgres:postgres@localhost:5432/autoluxcrm"

connect_args = {"check_same_thread": False}
engine = create_engine(postgres_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
