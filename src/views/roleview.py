from src.app import ma
from src.models.rolemodel import Role
from marshmallow import fields

class RoleSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")