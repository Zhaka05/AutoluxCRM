from fastapi import HTTPException, APIRouter, Response, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from typing import Annotated

from models import owner
import schemas
import utils, oauth2

from dependencies import SessionDep

router = APIRouter(prefix="/owner", tags=["Owner"])


@router.post("/", response_model=owner.OwnerPublic)
def post_owner(session: SessionDep, owner_form: owner.OwnerCreate):
    owner_data = owner_form.model_dump(exclude={"password"})

    current_owner = owner.Owner(
        **owner_data, password_hash=utils.get_password_hash(owner_form.password)
    )

    session.add(current_owner)
    session.commit()
    session.refresh(current_owner)

    return current_owner


@router.get("/{owner_id}", response_model=owner.OwnerPublic)
def get_owner(owner_id: int, session: SessionDep):
    current_owner = session.get(owner.Owner, owner_id)

    if not current_owner:
        raise HTTPException(
            status_code=404, detail=f"carwash with id {owner_id} was not found"
        )
    return current_owner


@router.post("/login", response_model=schemas.Token)
def login(owner_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    statement = select(owner.Owner).where(owner.Owner.phone == owner_credentials.username)
    current_owner = session.exec(statement).first()

    if not current_owner or not utils.verify_password(
        owner_credentials.password, current_owner.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    access_token = oauth2.create_access_token(data={"user_id": current_owner.id})
    return {"access_token": access_token, "token_type": "bearer"}
