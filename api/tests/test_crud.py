import pytest
from api.main import app
from api.database import get_session
from api.database import Base
from api.tests.db_tests import test_engine
from api.tests.db_tests import override_get_session

from starlette.testclient import TestClient


@pytest.fixture()
def test_db():
    """
    Ensuring that we setup and teardown 
    test data at the end of the test suite.
    """
    Base.metadata.create_all(bind=test_engine)

    yield
    Base.metadata.drop_all(bind=test_engine)


app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)

fake_test_db = {
    "staff": {"username": "staff", "birthdate": "1983-06-19"},
    "bad_username": {"username": "test1234", "birthdate": "1984-04-23"},
    "bad_birthdate": {"username": "unix", "birthdate": "2023-06-23"}, # future and current dates not allowed
}

def test_create_user(test_db):
    username = fake_test_db["staff"]["username"]
    birthdate = fake_test_db["staff"]["birthdate"]

    response = client.post(
        f"/hello/{username}?birthdate={birthdate}"
    )
    assert response.status_code == 200, response.text

    # check that the user was actually created
    response = client.get(f"/hello/staff")
    assert response.status_code == 200, response.text
    assert f"Hello, {username}!" in response.text


def test_create_user_bad_username(test_db):
    username = fake_test_db["bad_username"]["username"]
    birthdate = fake_test_db["bad_username"]["birthdate"]

    response = client.post(
        f"/hello/{username}?birthdate={birthdate}"
    )
    assert "Username must contain letters only and Birthdate must be in the past." in response.text

    response = client.get(f"/hello/{username}")
    assert response.status_code == 204 # no content

def test_create_user_bad_birthdate(test_db):
    username = fake_test_db["bad_birthdate"]["username"]
    birthdate = fake_test_db["bad_birthdate"]["birthdate"]

    response = client.post(
        f"/hello/{username}?birthdate={birthdate}"
    )
    assert "Username must contain letters only and Birthdate must be in the past." in response.text

def test_read_username(test_db):
    username = fake_test_db["staff"]["username"]
    birthdate = fake_test_db["staff"]["birthdate"]

    response = client.post(
        f"/hello/{username}?birthdate={birthdate}"
    )
    response = client.get(
        f"/hello/{username}"
    )
    assert response.status_code == 200, response.text
    assert f"Hello, {username}!" in response.text

def test_update_user(test_db):
    username = fake_test_db["staff"]["username"]
    birthdate = fake_test_db["staff"]["birthdate"]

    response = client.post(
        f"/hello/{username}?birthdate={birthdate}"
    )
    assert response.status_code == 200, response.text

    # run updates
    new_birthdate = "2004-09-13"
    response = client.patch(f"/hello/{username}?birthdate={new_birthdate}")
    assert response.status_code == 200
    assert response.json()["username"] == username
    assert response.json()["birthdate"] == new_birthdate
