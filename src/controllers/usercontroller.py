from flask import Blueprint, request
from src.models import db, User
from src.utils import requires_role
from http import HTTPStatus
from sqlalchemy import inspect
from flask_jwt_extended import jwt_required

app = Blueprint("user", __name__, url_prefix="/users")

@app.route("/", methods=["POST"])
@jwt_required()
@requires_role("admin")
def create_user():
    data = request.json
    user = User(
        username=data["username"],
        active=data["active"],
        password=data["password"],
        role_id=data["role_id"],
    )
    db.session.add(user)
    db.session.commit()

    return {"message": "User created!"}, HTTPStatus.CREATED

@app.route("/", methods=["GET"])
@jwt_required()
@requires_role("visitante")
def list_user():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    list = [
        {
            "id": user.id,
            "username":user.username,
            "active":user.active,
            "role":{
                "id": user.role.id,
                "name": user.role.name,
            },
        }
        for user in users
    ]

    return {"users": list}, HTTPStatus.OK

@app.route("/<int:user_id>")
@jwt_required()
@requires_role("admin")
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
        "id": user.id,
        "username": user.username,
        "active":user.active,
        "role":{
            "id": user.role.id,
            "name": user.role.name,
        },
        "password":user.password,
    }

@app.route("/<int:user_id>", methods=["PATCH"])
@jwt_required()
@requires_role("admin")
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json

    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()

    return {
        "id": user.id,
        "username": user.username,
        "active":user.active,
        "password":user.password,
    }

@app.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@requires_role("admin")
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT