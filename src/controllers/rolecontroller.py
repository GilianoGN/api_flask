from flask import Blueprint, request
from src.models import db, Role
from src.utils import requires_role
from src.views.roleview import RoleSchemaAll, CreateRoleSchema
from http import HTTPStatus
from sqlalchemy import inspect # type: ignore
from flask_jwt_extended import jwt_required # type: ignore
from marshmallow import ValidationError # type: ignore

app = Blueprint("role", __name__, url_prefix="/roles")

@app.route("/", methods=["POST"])
@jwt_required()
@requires_role("admin")
def create_role():
    """Create a role
    ---
    post:
        tags:
            - role
        summary: Create a new role (Apenas Administradores)
        description: Create a new role with name
        requestBody:
            required: true
            content:
                application/json:
                    schema: CreateRoleSchema
        responses:
            201:
                description: Role created successfully
            400:
                description: Incomplete data for role creation
            422:
                description: Validation error
        security:
            - BearerAuth: []
    """
    role_schema = CreateRoleSchema()

    try:
        data = role_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    if not data or not data.get("name"):
        return {"error": "Dados incompletos para criação da role."}, HTTPStatus.BAD_REQUEST

    try:
        role = Role(name=data["name"])
        db.session.add(role)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": "Erro ao salva a role no banco de dados."}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    return {"message": "Role created!"}, HTTPStatus.CREATED

@app.route("/", methods=["GET"])
@jwt_required()
@requires_role("visitante")
def list_role():
    """List role view
    ---
    get:
        tags:
            - role
        summary: List all roles
        description: Retrieves a list of all registered roles
        responses:
            200:
                description: Successful operation
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                role:
                                    type: array
                                    items:
                                        Schema: RoleSchemaAll
        security:
            - BearerAuth: []
    """
    query = db.select(Role)
    roles = db.session.execute(query).scalars()
    roles_schema = RoleSchemaAll(many=True)
    list = roles_schema.dump(roles)

    return {"roles": list}, HTTPStatus.OK

@app.route("/<int:role_id>", methods=["DELETE"])
@jwt_required()
@requires_role("admin")
def delete_role(role_id):
    """Role delete view
    ---
    delete:
        tags:
            - role
        summary: Deletes a role (Apenas Administradores)
        description: delete a role
        parameters:
            - in: path
              name: role_id
              schema: RoleIdParameter
        responses:
            204:
                description: Successful operation
            400:
                description: Cannot delete role with associated users
            404:
                description: Not found role
        security:
            - BearerAuth: []
    """
    role = db.get_or_404(Role, role_id)
    if role.user:
        return {"message": "Cannot delete role with associated users"}, HTTPStatus.BAD_REQUEST
    
    db.session.delete(role)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT

# Lista de view do Role para a APISpec
ROLE_VIEWS = [
    create_role,
    list_role,
    delete_role
]