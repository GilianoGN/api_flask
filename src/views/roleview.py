from src.app import ma
from src.models.rolemodel import Role
from marshmallow import fields # type: ignore

class RoleSchemaAll(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        include_fk = True

class CreateRoleSchema(ma.Schema):
    name = fields.String(required=True)

class RoleIdParameter(ma.Schema):
    role_id = fields.Integer(required=True)