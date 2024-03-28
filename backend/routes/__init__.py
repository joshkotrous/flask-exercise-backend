import jwt
import jwt.algorithms
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from backend import db
from backend.entities.user import User

allowed_users = {
    "test": generate_password_hash("pass"),
    "josh": generate_password_hash("Password"),
}

allowed_tokens = {"token-test": "test"}

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth(scheme="Bearer")

secret_token = "mysecret"


@basic_auth.verify_password
def verify_basic_password(username, password):
    try:
        print("username: " + username)
        user = db.session.scalars(select(User).where(User.email == username)).one()
        print(user.username)
        if user is None:
            return None

        if check_password_hash(user.username, password):
            return username

    except Exception:
        print(Exception)

    return None


@token_auth.verify_token
def verify_token(token):
    try:
        decoded_jwt = jwt.decode(token, secret_token, algorithms=["HS256"])
    except Exception:
        return None
    try:
        user = db.session.scalars(
            select(User).where(User.username == decoded_jwt["name"])
        ).one()
        print(user.username)
        if user is not None:
            return decoded_jwt["name"]
    except Exception:
        print(Exception)
    # if decoded_jwt["name"] in allowed_users:
    #     return decoded_jwt["name"]
    return None

    # if token not in allowed_tokens:
    #     return None

    # return allowed_tokens[token]
