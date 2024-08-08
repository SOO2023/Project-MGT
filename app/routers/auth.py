from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from ..authenticate import JWT, verify_user
from ..database import db_session
from sqlalchemy.orm import Session


router = APIRouter(prefix="/auth", tags=["Login"])
jwt_obj = JWT()


@router.post(
    "/login",
    description="This endpoint is used to authenticate the user. The access token is generated and attached to the header using this endpoint.",
)
def login(
    formdata: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_session)
):
    user = verify_user(formdata.username, formdata.password, db)
    payload = {"id": user.id, "role": user.role}
    token = jwt_obj.jwt_encode(payload=payload)
    return {"access_token": token, "token_type": "bearer"}
