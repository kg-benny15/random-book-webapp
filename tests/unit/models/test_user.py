"""
Tests for User model.
"""

import pytest
from sqlmodel import select
from app.models import User
from app.core.security import hash_password, verify_password


class TestUser:

    def test_create_user(self, test_user):
        """Test successful creation via fixture."""
        assert test_user.id is not None
        assert test_user.username == "test_user"
        assert test_user.email == "test@email.com"
        assert verify_password("password", test_user.hash_password)

    def test_create_new_user(self, db_session):
        """Test creating a brand new user."""
        user = User(
            username="brand_new",
            email="brand@new.com",
            hash_password=hash_password("secret"),
        )
        db_session.add(user)
        db_session.commit()

        assert user.id is not None
        assert user.username == "brand_new"
        assert user.email == "brand@new.com"

    def test_required_fields(self, db_session):
        """Test that required fields cannot be null."""
        # Missing username
        with pytest.raises(Exception):
            u = User(username=None, email="x@x.com", hash_password="hash")
            db_session.add(u)
            db_session.commit()
        db_session.rollback()

        # Missing email
        with pytest.raises(Exception):
            u = User(username="x", email=None, hash_password="hash")
            db_session.add(u)
            db_session.commit()

    def test_duplicate_username(self, db_session, test_user):
        """Test that duplicate username is rejected."""
        duplicate = User(
            username=test_user.username,
            email="different@email.com",
            hash_password="hash",
        )
        db_session.add(duplicate)
        with pytest.raises(Exception):
            db_session.commit()

    def test_duplicate_email(self, db_session, test_user):
        """Test that duplicate email is rejected."""
        duplicate = User(
            username="different_user", email=test_user.email, hash_password="hash"
        )
        db_session.add(duplicate)
        with pytest.raises(Exception):
            db_session.commit()

    def test_get_by_email(self, db_session):
        """Test query by email."""
        user = User(
            username="query_user",
            email="query@test.com",
            hash_password=hash_password("pass"),
        )
        db_session.add(user)
        db_session.commit()

        stmt = select(User).where(User.email == "query@test.com")
        found = db_session.exec(stmt).first()

        assert found is not None
        assert found.id == user.id
        assert found.username == "query_user"

    def test_get_by_username(self, db_session):
        """Test query by username."""
        user = User(
            username="unique_username",
            email="unique@test.com",
            hash_password=hash_password("pass"),
        )
        db_session.add(user)
        db_session.commit()

        stmt = select(User).where(User.username == "unique_username")
        found = db_session.exec(stmt).first()

        assert found is not None
        assert found.id == user.id
        assert found.email == "unique@test.com"

    def test_update_user(self, db_session, test_user):
        """Test updating fields."""
        test_user.username = "updated_username"
        db_session.commit()
        db_session.refresh(test_user)

        assert test_user.username == "updated_username"
