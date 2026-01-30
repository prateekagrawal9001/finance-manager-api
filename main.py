from fastapi import FastAPI
from api.routers import user, auth

app = FastAPI()

# Include user router
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def home():
    return {"message": "Welcome to the Finance Manager API"}
