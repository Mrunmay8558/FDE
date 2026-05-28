from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from auth import encrypt_password, signJWT, verify_hash_password, decodeJWT
from fastapi.security import OAuth2PasswordBearer
import uuid
import time

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/login")


class UserAddress(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    mobile_number: str
    password: str
    address: Optional[UserAddress] = None


class User(BaseModel):
    id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    mobile_number: Optional[str] = None
    address: Optional[UserAddress] = None
    password: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    mobile_number: str
    address: Optional[UserAddress] = None
    created_at: str
    updated_at: str
    access_token: str


class LoginRequest(BaseModel):
    email: str
    password: str


class ResetPasswordRequest(BaseModel):
    old_password: str
    new_password: str


users = []


@app.get("/")
def read_root():
    return {"response": "ping to user dashboard"}


@app.get("/v1/users")
def get_users(token: str = Depends(oauth2_scheme), page: int = 1, page_size: int = 10):
    """
    Returns a list of all users in the system.

    Returns:
        A list of user objects, where each object contains the user's id, name, and email.
    """
    authenticated_user_details = decodeJWT(token)
    if not authenticated_user_details:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return users[start_index:end_index]


@app.get("/v1/users/{user_id}")
def get_user(user_id: str, token: str = Depends(oauth2_scheme)):
    """
    Returns the details of a specific user.

    Args:
        user_id: The unique identifier of the user to retrieve.

    Returns:
        A user object containing the user's id, name, and email.
    """
    authenticated_user_details = decodeJWT(token)
    if not authenticated_user_details:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    user = next((user for user in users if user["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


@app.post("/v1/users")
def create_user(request: UserCreate):
    """
    Creates a new user in the system.

    Args:
        user: A dictionary containing the user's name and email.

    Returns:
        The created user object, which includes the user's id, name, and email.
    """
    try:
        request = request.model_dump()
        existing_user = next(
            (user for user in users if user["email"] == request["email"]), None
        )
        if existing_user:
            raise HTTPException(
                status_code=400, detail="A user with this email already exists."
            )
        hashed_password = encrypt_password(request["password"])
        user_id = str(uuid.uuid4())

        user = {
            "id": user_id,
            "first_name": request["first_name"],
            "last_name": request["last_name"],
            "email": request["email"],
            "mobile_number": request["mobile_number"],
            "address": request.get("address"),
            "password": hashed_password,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

        user = User(**user)
        users.append(user.model_dump())
        access_token = signJWT(user_id, request["email"], 3600)
        user_dict = user.model_dump()
        user_dict["access_token"] = access_token
        return UserResponse(**user_dict)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/login")
async def login(request: LoginRequest):
    """
    Authenticates a user and returns an access token.

    Args:
        request: A LoginRequest object containing the user's email and password.
    Returns:
        A UserResponse object containing the user's details and an access token.
    """
    try:
        request = request.model_dump()
        user = next((user for user in users if user["email"] == request["email"]), None)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        if not verify_hash_password(request["password"], user["password"]):
            raise HTTPException(status_code=401, detail="Invalid Credentials.")
        access_token = signJWT(user["id"], user["email"], 3600)
        user_dict = User(**user).model_dump()
        user_dict["access_token"] = access_token
        return UserResponse(**user_dict)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/reset-password")
def reset_password(request: ResetPasswordRequest, token: str = Depends(oauth2_scheme)):
    """
    Resets a user's password.

    Args:
        request: A ResetPasswordRequest object containing the old and new passwords.

    Returns:
        A success message if the password was reset successfully.
    """
    try:
        request = request.model_dump()
        authenticated_user_details = decodeJWT(token)
        if not authenticated_user_details:
            raise HTTPException(status_code=401, detail="Invalid or expired token.")
        user = next(
            (
                user
                for user in users
                if user["id"] == authenticated_user_details["user_id"]
            ),
            None,
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        if not verify_hash_password(request["old_password"], user["password"]):
            raise HTTPException(status_code=401, detail="Invalid Credentials.")
        hashed_password = encrypt_password(request["new_password"])
        user["password"] = hashed_password
        user["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        return {"message": "Password reset successful."}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
