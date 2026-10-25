from flask import Blueprint, request
from src.app import bcrypt
from src.models import db, User
from http import HTTPStatus
from flask_jwt_extended import create_access_token # type: ignore

app = Blueprint("auth", __name__, url_prefix="/auth")

def _valid_password(password_hash, password_raw):
    return bcrypt.check_password_hash(password_hash, password_raw)

@app.route("/login", methods=["POST"])
def login():
    """User Login.
    ---
    post:
        tags:
            - auth
        summary: Authenticate user and get JWT token
        description: Authenticates a user with username and password, returning an access token (Administrador - teste123)
        requestBody:
            required: true
            content:
                application/json:
                    schema:
                        type: object
                        properties:
                            username:
                                type: string
                                example: admin
                            password:
                                type: string
                                example: secret123
        responses:
            200:
                description: Token generated successfully
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                access_token:
                                    type: string
            401:
                description: Bad username or password
    """
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()

    if not user or not _valid_password(user.password, password):
        return {"message":"Bad username or password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(user.id))
    return {'access_token':access_token}

AUTH_VIEWS = [
    login
]