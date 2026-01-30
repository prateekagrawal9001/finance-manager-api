from fastapi.testclient import TestClient
from database.session import get_db
from Test.test_database import get_test_db
from main import app
from unittest.mock import patch

tclient = TestClient(app)
app.dependency_overrides[get_db] = get_test_db


# ===== User Creation Tests =====

def test_add_user_success():
    """Test adding a new user successfully"""
    user_data = {
        "first_name": "Rupesh",
        "last_name": "Jha",
        "phone_number": "1234568901",
        "email": "rupesh.jha@example.com",
        "dob": "1998-08-15",
        "password": "StrongP@ssw0rd",
        "confirm_password": "StrongP@ssw0rd"
    }
    response = tclient.post("/user/add-user", json=user_data)
    print(response.json())
    assert response.status_code == 201
    assert response.json()["message"] == "User added successfully"


def test_add_user_password_mismatch():
    """Test adding user with mismatched passwords"""
    user_data = {
        "first_name": "Rupesh",
        "last_name": "Jha",
        "phone_number": "1234568901",
        "email": "rupesh.jha@example.com",
        "dob": "1998-08-15",
        "password": "StrongP@ssw0rd",
        "confirm_password": "DifferentP@ssw0rd"
    }
    response = tclient.post("/user/add-user", json=user_data)
    print(response.json())
    assert response.status_code == 400


def test_add_user_existing_email():
    """Test adding user with existing email"""
    user_data = {
        "first_name": "Rupesh",
        "last_name": "Jha",
        "phone_number": "1234568901",
        "email": "rupesh.jha@example.com",
        "dob": "1998-08-15",
        "password": "StrongP@ssw0rd",
        "confirm_password": "StrongP@ssw0rd"
    }
    response2 = tclient.post("/user/add-user", json=user_data)
    assert response2.status_code == 400
    assert response2.json()["detail"] == "User with given email or phone number already exists"


# ===== Authentication Tests =====

