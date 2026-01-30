from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from typing import Annotated
from starlette import status
from database.model.user import Users
from core import security
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
db_depends = Annotated[Session, Depends(get_db)]


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(db: db_depends, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    db_query = db.query(Users).filter(Users.username == form_data.username).first()
    if not db_query:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    if not security.verify_password(form_data.password, db_query.enc_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    jwt_token = security.create_access_token(data={"sub": db_query.username, "dob": db_query.dob})
    return {"access_token": jwt_token, "token_type": "bearer"}

