"""
Models package - defines database relationships between User and ReadingMaterial.

All relationships are centralized here to avoid circular imports.
Model classes define only fields (columns), connections are defined below.
"""

from sqlmodel import Relationship
from app.models.user import User
from app.models.reading_material import ReadingMaterial
from app.models.user_material_link import UserMaterialLink

# ============================================================
# USER RELATIONSHIPS
# ============================================================

# Many-to-Many: User → ReadingMaterial (via link table)
User.reading_materials = Relationship(
    back_populates="users", link_model=UserMaterialLink
)

# One-to-Many: User → UserMaterialLink (access intermediate table fields)
User.reading_links = Relationship(back_populates="user")


# ============================================================
# READINGMATERIAL RELATIONSHIPS
# ============================================================

# Many-to-Many: ReadingMaterial → User (via link table)
ReadingMaterial.users = Relationship(
    back_populates="reading_materials", link_model=UserMaterialLink
)

# One-to-Many: ReadingMaterial → UserMaterialLink (access user-specific data)
ReadingMaterial.reading_links = Relationship(back_populates="reading_material")


# ============================================================
# USERMATERIALLINK RELATIONSHIPS (Intermediate Table)
# ============================================================

# Many-to-One: Link → User (owner of this link)
UserMaterialLink.user = Relationship(back_populates="reading_links")

# Many-to-One: Link → ReadingMaterial (target of this link)
UserMaterialLink.reading_material = Relationship(back_populates="reading_links")

__all__ = ["User", "ReadingMaterial", "UserMaterialLink"]
