from flask import Blueprint, Response, jsonify, request
from sqlalchemy import insert, select

from backend import db
from backend.dto.like_creation import LikeCreationSchema
from backend.dto.post_creation import PostCreationSchema
from backend.entities.like import Like
from backend.entities.post import Post
from backend.routes import token_auth

posts_bp = Blueprint("posts", __name__, url_prefix="/api/posts")
post_creation_schema = PostCreationSchema()
like_creation_schema = LikeCreationSchema()


@posts_bp.route("/<user_id>", methods=["GET"])
@token_auth.login_required
def get_all_posts(user_id):
    # d = request.json

    posts = db.session.scalars(select(Post)).all()
    return jsonify(
        [
            {
                "post_id": post.id,
                "user_id": post.user_id,
                "author": post.author.username,
                "likes": post.like_count,
                "content": post.content,
                "is_liked": post.isLiked(user_id),
            }
            for post in posts
        ]
    )


@posts_bp.route("", methods=["POST"])
@token_auth.login_required
def create_post():
    d = request.json
    print(d)

    new_post = post_creation_schema.load(d)

    db.session.execute(
        insert(Post).values(user_id=new_post.user_id, content=new_post.content)
    )
    db.session.commit()

    return Response(status=204)


@posts_bp.route("/like", methods=["POST"])
@token_auth.login_required
def like_post():
    d = request.json
    like = like_creation_schema.load(d)
    post = db.session.query(Post).get(like.post_id)  # Fetch the post

    if post.isLiked(like.user_id):
        db.session.query(Like).filter(
            Like.user_id == like.user_id, Like.post_id == like.post_id
        ).delete()
    else:
        db.session.execute(
            insert(Like).values(user_id=like.user_id, post_id=like.post_id)
        )

    db.session.commit()

    return Response(status=204)
