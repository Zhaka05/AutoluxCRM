from fastapi import Depends


from sqlmodel import Session
from database import create_db_and_tables, get_session
from typing import Annotated

SessionDep = Annotated[Session, Depends(get_session)]
