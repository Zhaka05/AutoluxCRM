from fastapi import HTTPException, APIRouter, Response, status

from models import owner

from dependencies import SessionDep

router = APIRouter(
    prefix="/owner",
    tags=["Owner"]
)

@router.post("/", response_model=owner.OwnerPublic)
def post_owner(session: SessionDep, owner_form: owner.OwnerCreate):
    
    current_owner = owner.Owner(**owner_form.model_dump())

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