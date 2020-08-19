from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt

# instantiate the extensions
db = SQLAlchemy()
admin = Admin(template_mode="bootstrap3")
cors = CORS()
bcrypt = Bcrypt()