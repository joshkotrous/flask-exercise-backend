import jwt
import jwt.algorithms
from dto.credentials import CredentialsSchema
from flask import Blueprint, jsonify, request
from sqlalchemy import select
from werkzeug.security import check_password_hash

from backend import db
from backend.entities.user import User
from backend.routes import secret_token

auth_bp = Blueprint("auth", __name__)
credentials_schema = CredentialsSchema()


@auth_bp.route("/login", methods=["POST"])
def login():
    d = request.json
    credentials = credentials_schema.load(d)
    user = db.session.scalars(
        select(User).where(User.username == credentials.username)
    ).one()

    if not check_password_hash(user.password, credentials.password):
        raise Exception("invalid password")

    encoded_jwt = jwt.encode(
        {"sub": user.id, "name": user.username}, secret_token, algorithm="HS256"
    )

    return jsonify({"token": encoded_jwt})
