"""
Reading Material Models for user's book library.

Models:
- ReadingMaterial: Database table (with relationships to users)
- PresentingReadingMaterial: Search/random book results
- AddReadingMaterial: Form data when user adds a book
- MaterialResume: User's reading list summary

Relationships:
- Many-to-Many with User through UserMaterialLink
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from sqlalchemy import JSON

# ============================================================
# DATABASE TABLE (WITH RELATIONSHIPS)
# ============================================================


class ReadingMaterial(SQLModel, table=True):
    """Stores books that users have added to their library"""

    __tablename__ = "reading_materials"

    id: int | None = Field(default=None, primary_key=True)
    work_id: str = Field(index=True, max_length=50)  # OpenLibrary ID
    cover_id: int | None = Field(default=None)  # Book cover from OpenLibrary
    year: int | None = Field(default=None, gt=1000)  # Publication year
    title: str = Field(max_length=200)  # Book title
    author: str = Field(max_length=100)  # Author name
    genre: list[str] = Field(default=[], sa_type=JSON)  # Tags/categories
    material_type: str = Field(max_length=30)  # book, comic, etc.
    total_pages: int | None = Field(default=None, ge=1)  # Total pages


# ============================================================
# API SCHEMAS
# ============================================================


class PresentingReadingMaterial(SQLModel):
    """Book preview for search results / random discovery"""

    cover_id: int
    year: int
    title: str
    author: str
    total_pages: int
    genre: list[str]
    cover_id: int | None = None


class AddReadingMaterial(SQLModel):
    """Form data when user adds a book to their library"""

    cover_id: int
    year: int
    title: str
    author: str
    genre: list[str]
    total_pages: int
    current_page: int
    status: bool
    start_date: datetime
    last_read_at: datetime
    cover_id: int | None = None


class MaterialResume(SQLModel):
    """Book summary for user's reading history list"""

    cover_id: int
    year: int
    title: str
    author: str
    status: bool
    genre: list[str]
    last_read_at: datetime
    cover_id: int | None = None
