"""
User models for authentication and profile management.

Models included:
- User: Database table
- CreateUser: Registration validation
- UpdateUserInfo: Profile updates
- ResetPassword: Password change
- UserResponse: API response (safe, no password)
"""

from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator
from typing import Optional

# ============================================================
# DATABASE TABLE
# ============================================================


class User(SQLModel, table=True):
    """Users table in PostgreSQL"""

    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=20)
    email: str = Field(unique=True, max_length=100)
    hash_password: str = Field(max_length=255)  # bcrypt hash, never plain text


# ============================================================
# REGISTRATION
# ============================================================


class CreateUser(SQLModel):
    """Validate user registration data"""

    username: str = Field(min_length=3, max_length=20)
    email: EmailStr
    plain_password: str = Field(
        min_length=8,
        max_length=20,
        pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$",
    )
    plain_password2: str  # confirmation

    @field_validator("plain_password2")
    @classmethod
    def confirm_password(cls, v: str, info) -> str:
        """Ensure password and confirmation match"""
        if v != info.data.get("plain_password"):
            raise ValueError("The passwords don't match")
        return v


# ============================================================
# PROFILE UPDATE
# ============================================================


class UpdateUserInfo(SQLModel):
    """Update user profile (all fields optional)"""

    username: Optional[str] = Field(default=None, min_length=3, max_length=20)
    email: Optional[EmailStr] = Field(default=None)


# ============================================================
# PASSWORD RESET
# ============================================================


class ResetPassword(SQLModel):
    """Change user password"""

    new_plain_password: str = Field(
        min_length=8,
        max_length=20,
        pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$",
    )
    new_plain_password2: str  # confirmation

    @field_validator("new_plain_password2")
    @classmethod
    def confirm_password(cls, v: str, info) -> str:
        """Ensure password and confirmation match"""
        if v != info.data.get("new_plain_password"):
            raise ValueError("The passwords don't match")
        return v


# ============================================================
# API RESPONSE (NO sensitive data)
# ============================================================


class UserResponse(SQLModel):
    """Safe user data for API responses (no password hash)"""

    id: int
    username: str
    email: EmailStr
