from flask import Blueprint, Response, jsonify, request
from sqlalchemy import insert, select
from werkzeug.security import generate_password_hash

from backend import db
from backend.dto.user_creation import UserCreationSchema
from backend.entities.country import Country
from backend.entities.user import User
from backend.routes import token_auth

users_bp = Blueprint("users", __name__, url_prefix="/api/users")
user_creation_schema = UserCreationSchema()


@users_bp.route("", methods=["GET"])
@token_auth.login_required
def get_all_users():
    # style 1
    # all_users = User.query.all()
    # return jsonify(all_users)

    # style 2 (more complex)
    users = db.session.scalars(select(User)).all()
    return jsonify([{"id": u.id, "username": u.username} for u in users])


@users_bp.route("", methods=["POST"])
@token_auth.login_required
def create_user():
    d = request.json
    new_user = user_creation_schema.load(d)

    print(d)

    # style 1
    # u = User()
    # u.username = d["username"]
    # u.email = d["email"]
    # u.password = generate_password_has(d["password"])
    # db.session.add(u)

    # style 2
    db.session.execute(
        insert(User).values(
            username=new_user.username,
            email=new_user.email,
            password=generate_password_hash(new_user.password),
        )
    )
    db.session.commit()

    return Response(status=204)


@users_bp.route("/<user_id>", methods=["GET"])
@token_auth.login_required
def get_user(user_id):
    # style 1
    # u = User.query.filter(User.is == user_id).one()

    # style 2
    user = db.session.scalars(select(User).where(User.id == user_id)).one()
    if user.country_id is not None:
        country = db.session.scalars(
            select(Country).where(Country.id == user.country_id)
        ).one()
        return jsonify(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "country": country.code,
            }
        )

    return jsonify(
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "country": "",
        }
    )


@users_bp.route("/<user_id>", methods=["POST"])
@token_auth.login_required
def update_user(user_id):
    d = request.json
    userInfo = user_creation_schema.load(d)
    user = db.session.scalars(select(User).where(User.id == user_id)).one()
    if userInfo.first_name is not None:
        user.first_name = userInfo.first_name
    if userInfo.last_name is not None:
        user.last_name = userInfo.last_name
    if userInfo.email is not None:
        user.email = userInfo.email
    if userInfo.username is not None:
        user.username = userInfo.username

    db.session.commit()

    return Response(status=204)
