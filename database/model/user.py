from ..session import Base, get_db
from sqlalchemy import Column, Integer, String, Float, ForeignKey

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, dialect_kwargs={"description": "Unique user ID", "autoincrement": True})
    username = Column(String, unique=True, index=True, nullable=False, dialect_kwargs={"description": "First Name + dob"})
    first_name = Column(String, nullable=False, dialect_kwargs={"description": "User's first name"})
    last_name = Column(String, nullable=False, dialect_kwargs={"description": "User's last name"})
    phone_number = Column(String, unique=True, index=True, nullable=False, dialect_kwargs={"description": "User's phone number"})
    email = Column(String, unique=True, index=True, nullable=False, dialect_kwargs={"description": "User's email address"})
    dob = Column(String, nullable=False, dialect_kwargs={"description": "User's date of birth in YYYY-MM-DD format"})
    enc_password = Column(String, nullable=False, dialect_kwargs={"description": "User's encrypted password"})

class UserAccount(Base):
    __tablename__="useraccount"
    userid = Column(Integer, primary_key=True, index=True, autoincrement=True, dialect_kwargs={"description": "Unique account ID"})
    username = Column(String, ForeignKey("users.username"), nullable=False, dialect_kwargs={"description": "Username associated with the account"})
    account_number = Column(String, nullable=False, unique=True, dialect_kwargs={"description": "Unique account number"})
    account_type = Column(String, nullable=False, dialect_kwargs={"description": "Type of account (e.g., savings, checking)"})
    account_currency = Column(String(10), nullable=False, dialect_kwargs={"description": "Currency of the account"})
    act_balance = Column(Float, nullable=False, dialect_kwargs={"description": "Actual balance in the account"})
    calc_balance = Column(Float, nullable=False, dialect_kwargs={"description": "Calculated balance in the account"})

class UserFixedTransaction(Base):
    __tablename__="userfixedtransaction"
    fixed_trans_id = Column(Integer, primary_key=True, index=True, autoincrement=True, dialect_kwargs={"description": "Unique fixed transaction ID"})
    username = Column(String, ForeignKey("users.username"), nullable=False, dialect_kwargs={"description": "Username associated with the account"})
    account_trans_id = Column(String, nullable=False, dialect_kwargs={"description": "Account Type + '-' + account number"})
    int_trans_name = Column(String, nullable=False, dialect_kwargs={"description": "Name of the fixed transaction"})
    int_trans_type = Column(String, nullable=False, dialect_kwargs={"description": "Type of the fixed transaction"})
    int_amount = Column(Float, nullable=False, dialect_kwargs={"description": "Amount of the fixed transaction"})
    int_currency = Column(String(10), nullable=False, dialect_kwargs={"description": "Currency of the fixed transaction"})
    interval = Column(String, nullable=False, dialect_kwargs={"description": "Interval of the fixed transaction"})
    int_trans_date = Column(String, nullable=False, dialect_kwargs={"description": "Date of the fixed transaction"})

Base.metadata.create_all(bind=get_db().__next__().bind)