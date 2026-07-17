from fastapi import HTTPException, APIRouter, Response, status

from models import staff

from dependencies import SessionDep


router = APIRouter(
    prefix="/staff",
    tags=["Staff"]
)


@router.post("/", response_model=staff.StaffPublic)
def post_staff(session: SessionDep, staff_form: staff.StaffCreate):
    
    current_staff = staff.Staff(**staff_form.model_dump())

    session.add(current_staff)
    session.commit()
    session.refresh(current_staff)

    return current_staff

@router.get("/{staff_id}", response_model=staff.StaffPublic)
def get_staff(staff_id: int, session: SessionDep):
    current_staff = session.get(staff.Staff, staff_id)

    if not current_staff:
        raise HTTPException(
            status_code=404, detail=f"Staff with id {staff_id} was not found"
        )
    return current_staff