from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from models import pydantic_validators
from db_module import db, user_handler
from passlib.context import CryptContext
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import create_engine, text, exc
import os

db.db_bootstrap()
app = FastAPI()

# # Pick DB credentials from environment variables
# host = os.getenv("TEST_DB_HOST")
# port = os.getenv("TEST_DB_PORT", 5432)  # Default to 5432 if not specified
# database = os.getenv("TEST_DB_NAME")
# user = os.getenv("TEST_DB_USER")
# password = os.getenv("TEST_DB_PASSWORD")

# # Create the database URL
# db_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
db_url = f"postgresql://airflow:airflow@postgres:5432/airflow"

print("Database URL:", db_url)

# Initialize the engine
engine = create_engine(db_url)

# Initialize password context for hashing and verification
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Basic Auth
security = HTTPBasic()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    user = user_handler.get_user_details(credentials.username, engine)
    correct_password = verify_password(credentials.password, user_handler.get_hashed_password(credentials.username, engine))
    if not user or not correct_password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return credentials.username

@app.get("/healthz")
def db_health_check():
    try:
        # Attempt to connect to the database
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))  # Using text to ensure it's executable
            result.fetchone()
            return JSONResponse(status_code=200, content={"message": "Health Check Successful"})
    except exc.SQLAlchemyError as e:
        print(f"Database connection failed: {str(e)}")
        return JSONResponse(status_code=503, content={"message": "Health Check Failed"})

@app.post("/v1/user")
async def create_user(user: pydantic_validators.CreateUserPayload):
    try:
        # Hash the password
        hashed_password = pwd_context.hash(user.password)
        user.password = hashed_password
        result = user_handler.create_user(user.dict(), engine)
        if result['status_code'] == 201:
            return JSONResponse(status_code=201, content={"message": "User created successfully"})
        else:
            return JSONResponse(status_code=result['status_code'], content={"message": result['description']})
    except ValidationError as e:
        return JSONResponse(status_code=400, content={"message": "Invalid payload"})

# @app.get("/v2/user/self")
# async def get_user_details(username: str = Depends(get_current_username)):
#     user = user_handler.get_user_details(username, engine)
#     if user:
#         return user
#     else:
#         raise HTTPException(status_code=404, detail="User not found")

# @app.put("/v2/user/self")
# async def update_user_details(update: pydantic_validators.UpdateUserPayload, username: str = Depends(get_current_username)):
#     if user_handler.check_user_exists(username, engine):
#         hashed_password = pwd_context.hash(update.password)
#         update.password = hashed_password
#         result = user_handler.update_user_details(username, update.dict(), engine)
#         return result
#     else:
#         raise HTTPException(status_code=404, detail="User not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
