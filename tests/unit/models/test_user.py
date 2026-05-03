import pytest
from sqlmodel import select
from app.models.user import User
from app.core.security import hash_password, verify_password


class TestUser:

    def test_sucess_create_user(self, db_session):

        test_user_1 = User(
            username="username1",
            email="testemail@test.com",
            hash_password=hash_password("password"),
        )

        db_session.add(test_user_1)
        db_session.commit()

        assert test_user_1.id is not None
        assert verify_password("password", test_user_1.hash_password)
        assert test_user_1.username == "username1"

    def test_failed_create_user(self, db_session):

        invalid_test_user = User(
            username=None,
            email="testemail@test.com",
            hash_password=hash_password("password"),
        )

        db_session.add(invalid_test_user)

        with pytest.raises(Exception):
            db_session.commit()

    def test_duplicate_email(self, db_session):
        test_user_2 = User(
            username="username2",
            email="testemail@test.com",
            hash_password=hash_password("password2"),
        )

        db_session.add(test_user_2)

        with pytest.raises(Exception):
            db_session.commit()

    def test_duplicate_username(self, db_session):
        test_user_3 = User(
            username="username1",
            email="testemail3@test.com",
            hash_password=hash_password("password3"),
        )

        db_session.add(test_user_3)

        with pytest.raises(Exception):
            db_session.commit()

    def test_get_user_by_email(self, db_session):
        stmt = select(User).where(User.email == "testemail@test.com")
        user = db_session.exec(stmt).first()

        assert user.id is not None
        assert user.id == 1
        assert user.username == "username1"
