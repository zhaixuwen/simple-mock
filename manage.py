from app import app
from exts import db, jwt
from views import register, login
from models import User, Apis, Result, Record


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run()
