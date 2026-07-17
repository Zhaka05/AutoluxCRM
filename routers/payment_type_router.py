from fastapi import HTTPException, APIRouter, Response, status

from models import payment_type

from dependencies import SessionDep


router = APIRouter(
    prefix="/payment_type",
    tags=["Payment Type"]
)


@router.post("/", response_model=payment_type.PaymentTypePublic)
def post_payment_type(session: SessionDep, payment_form: payment_type.PaymentTypeCreate):
    
    payment = payment_type.PaymentType(**payment_form.model_dump())

    session.add(payment)
    session.commit()
    session.refresh(payment)

    return payment

@router.get("/{payment_type_id}", response_model=payment_type.PaymentTypePublic)
def get_payment_type(payment_type_id: int, session: SessionDep):
    payment = session.get(payment_type.PaymentType, payment_type_id)

    if not payment:
        raise HTTPException(
            status_code=404, detail=f"Payment Type with id {payment_type_id} was not found"
        )
    return payment