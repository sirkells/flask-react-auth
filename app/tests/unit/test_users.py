import json

# from app import db
from app.api.models import User


def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"username": "michael", "email": "michael@testdriven.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "michael@testdriven.io was added!" in data["message"]


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post("/users", data=json.dumps({}), content_type="application/json",)
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"email": "john@testdriven.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        "/users",
        data=json.dumps({"username": "michael", "email": "michael@testdriven.io"}),
        content_type="application/json",
    )
    resp = client.post(
        "/users",
        data=json.dumps({"username": "michael", "email": "michael@testdriven.io"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That email already exists." in data["message"]


def test_single_user(test_app, test_database, add_user):
    user = add_user("jeffrey", "jeffrey@testdriven.io")
    client = test_app.test_client()
    resp = client.get(f"/users/{user.id}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "jeffrey" in data["username"]
    assert "jeffrey@testdriven.io" in data["email"]


def test_single_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_all_users(test_app, test_database, add_user):
    test_database.session.query(User).delete()
    add_user("michael", "michael@mherman.org")
    add_user("fletcher", "fletcher@notreal.com")
    client = test_app.test_client()
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert "michael" in data[0]["username"]
    assert "michael@mherman.org" in data[0]["email"]
    assert "fletcher" in data[1]["username"]
    assert "fletcher@notreal.com" in data[1]["email"]


# def test_remove_user(test_app, test_database, add_user):
#     test_database.session.query(User).delete()
#     user = add_user("user-to-be-removed", "remove-me@testdriven.io")
#     client = test_app.test_client()
#     resp_one = client.get("/users")
#     data = json.loads(resp_one.data.decode())
#     assert resp_one.status_code == 200
#     assert len(data) == 1
#     resp_two = client.delete(f"/users/{user.id}")
#     data = json.loads(resp_two.data.decode())
#     assert resp_two.status_code == 200
#     assert 'remove-me@testdriven.io was removed!' in data['message']
#     resp_three = client.get("/users")
#     data = json.loads(resp_three.data.decode())
#     assert resp_three.status_code == 200
#     assert len(data) == 0


# def test_remove_user_incorrect_id(test_app, test_database):
#     client = test_app.test_client()
#     resp = client.delete("/users/999")
#     data = json.loads(resp.data.decode())
#     assert resp.status_code == 404
#     assert "User 999 does not exist" in data["message"]


# # normal run
# $ docker-compose exec users python -m pytest "project/tests"

# # disable warnings
# $ docker-compose exec users python -m pytest "project/tests" -p no:warnings

# # run only the last failed tests
# $ docker-compose exec users python -m pytest "project/tests" --lf

# # run only the tests with names that match the string expression
# $ docker-compose exec users python -m pytest "project/tests" -k "config and not test_development_config"

# # stop the test session after the first failure
# $ docker-compose exec users python -m pytest "project/tests" -x

# # enter PDB after first failure then end the test session
# $ docker-compose exec users python -m pytest "project/tests" -x --pdb

# # stop the test run after two failures
# $ docker-compose exec users python -m pytest "project/tests" --maxfail=2

# # show local variables in tracebacks
# $ docker-compose exec users python -m pytest "project/tests" -l

# # list the 2 slowest tests
# $ docker-compose exec users python -m pytest "project/tests" --durations=2
