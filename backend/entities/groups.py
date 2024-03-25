from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy.orm import relationship

from backend import db
from backend.entities.user import User

users_to_groups_association = db.Table(
    "user_to_groups_association",
    db.Column("user_id", db.Integer, db.ForeignKey(User.id), primary_key=True),
    db.Column("group_id", db.Integer, db.ForeignKey("group_id"), primary_key=True),
)


class Group(db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    users = relationship(
        User.__name__, secondary=users_to_groups_association, backref="groups"
    )


class GroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Group
        include_relationships = True
        load_instance = True
