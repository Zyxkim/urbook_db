from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "postgres"
PASS = input()
UPLOAD_FOLDER = input()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'not_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{PASS}@localhost/{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .test import tests

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(tests, url_prefix='/')

    from .models import User

    db.create_all(app=app)

    from .views import views
    from .auth import auth

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
