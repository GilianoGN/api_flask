from src.app import ma
from src.views.roleview import RoleSchema
from src.models.usermodel import User
from marshmallow import fields

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
#        fields = ("id", "username", "active", "role")
        model = User
    id = ma.auto_field()
    username = ma.auto_field()
    active = ma.auto_field()
    role = ma.Nested(RoleSchema)

class CreateUserSchema(ma.Schema):
    username = fields.String(required=True)
    active = fields.Boolean(required=True)
    password = fields.String(required=True)
    role_id = fields.Integer(required=True)

class UserSchemaAll(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True

class UserIdParameter(ma.Schema):
    user_id = fields.Integer(required=True)