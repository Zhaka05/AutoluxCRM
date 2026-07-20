from fastapi import HTTPException, APIRouter, Response, status
from sqlmodel import select

from models import owner
import utils

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


@router.post("/login")
def login(owner_credentials: owner.OwnerLogin, session: SessionDep):
    statement = select(owner.Owner).where(owner.Owner.phone == owner_credentials.phone)
    current_owner = session.exec(statement).first()

    if not current_owner or not utils.verify_password(
        owner_credentials.password, current_owner.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials"
        )

    return {"example_token": "token"}
