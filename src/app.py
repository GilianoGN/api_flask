import os

from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from src.models import db

migrate = Migrate()
jwt = JWTManager()

def create_app(environment=os.environ["ENVIRONMENT"]):
    # criar e configurar o app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"src.cofig.{environment.title()}Config")

    # Instancia pasta existente
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # register blueprints
    from src.controllers import usercontroller, postcontroller, authcontroller, rolecontroller

    app.register_blueprint(usercontroller.app)
    app.register_blueprint(postcontroller.app)
    app.register_blueprint(authcontroller.app)
    app.register_blueprint(rolecontroller.app)

    return app