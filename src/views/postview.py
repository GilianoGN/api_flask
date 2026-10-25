from src.app import ma
from src.views.userview import UserIdParameter
from src.models.postmodel import Post
from marshmallow import fields # type: ignore

class PostSchemaAll(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_fk = True

class CreatePostSchema(ma.Schema):
    author_id = fields.Integer(required=True)
    title = fields.String(required=True)
    body = fields.String(required=True)

class PostIdParameter(ma.Schema):
    post_id = fields.Integer(required=True)