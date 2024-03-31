from sqlalchemy.orm import backref, relationship

from backend import db
from backend.entities.user import User


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    content = db.Column(db.String(500), nullable=False)
    attachments = db.Column(db.String(500), nullable=True)
    likes = db.relationship("Like", lazy="dynamic")

    @property
    def like_count(self):
        return self.likes.count()

    # @property
    def isLiked(self, user_id):
        return self.likes.filter_by(user_id=user_id).first() is not None

    author = relationship(User, backref=backref("posts", lazy="dynamic"))
