from fastapi import HTTPException, APIRouter, Response, status

from models import carwash

from dependencies import SessionDep

from . import tickets_router

router = APIRouter(
    prefix="/carwash",
    tags=["Carwash"]
)

# router.add_route(tickets_router.router)

@router.post("/", response_model=carwash.CarWashPublic)
def post_owner(session: SessionDep, carwash_form: carwash.CarWashCreate):
    
    current_carwash = carwash.CarWash(**carwash_form.model_dump())

    session.add(current_carwash)
    session.commit()
    session.refresh(current_carwash)

    return current_carwash

@router.get("/{carwash_id}", response_model=carwash.CarWashPublic)
def get_owner(carwash_id: int, session: SessionDep):
    current_carwash = session.get(carwash.CarWash, carwash_id)

    if not current_carwash:
        raise HTTPException(
            status_code=404, detail=f"CarWash with id {carwash_id} was not found"
        )
    return current_carwash