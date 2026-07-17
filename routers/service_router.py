from fastapi import HTTPException, APIRouter, Response, status

from models import service

from dependencies import SessionDep


router = APIRouter(
    prefix="/service",
    tags=["Service"]
)


@router.post("/", response_model=service.ServicePublic)
def post_service(session: SessionDep, service_form: service.ServiceCreate):
    
    current_service = service.Service(**service_form.model_dump())

    session.add(current_service)
    session.commit()
    session.refresh(current_service)

    return current_service

@router.get("/{service_id}", response_model=service.ServicePublic)
def get_service(service_id: int, session: SessionDep):
    current_service = session.get(service.Service, service_id)

    if not current_service:
        raise HTTPException(
            status_code=404, detail=f"Service with id {service_id} was not found"
        )
    return current_service