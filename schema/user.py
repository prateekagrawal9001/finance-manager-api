from pydantic import BaseModel, EmailStr, Field


class AddUserSchema(BaseModel):
    first_name: str = Field(min_length=3, max_length=30, description="First name must be between 5 and 30 characters", default="Prateek", pattern="^[A-Za-z]+$")
    last_name: str = Field(min_length=3, max_length=30, description="Last name must be between 5 and 30 characters", default="Agrawal", pattern="^[A-Za-z]+$")
    phone_number: str = Field(min_length=10, max_length=15, description="Phone number must be between 10 and 15 characters", default="7823897738", pattern="^[0-9]+$")
    email: EmailStr = Field(description="Valid email address", default="prateekagrawal9001@gmail.com", pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    dob: str = Field(description="Date of Birth in YYYY-MM-DD format", default="1995-08-15", pattern=r'^\d{4}-\d{2}-\d{2}$')
    password: str = Field(min_length=8, max_length=30, description="Password must be between 8 and 30 characters", default="StrongP@ssw0rd")
    confirm_password: str = Field(min_length=8, max_length=30, description="Confirm password must match the password", default="StrongP@ssw0rd")

class UserLoginSchema(BaseModel):
    username: str = Field(min_length=5, max_length=30, description="Username must be between 5 and 30 characters", default="Prateek7738")
    password: str = Field(min_length=8, max_length=30, description="Password must be between 8 and 30 characters", default="StrongP@ssw0rd")


class ChangePasswordSchema(BaseModel):
    old_password: str = Field(min_length=8, max_length=30)
    new_password: str = Field(min_length=8, max_length=30)
    confirm_new_password: str = Field(min_length=8, max_length=30)

class UserChangePassword(BaseModel):
    old_password: str = Field(min_length=8, max_length=30, description="Old password must be between 8 and 30 characters", default="StrongP@ssw0rd")
    new_password: str = Field(min_length=8, max_length=30, description="New password must be between 8 and 30 characters", default="NewStrongP@ssw0rd")
    confirm_new_password: str = Field(min_length=8, max_length=30, description="Confirm new password must match the new password", default="NewStrongP@ssw0rd")

class UserAccountAddition(BaseModel):
    account_number: str = Field(min_length=4, max_length=20, description="account number/card number/upi id", default="1234")
    account_type: str = Field(min_length=3, max_length=20, description="Account type must be between 3 and 20 characters", default="savings", examples=["savings", "current", "credit card", "debit card", "upi", ])
    account_currency: str = Field(min_length=3, max_length=10, description="Account currency must be between 3 and 10 characters", default="INR", examples=["INR", "USD", "EUR"])
    act_balance: float = Field(ge=0, description="Actual balance must be non-negative", default=1000.0)

class UserTotalBalanceSchema(BaseModel):
    target_currency: str = Field(min_length=3, max_length=10, description="Target currency must be between 3 and 10 characters", default="INR")