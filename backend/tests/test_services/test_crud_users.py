import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User
from app.crud import users


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_create_user(db_session):
    user = users.create_user(db_session, "test@example.com", "hashed_pass")
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.password_hash == "hashed_pass"

    users_in_db = db_session.query(User).all()
    assert len(users_in_db) == 1


def test_get_user_by_email(db_session):
    users.create_user(db_session, "test@example.com", "pass123")

    user = users.get_user_by_email(db_session, "test@example.com")
    assert user is not None
    assert user.email == "test@example.com"

    assert users.get_user_by_email(db_session, "none@example.com") is None


def test_get_user_by_id(db_session):
    new_user = users.create_user(db_session, "test@example.com", "pass123")

    user = users.get_user_by_id(db_session, new_user.id)
    assert user is not None
    assert user.email == "test@example.com"

    assert users.get_user_by_id(db_session, 999) is None


def test_update_user_password(db_session):
    user = users.create_user(db_session, "test@example.com", "old_pass")

    updated_user = users.update_user_password(db_session, user, "new_pass")
    assert updated_user.password_hash == "new_pass"

    refreshed_user = users.get_user_by_id(db_session, user.id)
    assert refreshed_user.password_hash == "new_pass"
