from marshmallow import Schema, fields, post_load

from backend.entities.like import Like


class LikeCreationSchema(Schema):
    post_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    liked_by_user = fields.Boolean()

    @post_load
    def make_post(self, data, **kwargs):
        return Like(**data)
