from flask_jwt_extended import get_jwt_identity
from src.app import User, db
from http import HTTPStatus
from functools import wraps

ROLE_NIVEL = {
    "visitante": 1,
    "normal": 2,
    "admin": 3
}

def requires_role(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.get_or_404(User, user_id)

            user_role_name = user.role.name.lower()
            required_role_name = role_name.lower()

            user_level = ROLE_NIVEL.get(user_role_name, 0)
            required_level = ROLE_NIVEL.get(required_role_name, 99)

            if user_level < required_level:
                return {"message": "User dont have access."}, HTTPStatus.FORBIDDEN
            return f(*args, **kwargs)
        return wrapped
    return decorator

def eleva_quadrado(x):
    return x**2