import re

from marshmallow import Schema, ValidationError, fields, post_load, validates

from backend.entities.user import User


class UserCreationSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.String(required=True)

    @validates("password")
    def validates_password(self, value):
        if len(value) < 8:
            raise ValidationError("Password length must be at least 8 characters.")
        if not any(c.isupper() for c in value):
            raise ValidationError("Password must contain upper case")
        if not any(c.islower() for c in value):
            raise ValidationError("Password must contain lower case")

    @validates("email")
    def validates_email(self, value):
        if not re.match("[^^]+@[^@]+\.{^@]+", value):  # noqa: W605
            raise ValidationError("Invalid email format")

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
