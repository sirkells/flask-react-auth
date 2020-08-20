import os

from app.extensions import admin, bcrypt, cors, db
from flask import Flask


def create_app(script_info=None):
    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)
    cors.init_app(app, resources={r"*": {"origins": "*"}})
    bcrypt.init_app(app)
    if os.getenv("FLASK_ENV") == "development":
        admin.init_app(app)

    # register api
    from app.api import api

    api.init_app(app)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    # Take note of the shell_context_processor.
    # This is used to register the app and db to the shell.
    # Now we can work with the application context and the database
    # without having to import them directly into the shell,
    # run docker-compose exec users flask shell
    # then type app and also db in the python console
    return app
