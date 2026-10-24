from flask import Blueprint, request
from src.models import db, Role
from src.utils import requires_role
from http import HTTPStatus
from flask_jwt_extended import jwt_required

app = Blueprint("role", __name__, url_prefix="/roles")

@app.route("/", methods=["POST"])
@jwt_required()
@requires_role("admin")
def create_role():
    data = request.json

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
    query = db.select(Role)
    roles = db.session.execute(query).scalars()
    list = [
        {
            "id": role.id,
            "name": role.name,
        }
        for role in roles
    ]
    return {"roles": list}, HTTPStatus.OK

@app.route("/<int:role_id>", methods=["DELETE"])
@jwt_required()
@requires_role("admin")
def delete_role(role_id):
    role = db.get_or_404(Role, role_id)
    if role.user:
        return {"message": "Cannot delete role with associated users"}, HTTPStatus.BAD_REQUEST
    
    db.session.delete(role)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT