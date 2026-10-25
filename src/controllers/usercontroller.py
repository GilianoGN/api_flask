from flask import Blueprint, request
from src.app import bcrypt
from src.models import db, User
from src.utils import requires_role
from src.views.userview import UserSchema, CreateUserSchema
from http import HTTPStatus
from sqlalchemy import inspect # type: ignore
from flask_jwt_extended import jwt_required # type: ignore
from marshmallow import ValidationError # type: ignore

app = Blueprint("user", __name__, url_prefix="/users")

@app.route("/", methods=["POST"])
@jwt_required()
@requires_role("admin")
def create_user():
    """Create a user.
    ---
    post:
        tags:
            - user
        summary: Create a new user (Apenas Administradores)
        description: Creates a new user with username, password, active status, and role_id
        requestBody:
            required: true
            content:
                application/json:
                    schema: CreateUserSchema
        responses:
            201:
                description: User created successfully
            400:
                description: Incomplete data for user creation
            422:
                description: Validation error
        security:
            - BearerAuth: []
    """
    user_schema = CreateUserSchema()

    try:
        data = user_schema.load(request.json)
    except ValidationError as exc:
        return exc.messages, HTTPStatus.UNPROCESSABLE_ENTITY

    if not data or not all(data.get(k) for k in ("username", "active", "password", "role_id")):
        return {"error": "Incomplete data for user creation."}, HTTPStatus.BAD_REQUEST

    try:
        user = User(
            username=data["username"],
            active=data["active"],
            password=bcrypt.generate_password_hash(data["password"]).decode("utf-8"),
            role_id=data["role_id"],
        )
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": "Error saving the user to the database."}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    return {"message": "User created!"}, HTTPStatus.CREATED

@app.route("/", methods=["GET"])
@jwt_required()
@requires_role("visitante")
def list_user():
    """List user view.
    ---
    get:
        tags:
            - user
        summary: List all users
        description: Retrieves a list of all registered users
        responses:
            200:
                description: Successful operation
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                user:
                                    type: array
                                    items:
                                        Schema: UserSchema
        security:
            - BearerAuth: []
    """
    query = db.select(User)
    users = db.session.execute(query).scalars()
    users_schema = UserSchema(many=True)
    list = users_schema.dump(users)

    return {"users": list}, HTTPStatus.OK

@app.route("/<int:user_id>")
@jwt_required()
@requires_role("admin")
def get_user(user_id):
    """User detail view.
    ---
    get:
        tags:
            - user
        summary: Get a user (Apenas Administradores)
        description: get a user
        parameters:
            - in: path
              name: user_id
              schema: UserIdParameter
        responses:
            200:
                description: Successful operation
                content:
                    application/json:
                        schema: UserSchema
        security:
            - BearerAuth: []
    """
    user = db.get_or_404(User, user_id)
    user_schema = UserSchema()
    result = user_schema.dump(user)
    result["password"] = user.password
    return result, HTTPStatus.OK

@app.route("/<int:user_id>", methods=["PATCH"])
@jwt_required()
@requires_role("admin")
def update_user(user_id):
    """Update a user.
    ---
    patch:
        tags:
            - user
        summary: Update a user partially (Apenas Administradores)
        description: Updates specific fields of an existing user by ID
        parameters:
            - in: path
              name: user_id
              schema: UserIdParameter
        responses:
            200:
                description: Successful operation
                content:
                    application/json:
                        schema: UserSchema
            400:
                description: User not found
        security:
            - BearerAuth: []
    """
    user = db.get_or_404(User, user_id)
    data = request.json

    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()

    user_schema = UserSchema()
    result = user_schema.dump(user)
    result["password"] = user.password
    return result, HTTPStatus.OK

@app.route("/<int:user_id>", methods=["DELETE"])
@jwt_required()
@requires_role("admin")
def delete_user(user_id):
    """User delete view.
    ---
    delete:
        tags:
            - user
        summary: Deletes a user (Apenas Administradores)
        description: delete a user
        parameters:
            - in: path
              name: user_id
              schema: UserIdParameter
        responses:
            204:
                description: Successful operation
            404:
                description: Not found user
        security:
            - BearerAuth: []
    """
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return "", HTTPStatus.NO_CONTENT

# Lista de view do User para o APISpec
USER_VIEWS = [
    create_user,
    list_user,
    get_user,
    update_user,
    delete_user
]