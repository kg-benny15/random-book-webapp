"""
User models for authentication and profile management.

Models included:
- User: Database table (with relationships to reading materials)
- CreateUser: Registration validation
- UpdateUserInfo: Profile updates
- ResetPassword: Password change
- UserResponse: API response (safe, no password)

Relationships:
- Many-to-Many with ReadingMaterial through UserMaterialLink
"""

from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr, field_validator
from typing import Optional, TYPE_CHECKING
from app.models.user_material_link import UserMaterialLink

if TYPE_CHECKING:
    from app.models import ReadingMaterial

# ============================================================
# DATABASE TABLE (WITH RELATIONSHIPS)
# ============================================================


class User(SQLModel, table=True):
    """Users table in PostgreSQL"""

    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=20)
    email: str = Field(unique=True, max_length=100)
    hash_password: str = Field(max_length=255)  # bcrypt hash, never plain text

    # ============================================================
    # USER RELATIONSHIPS
    # ============================================================

    # Many-to-Many: User → ReadingMaterial (via link table)
    reading_materials: list["ReadingMaterial"] = Relationship(
        back_populates="users", link_model=UserMaterialLink
    )

    # One-to-Many: User → UserMaterialLink (access intermediate table fields)
    user_reading_links: list[UserMaterialLink] = Relationship(back_populates="user")


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
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$",
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
        regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$",
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
