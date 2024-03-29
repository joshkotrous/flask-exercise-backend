from backend import db
from backend.entities.post import Post
from backend.entities.user import User


class Like(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    post_id = db.Column(db.Integer, db.ForeignKey(Post.id))
