from marshmallow import Schema, fields, post_load

from backend.entities.post import Post


class PostCreationSchema(Schema):
    content = fields.String(required=True)
    user_id = fields.Integer()
    attachments = fields.String()

    @post_load
    def make_user(self, data, **kwargs):
        return Post(**data)
