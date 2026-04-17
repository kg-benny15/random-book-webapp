"""
UserMaterialLink Model (Junction/Intermediate Table)

Purpose:
- Creates a Many-to-Many relationship between User and ReadingMaterial
- Stores user-specific information for each book (reading progress, dates)

Table: users_materials_links

Relationships:
- Many-to-One with User (a link belongs to one user)
- Many-to-One with ReadingMaterial (a link belongs to one book)

Why needed:
- A user can read many books
- A book can be read by many users
- Each user has different progress for the same book
"""

from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, UTC
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.reading_material import ReadingMaterial


class UserMaterialLink(SQLModel, table=True):
    """Junction table connecting User and ReadingMaterial (Many-to-Many)"""

    __tablename__ = "users_materials_links"

    # ============================================================
    # COMPOSITE PRIMARY KEY (Both fields together form the PK)
    # ============================================================

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    reading_material_id: int = Field(
        foreign_key="reading_materials.id", primary_key=True
    )

    # ============================================================
    # USER-SPECIFIC BOOK DATA (Stored per user, per book)
    # ============================================================

    current_page: int = Field(default=0, ge=0)  # Reading progress (0 = not started)
    status: bool = Field(default=False)  # False = reading, True = completed
    start_date: datetime | None = Field(default=None)  # When user started reading
    end_date: datetime | None = Field(default=None)  # When user finished
    last_read_at: datetime | None = Field(
        default_factory=lambda: datetime.now(UTC)  # Last activity timestamp
    )

    # ============================================================
    # RELATIONSHIPS (Direct access to related tables)
    # ============================================================

    # Access the User who owns this link
    user: Optional["User"] = Relationship(back_populates="reading_links")
    # Access the Book/Material this link refers to
    reading_material: Optional["ReadingMaterial"] = Relationship(
        back_populates="reading_links"
    )
