from api.main import app
from api.database import get_session
from api.database import Base
from api.tests.db_tests import test_engine
from api.tests.db_tests import override_get_session

from starlette.testclient import TestClient

Base.metadata.create_all(test_engine)

app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)

# fake_test_db = {
#     "staff": {"username": "staff", "birthdate": "1998-03-09"},
#     "notallowed_username": {"username": "test1234", "birthdate": "1984-04-23"},
#     "notallowed_birthdate": {"username": "admin", "birthdate": "2023-06-23"}, # future and current dates not allowed
# }

def test_create_user():
    response = client.post(
        "/hello",
        json={"username": "staff", "birthdate": "1998-03-09"}
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["username"] == "staff"
    assert "1998-03-09" == data["birthdate"]
    username = data["username"]

    # check that the user was actually created
    response = client.get(f"/hello/{username}")
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["status"] == "success"
    assert data["birthdate"] == "1998-03-09"
    assert data["username"] == username


# def test_create_user_bad_username():
#     response = client.post(
#         "/hello/",
#         json={"username": "test1234", "birthdate": "2004-03-12"},
#     )
#     assert response.status_code == 201
#     assert response == "Username must contain letters only and Birthday must be in the past."

# def test_create_user_bad_birthdate():
#     response = client.post(
#         "/hello/",
#         json={"username": "usernameok", "birthdate": "2023-04-20"},
#     )
#     assert response.status_code == 201
#     assert response == "Username must contain letters only and Birthday must be in the past."

# def test_create_existing_username():
#     response = client.post(
#         "/hello/",
#         json={
#             "username": "staff",
#             "birthdate": "1997-03-09"
#         },
#     )
#     assert response.status_code == 201
#     assert response.json() == {
#     "staff": "Username already exists, make sure to pass a unique username ID"
#     }

# def test_read_username():
#     response= client.get("/hello/staff")
    # assert response.status_code == 200
    # assert response == "Hello, staff! Your birthday is in 356 day(s)"

# def test_read_non_existing_username():
#     response = client.get("/items/capitan")
#     assert response.status_code == 404 # no content

# def test_read_birthday_user():
#     response = client.post(
#         "/hello/",
#         json={"username": "staff", "birthdate": "1998-03-09"},
#     )
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["username"] == "staff"
#     assert "1998-03-09" in data
#     username = data["username"]

#     response = client.get(f"/hello/{username}")
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert data["birthdate"] == "1998-03-09"
#     assert data["username"] == username


    # response = client.get("/hello/today")
    # assert response.status_code == 200
    # assert response == "Hello, today! Happy birthday!" # this user has their birthday today

# def test_update_user():
#     response = client.patch(
#         "/hello/",
#         json={
#             "username": "staff",
#             "birthdate": "1999-05-29"
#         },
#     )
#     assert response.status_code == 200
#     assert response.json() == {
#             "status": "success",
#             "user": {
#                 "birthdate": "1999-05-29",
#                 "id": 1,
#                 "username": "staff"
#             }
#         }
    
# def test_update_non_existing_user():
#     response = client.patch(
#         "/hello/",
#         json={
#             "username": "client",
#             "birthdate": "1999-05-29"
#         },
#     )
#     assert response.status_code == 200
#     assert response.json() == {"detail": "user item with username `client` not found"}