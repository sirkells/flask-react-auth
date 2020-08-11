from app.api.ping import ping_namespace
from app.api.users.views import users_namespace
from flask_restx import Api

api = Api(version="1.0", title="Users API", doc="/doc/")

api.add_namespace(ping_namespace, path="/ping")
api.add_namespace(users_namespace, path="/users")
