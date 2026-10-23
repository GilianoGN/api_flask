from flask import Blueprint, request
from src.app import Role, db
from src.utils import requires_role
from http import HTTPStatus
from flask_jwt_extended import jwt_required

app = Blueprint("role", __name__, url_prefix="/roles")

@app.route("/", methods=["POST"])
@jwt_required()
@requires_role("admin")
def create_role():
    data = request.json
    role = Role(name=data["name"])
    db.session.add(role)
    db.session.commit()
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
    db.session.delete(role)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT