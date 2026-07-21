from sqlmodel import SQLModel, Session, create_engine
import models.service_ticket as service_ticket
from models import carwash, service, owner, staff, vehicle_type, payment_type
from config import settings

postgres_url = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(postgres_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
