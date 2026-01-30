from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from database.model.user import Users, UserAccount
from typing import Annotated
from schema.user import AddUserSchema, ChangePasswordSchema, UserAccountAddition, UserTotalBalanceSchema    
from starlette import status
from core import security, config
from core.dependencies import verify_token
from fastapi.security import OAuth2PasswordBearer
from services.userserv import total_balance_calc

oauth_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()

db_depends = Annotated[Session, Depends(get_db)]


# Placeholder for actual decoding logic if needed
@router.post("/add-user", status_code=status.HTTP_201_CREATED)
async def add_user(db:db_depends, user: AddUserSchema):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    db_user = db.query(Users).filter((Users.email == user.email) | (Users.phone_number == user.phone_number)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="User with given email or phone number already exists")   

    hashed_pw = security.hash_password(user.password)
    new_user = Users(
        username=user.first_name + user.dob.replace("-", ""),
        first_name=user.first_name,
        last_name=user.last_name,
        phone_number=user.phone_number,
        email=user.email,
        dob=user.dob,
        enc_password=hashed_pw
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User added successfully", "username": new_user.username}

@router.get("/logged-user", status_code=status.HTTP_200_OK)
async def get_users(db: db_depends, userdata: Annotated[str, Depends(verify_token)]):
    return {"message": "Users retrieved successfully", "userdata": userdata}

@router.put("/user/change-password", status_code=status.HTTP_200_OK)
async def change_password(db: db_depends, userdata: Annotated[dict, Depends(verify_token)], payload: ChangePasswordSchema):
    username = userdata.get("sub")
    old_password = payload.old_password
    new_password = payload.new_password
    confirm_new_password = payload.confirm_new_password

    if new_password != confirm_new_password:
        raise HTTPException(status_code=400, detail="New passwords do not match")

    db_user = db.query(Users).filter(Users.username == username).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not security.verify_password(old_password, db_user.enc_password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    hashed_pw = security.hash_password(new_password)
    db_user.enc_password = hashed_pw
    db.commit()
    db.refresh(db_user)

    return {"message": "Password changed successfully"}

@router.post("/user/me/logout", status_code=status.HTTP_200_OK)
async def logout_user(token: Annotated[str, Depends(oauth_bearer)], db: db_depends):
    security.revoke_token(token, db)
    return {"message": "User logged out successfully"}

@router.post("/user/me/add-account", status_code=status.HTTP_201_CREATED)
async def add_account(db: db_depends, userdata: Annotated[dict, Depends(verify_token)], payload: UserAccountAddition):
    username = userdata.get("sub")
    db_user = db.query(Users).filter(Users.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    new_account = UserAccount(
        username=username,
        account_number=payload.account_number,
        account_type=payload.account_type,
        account_currency=payload.account_currency,
        act_balance=payload.act_balance,
        calc_balance=0.00
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return {"message": "Account added successfully", "username": new_account.username, "account_number": new_account.account_number, "account_type": new_account.account_type}

@router.get("/user/me/accounts", status_code=status.HTTP_200_OK)
async def get_accounts(db: db_depends, userdata: Annotated[dict, Depends(verify_token)]):
    username = userdata.get("sub")
    db_user = db.query(Users).filter(Users.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    accounts = db.query(UserAccount).filter(UserAccount.username == username).all()
    account_list = []
    for account in accounts:
        account_data = {
            "account_number": account.account_number,
            "account_type": account.account_type,
            "account_currency": account.account_currency,
            "act_balance": account.act_balance,
            "calc_balance": account.calc_balance
        }
        account_list.append(account_data)
    return {"message": "Accounts retrieved successfully", "accounts": account_list}

@router.post("/user/me/total-balance", status_code=status.HTTP_200_OK)
async def user_total_balance(db: db_depends, userdata: Annotated[dict, Depends(verify_token)], usertt : UserTotalBalanceSchema):
    username = userdata.get("sub")
    accounts = db.query(UserAccount).filter(UserAccount.username == username).all()
    if not accounts:
        raise HTTPException(status_code=404, detail="No accounts found for user")
    
    total_balance = total_balance_calc(usertt.target_currency, accounts)
    return {"message": "Total balance calculated successfully", "total_balance": total_balance}