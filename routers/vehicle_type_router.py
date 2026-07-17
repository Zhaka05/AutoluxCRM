from fastapi import HTTPException, APIRouter, Response, status

from models import vehicle_type

from dependencies import SessionDep


router = APIRouter(
    prefix="/vehicle_type",
    tags=["Vehicle Type"]
)


@router.post("/", response_model=vehicle_type.VehicleTypePublic)
def post_vehicle_type(session: SessionDep, vehicle_form: vehicle_type.VehicleTypeCreate):
    
    vehicle = vehicle_type.VehicleType(**vehicle_form.model_dump())

    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)

    return vehicle

@router.get("/{vehicle_type_id}", response_model=vehicle_type.VehicleTypePublic)
def get_vehicle_type(vehicle_type_id: int, session: SessionDep):
    vehicle = session.get(vehicle_type.VehicleType, vehicle_type_id)

    if not vehicle:
        raise HTTPException(
            status_code=404, detail=f"Vehicle Type with id {vehicle_type_id} was not found"
        )
    return vehicle