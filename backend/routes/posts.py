from flask import Blueprint, Response, jsonify, request
from sqlalchemy import insert, select

from backend import db
from backend.dto.post_creation import PostCreationSchema
from backend.entities.post import Post
from backend.routes import token_auth

posts_bp = Blueprint("posts", __name__, url_prefix="/api/posts")
post_creation_schema = PostCreationSchema()


@posts_bp.route("", methods=["GET"])
@token_auth.login_required
def get_all_posts():
    posts = db.session.scalars(select(Post)).all()
    return jsonify(
        [
            {
                "post_id": post.id,
                "user_id": post.user_id,
                "author": post.author.username,
                "likes": post.likes,
                "content": post.content,
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
        insert(Post).values(
            user_id=new_post.user_id, content=new_post.content, likes=new_post.likes
        )
    )
    db.session.commit()

    return Response(status=204)


@posts_bp.route("/<post_id>/like", methods=["POST"])
@token_auth.login_required
def like_post(post_id):
    db.session.query(Post).filter(Post.id == post_id).update(
        {Post.likes: Post.likes + 1}
    )
    db.session.commit()

    return Response(status=204)
