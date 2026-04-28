from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import date
from passlib.context import CryptContext
import re

from app.backend.database import get_db
from app.backend.utils.auth import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter(tags=["Authentication"])


class RegisterRequest(BaseModel):
    """User registration request model."""
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username (3-50 chars, alphanumeric, _, -)"
    )
    password: str = Field(
        ...,
        min_length=6,
        description="Password (minimum 6 characters)"
    )
    full_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Full name (can be duplicate)"
    )
    birth_date: str = Field(
        ...,
        description="Birth date in format YYYY-MM-DD, e.g. 1990-05-20"
    )

    def validate_birth_date(self) -> None:
        """Validate birth date is in past and reasonable age."""
        try:
            bd = date.fromisoformat(self.birth_date)
            today = date.today()
            if bd > today:
                raise ValueError("Birth date cannot be in the future")
            if (today.year - bd.year) > 120:
                raise ValueError("Age cannot exceed 120 years")
        except ValueError as e:
            raise ValueError(f"Invalid birth date: {str(e)}")

    def validate_username(self) -> None:
        """Validate username format: only alphanumeric, underscore, hyphen."""
        if not re.match(r"^[a-zA-Z0-9_-]+$", self.username):
            raise ValueError(
                "Username can only contain letters, numbers, underscore and hyphen"
            )


class LoginRequest(BaseModel):
    """User login request model."""
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class TokenResponse(BaseModel):
    """JWT token response model."""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")


class RegisterResponse(BaseModel):
    """Successful registration response with token and user details."""
    message: str = Field(..., description="Success message")
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")
    user_id: int = Field(..., description="New user ID")
    username: str = Field(..., description="Username")


@router.post("/register", response_model=RegisterResponse, summary="Register new user")
def register(req: RegisterRequest):
    """
    Register a new user and return JWT token immediately.

    - **username**: unique username (3-50 chars, only letters/numbers/_ -)
    - **password**: password (minimum 6 characters)
    - **full_name**: user's full name (can be duplicate)
    - **birth_date**: birth date in YYYY-MM-DD format
    """
    # Validate username format
    try:
        req.validate_username()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Validate birth date
    try:
        req.validate_birth_date()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Hash password
    password_hash = pwd_context.hash(req.password)

    with get_db() as conn:
        # Check if username already exists (must be unique)
        exists = conn.execute(
            "SELECT 1 FROM users WHERE username = ?",
            (req.username,)
        ).fetchone()
        if exists:
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )

        # Create new user
        cur = conn.execute(
            "INSERT INTO users (username, password_hash, full_name, birth_date) "
            "VALUES (?, ?, ?, ?)",
            (req.username, password_hash, req.full_name, req.birth_date),
        )
        user_id = cur.lastrowid
        conn.commit()
    # Generate JWT token immediately
    token = create_access_token({"sub": req.username})
    return {
        "message": "User successfully registered",
        "access_token": token,
        "token_type": "bearer",
        "user_id": user_id,
        "username": req.username
    }


@router.post("/login", response_model=TokenResponse, summary="Login and get JWT token")
def login(req: LoginRequest):
    """
    Authenticate user and return JWT token.

    Returns JWT token for use with protected endpoints.
    """
    with get_db() as conn:
        # Find user by username
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (req.username,)
        ).fetchone()

        # Check user exists and password is correct
        if not user or not pwd_context.verify(req.password, user["password_hash"]):
            raise HTTPException(
                status_code=401,
                detail="Incorrect username or password"
            )

        # Generate JWT token
        token = create_access_token({"sub": req.username})
        return {"access_token": token, "token_type": "bearer"}
