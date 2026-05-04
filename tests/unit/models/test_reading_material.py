import pytest
from sqlmodel import select
from app.models import ReadingMaterial


class TestReadingMaterial:

    def test_create_reading_material(self, db_session):

        reading_material_1 = ReadingMaterial(
            work_id="test_w-id",
            title="Test Book Title 1",
            author="Test Author 1",
            material_type="book",
        )

        db_session.add(reading_material_1)
        db_session.commit()

        assert reading_material_1.id is not None
        assert reading_material_1.work_id == "test_w-id"
        assert hasattr(reading_material_1, "total_pages")

    def test_failed_create_reading_material(self, db_session):

        reading_material_2 = ReadingMaterial(
            work_id="test_w-id",
            title=None,
            author="Test Author 1",
            material_type="book",
        )

        db_session.add(reading_material_2)

        with pytest.raises(Exception):
            db_session.commit()

    def test_get_reading_material_by_work_id(self, db_session):

        stmt = select(ReadingMaterial).where(ReadingMaterial.work_id == "test_w-id")
        reading_material = db_session.exec(stmt).first()

        assert reading_material.id is not None
        assert reading_material.id == 1
        assert reading_material.title == "Test Book Title 1"
