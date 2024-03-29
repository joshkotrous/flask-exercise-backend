from sqlalchemy.orm import backref, relationship

from backend import db
from backend.entities.user import User


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    content = db.Column(db.String(500), nullable=False)
    likes = db.Column(db.Integer, nullable=True)

    author = relationship(User, backref=backref("posts", lazy="dynamic"))
