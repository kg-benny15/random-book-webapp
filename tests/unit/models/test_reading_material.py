"""
Tests for ReadingMaterial model.
"""

import pytest
from sqlmodel import select
from app.models import ReadingMaterial


class TestReadingMaterial:

    def test_create_reading_material(self, db_session):
        """Test successful creation."""
        material = ReadingMaterial(
            work_id="test_123",
            title="Test Book",
            author="Test Author",
            material_type="book",
        )
        db_session.add(material)
        db_session.commit()

        assert material.id is not None
        assert material.work_id == "test_123"
        assert material.title == "Test Book"

    def test_create_with_all_fields(self, db_session):
        """Test creation with optional fields."""
        material = ReadingMaterial(
            work_id="full_123",
            title="Full Book",
            author="Author",
            material_type="book",
            cover_id=999,
            year=2025,
            genre=["fiction", "adventure"],
            total_pages=300,
        )
        db_session.add(material)
        db_session.commit()

        assert material.id is not None
        assert material.cover_id == 999
        assert material.year == 2025
        assert material.genre == ["fiction", "adventure"]
        assert material.total_pages == 300

    def test_required_fields(self, db_session):
        """Test that required fields cannot be null."""
        # Missing title
        with pytest.raises(Exception):
            m = ReadingMaterial(
                work_id="x", title=None, author="a", material_type="book"
            )
            db_session.add(m)
            db_session.commit()
        db_session.rollback()

        # Missing work_id
        with pytest.raises(Exception):
            m = ReadingMaterial(
                work_id=None, title="x", author="a", material_type="book"
            )
            db_session.add(m)
            db_session.commit()

    def test_get_by_work_id(self, db_session):
        """Test query by work_id."""
        material = ReadingMaterial(
            work_id="query_123",
            title="Query Book",
            author="Author",
            material_type="book",
        )
        db_session.add(material)
        db_session.commit()

        stmt = select(ReadingMaterial).where(ReadingMaterial.work_id == "query_123")
        found = db_session.exec(stmt).first()

        assert found is not None
        assert found.id == material.id

    def test_update_fields(self, db_session, test_reading_material):
        """Test updating fields."""
        test_reading_material.title = "New Title"
        test_reading_material.total_pages = 500
        db_session.commit()
        db_session.refresh(test_reading_material)

        assert test_reading_material.title == "New Title"
        assert test_reading_material.total_pages == 500

    def test_delete(self, db_session, test_reading_material):
        """Test deletion."""
        material_id = test_reading_material.id
        db_session.delete(test_reading_material)
        db_session.commit()

        assert db_session.get(ReadingMaterial, material_id) is None

    def test_genre_default(self, test_reading_material):
        """Test that genre defaults to empty list."""
        assert test_reading_material.genre == []

    def test_genre_can_store_list(self, db_session):
        """Test storing a list in genre field."""
        material = ReadingMaterial(
            work_id="genre_test",
            title="Genre Book",
            author="Author",
            material_type="book",
            genre=["fantasy", "sci-fi"],
        )
        db_session.add(material)
        db_session.commit()
        db_session.refresh(material)

        assert material.genre == ["fantasy", "sci-fi"]
