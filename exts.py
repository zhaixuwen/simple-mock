import pymysql

pymysql.install_as_MySQLdb()

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app import app

db = SQLAlchemy(app)
jwt = JWTManager(app)
cors = CORS()
cors.init_app(app=app, resources={
    r"/*": {"origins": "*", "supports_credentials": True,
            "allow_headers": "*"}})
