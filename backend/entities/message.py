from sqlalchemy.orm import relationship

from backend import db
from backend.entities.user import User


class Message(db.Model):
    __tablename__ = "message"

    id = id.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.Datetime(timezone=True), default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)

    user = relationship(User.__name__, backref="messages", cascade="all")
