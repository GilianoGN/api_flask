import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from flask import Flask, json
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from src.models import db

ma = Marshmallow()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
spec = APISpec(
    title="DIO Bank",
    version="1.0.0",
    openapi_version="3.0.3",
    info=dict(description="DIO Bank API"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)
SWAGGER_URL = '/docs'
API_URL = '/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "DIO Bank API"
    }
)

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
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # register blueprints
    from src.controllers import usercontroller, postcontroller, authcontroller, rolecontroller

    app.register_blueprint(usercontroller.app)
    app.register_blueprint(postcontroller.app)
    app.register_blueprint(authcontroller.app)
    app.register_blueprint(rolecontroller.app)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    @app.route('/docs')
    def docs():
        return spec.path(view=usercontroller.delete_user).path(view=usercontroller.get_user).to_dict()

    @app.route("/swagger.json")
    def create_swagger_spec():
        from src.controllers import usercontroller
        all_views = (
            getattr(usercontroller, "USER_VIEWS", [])
        )
        for view in all_views:
            spec.path(view=view)
        return spec.to_dict()

#    @app.errorhandler(HTTPExpection)
#    def handle_exception(e):
#        response = e.get_response()
#        response.data = json.dumps(
#            {
#                "code": e.code,
#                "name": e.name,
#                "description": e.description,
#            }
#        )
#        response.content_type = "application/json"
#        return response

    return app