# Finance Manager API

A comprehensive FastAPI-based REST API for managing personal finance operations including user authentication, account management, and balance tracking across multiple currencies.

## Features

### User Management
- User registration with email and phone validation
- Secure user authentication with JWT tokens
- Password management and change functionality
- User logout with token revocation

### Account Management
- Create and manage multiple bank accounts
- Support for multiple currencies per account
- View all accounts for a logged-in user
- Track actual and calculated balances

### Financial Operations
- Calculate total balance across multiple accounts
- Automatic currency conversion for balance calculations
- Transaction tracking and fixed transaction management

## Tech Stack

- **Backend Framework**: FastAPI
- **Language**: Python 3.8+
- **Database**: PostgreSQL / SQLite (for testing)
- **ORM**: SQLAlchemy
- **Authentication**: JWT (PyJWT)
- **Data Validation**: Pydantic
- **Security**: Bcrypt for password hashing
- **Testing**: Pytest with TestClient
- **HTTP Client**: HTTPX

## Project Structure

```
finance-manager-api/
├── api/
│   └── routers/
│       ├── auth.py           # Authentication endpoints
│       ├── user.py           # User management endpoints
│       └── trans.py          # Transaction endpoints
├── core/
│   ├── security.py           # Password hashing and token management
│   ├── config.py             # Configuration settings
│   └── dependencies.py        # FastAPI dependencies
├── database/
│   ├── session.py            # Database session configuration
│   ├── config.ini            # Database connection config
│   └── model/
│       ├── user.py           # User and Account models
│       └── revoked_token.py   # Token revocation model
├── schema/
│   └── user.py               # Pydantic request/response schemas
├── services/
│   ├── currency.py           # Currency conversion service
│   └── userserv.py           # User business logic
├── Test/
│   ├── test_database.py      # Test database setup
│   └── user_test.py          # User endpoint tests
├── main.py                   # Application entry point
└── requirement.txt           # Project dependencies
```

## API Endpoints

### Authentication
- **POST** `/auth/login` - User login with username and password

### User Management
- **POST** `/user/add-user` - Register a new user
- **GET** `/user/logged-user` - Get current logged-in user info
- **PUT** `/user/user/change-password` - Change user password
- **POST** `/user/user/me/logout` - Logout user (revoke token)

### Account Management
- **POST** `/user/user/me/add-account` - Add a new bank account
- **GET** `/user/user/me/accounts` - Get all accounts for user
- **POST** `/user/user/me/total-balance` - Calculate total balance in target currency

## Database Models

### Users Table
- `id`: Unique user identifier
- `username`: Generated from first_name + DOB (YYYYMMDD)
- `first_name`: User's first name
- `last_name`: User's last name
- `email`: User's email address (unique)
- `phone_number`: User's phone number (unique)
- `dob`: Date of birth (YYYY-MM-DD format)
- `enc_password`: Encrypted password

### UserAccount Table
- `userid`: Unique account identifier
- `username`: Foreign key to Users table
- `account_number`: Unique account number
- `account_type`: Type of account (e.g., savings, checking)
- `account_currency`: Account currency code (e.g., USD, INR)
- `act_balance`: Actual balance in the account
- `calc_balance`: Calculated balance

### RevokedToken Table
- `id`: Unique token identifier
- `jti`: JWT ID for revocation tracking
- `token`: Revoked token string
- `revoked_at`: Timestamp of revocation

### UserFixedTransaction Table
- `fixed_trans_id`: Unique transaction identifier
- `username`: Foreign key to Users table
- `account_trans_id`: Account identifier
- `int_trans_name`: Transaction name
- `int_trans_type`: Transaction type
- `int_amount`: Transaction amount
- `int_currency`: Transaction currency
- `interval`: Transaction interval
- `int_trans_date`: Transaction date

## Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL (for production) or SQLite (for testing)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd finance-manager-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv FINENV
   source FINENV/bin/activate  # On Windows: FINENV\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirement.txt
   ```

4. **Configure database**
   - Update `database/config.ini` with your database credentials
   - For PostgreSQL: Set appropriate connection string
   - For testing: SQLite database is created automatically

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`

6. **Access API documentation**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest Test/user_test.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=.
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Login**: POST request to `/auth/login` with username and password
2. **Receive Token**: Response includes `access_token` and `token_type`
3. **Use Token**: Include token in Authorization header: `Bearer <token>`
4. **Logout**: POST to `/user/user/me/logout` to revoke token

### Example Authentication Flow

```bash
# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user123&password=password"

# Use token
curl -X GET "http://localhost:8000/user/logged-user" \
  -H "Authorization: Bearer <access_token>"
```

## Configuration

### Environment Variables
Create a `.env` file with:
```
DATABASE_URL=postgresql://user:password@localhost/finance_manager
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
CURRENCY_API_KEY=your-api-key
CURRENCY_API_URL=https://api.example.com/convert
```

## Error Handling

The API returns standard HTTP status codes:
- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid input or validation error
- `401 Unauthorized`: Authentication required or token invalid
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Development

### Code Structure
- Routers in `api/routers/` handle HTTP requests
- Models in `database/model/` define database tables
- Schemas in `schema/` define request/response validation
- Services in `services/` contain business logic
- Core utilities in `core/` for configuration and security

### Adding New Endpoints
1. Create endpoint in appropriate router file
2. Define request/response schemas
3. Add database models if needed
4. Add comprehensive tests

## Testing

The project includes comprehensive unit tests for all endpoints:
- User registration and login
- Password management
- Account creation and retrieval
- Balance calculations
- Token revocation

Run tests with: `pytest`

## Future Enhancements

- [ ] Investment portfolio management
- [ ] Loan tracking system
- [ ] Transaction history and analytics
- [ ] Budget planning and tracking
- [ ] Bill reminders and notifications
- [ ] Mobile app support
- [ ] Advanced currency conversion with real-time rates

## License

[Specify your license]

## Author

[Your Name]

## Support

For issues and questions, please create an issue in the repository.