def test_login_success():
    """Test successful login"""
    response = tclient.post("/auth/login", data={"username": "Rupesh19980815", "password": "StrongP@ssw0rd"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_failed():
    """Test login with invalid credentials"""
    response = tclient.post("/auth/login", data={"username": "InvalidUser", "password": "WrongPassword"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"


def test_get_logged_user():
    """Test retrieving logged-in user info"""
    login_response = tclient.post("/auth/login", data={"username": "Rupesh19980815", "password": "StrongP@ssw0rd"})
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = tclient.get("/user/logged-user", headers=headers)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["userdata"]["sub"] == "Rupesh19980815"


def test_get_logged_user_unauthorized():
    """Test retrieving logged-in user without token"""
    response = tclient.get("/user/logged-user")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


# ===== Password Change Tests =====

def test_change_password_success():
    """Test changing password successfully"""
    login_response = tclient.post("/auth/login", data={"username": "Rupesh19980815", "password": "StrongP@ssw0rd"})
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    change_password_data = {
        "old_password": "StrongP@ssw0rd",
        "new_password": "NewStrongP@ssw0rd",
        "confirm_new_password": "NewStrongP@ssw0rd"
    }
    response = tclient.put("/user/user/change-password", headers=headers, json=change_password_data)
    print(response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "Password changed successfully"


def test_change_password_incorrect_old():
    """Test changing password with incorrect old password"""
    login_response = tclient.post("/auth/login", data={"username": "Rupesh19980815", "password": "NewStrongP@ssw0rd"})
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    change_password_data = {
        "old_password": "WrongOldP@ssw0rd",
        "new_password": "AnotherStrongP@ssw0rd",
        "confirm_new_password": "AnotherStrongP@ssw0rd"
    }
    response = tclient.put("/user/user/change-password", headers=headers, json=change_password_data)
    print(response.json())
    assert response.status_code == 400
    assert response.json()["detail"] == "Old password is incorrect"


def test_change_password_mismatch():
    """Test changing password with mismatched new passwords"""
    login_response = tclient.post("/auth/login", data={"username": "Rupesh19980815", "password": "NewStrongP@ssw0rd"})
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    change_password_data = {
        "old_password": "NewStrongP@ssw0rd",
        "new_password": "AnotherStrongP@ssw0rd",
        "confirm_new_password": "DifferentP@ssw0rd"
    }
    response = tclient.put("/user/user/change-password", headers=headers, json=change_password_data)
    print(response.json())
    assert response.status_code == 400
    assert response.json()["detail"] == "New passwords do not match"


def test_change_password_user_not_found():
    """Test changing password for non-existent user - simulate by using token after user deletion"""
    # First create and login a user
    user_data = {
        "first_name": "TempUser",
        "last_name": "ForDelete",
        "phone_number": "8888888888",
        "email": "tempuser@example.com",
        "dob": "1995-05-05",
        "password": "TempP@ssw0rd",
        "confirm_password": "TempP@ssw0rd"
    }
    tclient.post("/user/add-user", json=user_data)
    
    # Get token for this user
    login_response = tclient.post("/auth/login", data={"username": "TempUser19950505", "password": "TempP@ssw0rd"})
    token = login_response.json()["access_token"]
    
    # Delete the user from database to simulate non-existent user
    from database.session import SessionLocal
    from database.model.user import Users
    db = SessionLocal()
    db.query(Users).filter(Users.username == "TempUser19950505").delete()
    db.commit()
    db.close()
    
    # Try to change password with token but user no longer exists
    headers = {"Authorization": f"Bearer {token}"}
    change_password_data = {
        "old_password": "TempP@ssw0rd",
        "new_password": "AnotherStrongP@ssw0rd",
        "confirm_new_password": "AnotherStrongP@ssw0rd"
    }
    response = tclient.put("/user/user/change-password", headers=headers, json=change_password_data)
    print(response.json())
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


# ===== Logout Tests =====

def test_logout_user():
    """Test user logout"""
    login_response = tclient.post("/auth/login", data={"username": "Rupesh19980815", "password": "NewStrongP@ssw0rd"})
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    # Mock the database to ensure revoked_tokens table exists and operations succeed
    with patch('core.security.RevokedToken') as mock_revoked:
        response = tclient.post("/user/user/me/logout", headers=headers)
        print(response.json())
        assert response.status_code == 200
        assert response.json()["message"] == "User logged out successfully"


def test_logout_user_unauthorized():
    """Test logout without authentication"""
    response = tclient.post("/user/user/me/logout")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


# ===== Account Management Tests =====

def test_add_account_success():
    """Test adding an account successfully"""
    login_response = tclient.post("/auth/login", data={"username": "Rupesh19980815", "password": "NewStrongP@ssw0rd"})
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    account_data = {
        "account_number": "ACC123456",
        "account_type": "savings",
        "account_currency": "USD",
        "act_balance": 1500.0
    }
    response = tclient.post("/user/user/me/add-account", headers=headers, json=account_data)
    print(response.json())
    assert response.status_code == 201
    assert response.json()["message"] == "Account added successfully"


def test_add_account_user_not_found():
    """Test adding account for non-existent user"""
    # First create and login a user
    user_data = {
        "first_name": "TempUser2",
        "last_name": "ForDelete2",
        "phone_number": "7777777777",
        "email": "tempuser2@example.com",
        "dob": "1996-06-06",
        "password": "TempP@ssw0rd2",
        "confirm_password": "TempP@ssw0rd2"
    }
    tclient.post("/user/add-user", json=user_data)
    
    # Get token for this user
    login_response = tclient.post("/auth/login", data={"username": "TempUser219960606", "password": "TempP@ssw0rd2"})
    token = login_response.json()["access_token"]
    
    # Delete the user from database to simulate non-existent user
    from database.session import SessionLocal
    from database.model.user import Users
    db = SessionLocal()
    db.query(Users).filter(Users.username == "TempUser219960606").delete()
    db.commit()
    db.close()
    
    # Try to add account with token but user no longer exists
    headers = {"Authorization": f"Bearer {token}"}
    account_data = {
        "account_number": "ACC123456",
        "account_type": "savings",
        "account_currency": "USD",
        "act_balance": 1500.0
    }
    response = tclient.post("/user/user/me/add-account", headers=headers, json=account_data)
    print(response.json())
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_accounts_success():
    """Test retrieving accounts successfully"""
    login_response = tclient.post("/auth/login", data={"username": "Rupesh19980815", "password": "NewStrongP@ssw0rd"})
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = tclient.get("/user/user/me/accounts", headers=headers)
    print(response.json())
    assert response.status_code == 200
    assert "accounts" in response.json()
    assert len(response.json()["accounts"]) > 0


def test_get_accounts_user_not_found():
    """Test retrieving accounts for non-existent user"""
    # First create and login a user
    user_data = {
        "first_name": "TempUser3",
        "last_name": "ForDelete3",
        "phone_number": "6666666666",
        "email": "tempuser3@example.com",
        "dob": "1997-07-07",
        "password": "TempP@ssw0rd3",
        "confirm_password": "TempP@ssw0rd3"
    }
    tclient.post("/user/add-user", json=user_data)
    
    # Get token for this user
    login_response = tclient.post("/auth/login", data={"username": "TempUser319970707", "password": "TempP@ssw0rd3"})
    token = login_response.json()["access_token"]
    
    # Delete the user from database to simulate non-existent user
    from database.session import SessionLocal
    from database.model.user import Users
    db = SessionLocal()
    db.query(Users).filter(Users.username == "TempUser319970707").delete()
    db.commit()
    db.close()
    
    # Try to get accounts with token but user no longer exists
    headers = {"Authorization": f"Bearer {token}"}
    response = tclient.get("/user/user/me/accounts", headers=headers)
    print(response.json())
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


# ===== Balance Tests =====

def test_user_total_balance_success():
    """Test retrieving total balance successfully"""
    login_response = tclient.post("/auth/login", data={"username": "Rupesh19980815", "password": "NewStrongP@ssw0rd"})
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    balance_data = {
        "target_currency": "INR"
    }
    # Mock the currency conversion to avoid external API calls
    with patch('services.userserv.convert_currency', return_value=1500.0):
        response = tclient.post("/user/user/me/total-balance", headers=headers, json=balance_data)
        print(response.json())
        assert response.status_code == 200
        assert "total_balance" in response.json()


def test_user_total_balance_no_accounts():
    """Test total balance for user with no accounts"""
    # Add a new user with no accounts
    user_data = {
        "first_name": "NoAccount",
        "last_name": "User",
        "phone_number": "9999999999",
        "email": "noaccounts@example.com",
        "dob": "2000-01-01",
        "password": "TestP@ssw0rd",
        "confirm_password": "TestP@ssw0rd"
    }
    tclient.post("/user/add-user", json=user_data)
    
    # Login with the new user
    login_response = tclient.post("/auth/login", data={"username": "NoAccount20000101", "password": "TestP@ssw0rd"})
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    balance_data = {
        "target_currency": "INR"
    }
    # Mock the currency conversion to avoid external API calls
    with patch('services.userserv.convert_currency', return_value=0.0):
        response = tclient.post("/user/user/me/total-balance", headers=headers, json=balance_data)
        print(response.json())
        assert response.status_code == 404
        assert response.json()["detail"] == "No accounts found for user"


def test_user_total_balance_unauthorized():
    """Test total balance without authentication"""
    balance_data = {
        "target_currency": "INR"
    }
    response = tclient.post("/user/user/me/total-balance", json=balance_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"