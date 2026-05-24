"""
Tests for UserMaterialLink (many-to-many relationship between User and ReadingMaterial).
"""

import pytest
from datetime import datetime, UTC
from app.models import User, ReadingMaterial, UserMaterialLink
from app.core.security import hash_password


class TestUserMaterialLink:

    def test_create_link(self, db_session):
        """Test creating a link between user and material."""
        user = User(
            username=f"user_{id(self)}",
            email=f"user_{id(self)}@test.com",
            hash_password=hash_password("pass"),
        )
        material = ReadingMaterial(
            work_id=f"work_{id(self)}",
            title="Test Book",
            author="Author",
            material_type="book",
        )
        db_session.add_all([user, material])
        db_session.flush()

        link = UserMaterialLink(
            user_id=user.id,
            reading_material_id=material.id,
            current_page=10,
            status=False,
        )
        db_session.add(link)
        db_session.commit()

        saved = db_session.get(UserMaterialLink, (user.id, material.id))
        assert saved is not None
        assert saved.current_page == 10
        assert not saved.status

    def test_composite_primary_key(self, db_session):
        """Test that duplicate link is rejected."""
        user = User(
            username=f"user_{id(self)}",
            email=f"user_{id(self)}@test.com",
            hash_password=hash_password("pass"),
        )
        material = ReadingMaterial(
            work_id=f"work_{id(self)}",
            title="Test Book",
            author="Author",
            material_type="book",
        )
        db_session.add_all([user, material])
        db_session.flush()

        link1 = UserMaterialLink(user_id=user.id, reading_material_id=material.id)
        db_session.add(link1)
        db_session.commit()

        link2 = UserMaterialLink(user_id=user.id, reading_material_id=material.id)
        db_session.add(link2)
        with pytest.raises(Exception):
            db_session.commit()

    def test_user_access_materials(self, db_session):
        """Test user.reading_materials relationship."""
        user = User(
            username=f"user_{id(self)}",
            email=f"user_{id(self)}@test.com",
            hash_password=hash_password("pass"),
        )
        material = ReadingMaterial(
            work_id=f"work_{id(self)}",
            title="Test Book",
            author="Author",
            material_type="book",
        )
        db_session.add_all([user, material])
        db_session.flush()

        user.reading_materials.append(material)
        db_session.commit()

        assert material in user.reading_materials
        assert len(user.reading_materials) == 1

    def test_material_access_users(self, db_session):
        """Test material.users relationship."""
        user = User(
            username=f"user_{id(self)}",
            email=f"user_{id(self)}@test.com",
            hash_password=hash_password("pass"),
        )
        material = ReadingMaterial(
            work_id=f"work_{id(self)}",
            title="Test Book",
            author="Author",
            material_type="book",
        )
        db_session.add_all([user, material])
        db_session.flush()

        material.users.append(user)
        db_session.commit()

        assert user in material.users
        assert len(material.users) == 1

    def test_link_default_values(self, db_session):
        """Test default values on link."""
        user = User(
            username=f"user_{id(self)}",
            email=f"user_{id(self)}@test.com",
            hash_password=hash_password("pass"),
        )
        material = ReadingMaterial(
            work_id=f"work_{id(self)}",
            title="Test Book",
            author="Author",
            material_type="book",
        )
        db_session.add_all([user, material])
        db_session.flush()

        link = UserMaterialLink(user_id=user.id, reading_material_id=material.id)
        db_session.add(link)
        db_session.commit()

        assert link.current_page == 0
        assert not link.status
        assert link.start_date is None
        assert link.end_date is None
        assert link.last_read_at is not None

    def test_link_custom_values(self, db_session):
        """Test custom values on link."""
        user = User(
            username=f"user_{id(self)}",
            email=f"user_{id(self)}@test.com",
            hash_password=hash_password("pass"),
        )
        material = ReadingMaterial(
            work_id=f"work_{id(self)}",
            title="Test Book",
            author="Author",
            material_type="book",
        )
        db_session.add_all([user, material])
        db_session.flush()

        link = UserMaterialLink(
            user_id=user.id,
            reading_material_id=material.id,
            current_page=75,
            status=True,
            start_date=datetime(2025, 1, 1, tzinfo=UTC),
        )
        db_session.add(link)
        db_session.commit()

        assert link.current_page == 75
        assert link.status
        assert link.start_date is not None

    def test_user_can_have_multiple_materials(self, db_session):
        """Test one user -> many materials."""
        user = User(
            username=f"user_{id(self)}",
            email=f"user_{id(self)}@test.com",
            hash_password=hash_password("pass"),
        )
        m1 = ReadingMaterial(
            work_id=f"work1_{id(self)}",
            title="Book 1",
            author="Author",
            material_type="book",
        )
        m2 = ReadingMaterial(
            work_id=f"work2_{id(self)}",
            title="Book 2",
            author="Author",
            material_type="book",
        )
        db_session.add_all([user, m1, m2])
        db_session.flush()

        user.reading_materials.extend([m1, m2])
        db_session.commit()

        assert len(user.reading_materials) == 2
        assert m1 in user.reading_materials
        assert m2 in user.reading_materials

    def test_material_can_have_multiple_users(self, db_session):
        """Test one material -> many users."""
        material = ReadingMaterial(
            work_id=f"work_{id(self)}",
            title="Test Book",
            author="Author",
            material_type="book",
        )
        u1 = User(
            username=f"user1_{id(self)}",
            email=f"user1_{id(self)}@test.com",
            hash_password=hash_password("pass"),
        )
        u2 = User(
            username=f"user2_{id(self)}",
            email=f"user2_{id(self)}@test.com",
            hash_password=hash_password("pass"),
        )
        db_session.add_all([material, u1, u2])
        db_session.flush()

        material.users.extend([u1, u2])
        db_session.commit()

        assert len(material.users) == 2
        assert u1 in material.users
        assert u2 in material.users

    def test_different_progress_per_user(self, db_session):
        """Test each user has independent progress."""
        material = ReadingMaterial(
            work_id=f"work_{id(self)}",
            title="Test Book",
            author="Author",
            material_type="book",
        )
        u1 = User(
            username=f"user1_{id(self)}",
            email=f"user1_{id(self)}@test.com",
            hash_password=hash_password("pass"),
        )
        u2 = User(
            username=f"user2_{id(self)}",
            email=f"user2_{id(self)}@test.com",
            hash_password=hash_password("pass"),
        )
        db_session.add_all([material, u1, u2])
        db_session.flush()

        u1.reading_materials.append(material)
        u2.reading_materials.append(material)
        db_session.commit()

        link1 = db_session.get(UserMaterialLink, (u1.id, material.id))
        link2 = db_session.get(UserMaterialLink, (u2.id, material.id))
        link1.current_page = 30
        link2.current_page = 80
        db_session.commit()

        assert link1.current_page == 30
        assert link2.current_page == 80
