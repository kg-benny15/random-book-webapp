from sqlmodel import SQLModel, Field
from pydantic import EmailStr


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(min_length=1, max_length=20)
    email: EmailStr = Field(min_length=1, max_length=30)
    hash_password: str = Field(min_length=6, max_length=12)
