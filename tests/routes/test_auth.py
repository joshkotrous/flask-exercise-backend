from flask import url_for


def test_auth_no_user(app_with_db):
    # when
    response = app_with_db.post(
        url_for("auth.login"), json={"username": "test", "password": "pass"}
    )

    # then
    assert response.status_code == 404


def test_auth(app_with_data):
    # when
    response = app_with_data.post(
        url_for("auth.login"), json={"username": "test", "password": "pass"}, headers={}
    )

    # then
    assert response.status_code == 200

    data = response.json
    assert "token" in data
