"""
Models package - defines database relationships between User and ReadingMaterial.

All relationships are centralized here to avoid circular imports.
Model classes define only fields (columns), connections are defined below.
"""

from app.models.user import User
from app.models.reading_material import ReadingMaterial
from app.models.user_material_link import UserMaterialLink

__all__ = ["User", "ReadingMaterial", "UserMaterialLink"]
