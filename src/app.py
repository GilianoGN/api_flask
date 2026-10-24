import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from src.models import db

migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()

#def create_app(environment=os.environ["ENVIRONMENT"]):
def create_app(environment=None):
    if environment is None:
        environment = os.environ.get("ENVIRONMENT", "development")

    # criar e configurar o app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"src.config.{environment.title()}Config")

    # Instancia pasta existente
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # register blueprints
    from src.controllers import usercontroller, postcontroller, authcontroller, rolecontroller

    app.register_blueprint(usercontroller.app)
    app.register_blueprint(postcontroller.app)
    app.register_blueprint(authcontroller.app)
    app.register_blueprint(rolecontroller.app)

    return app