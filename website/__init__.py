from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "urbook"
PASS = input()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'not_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{PASS}@localhost/{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    db.create_all(app=app)

    from .views import views
    from .auth import auth

    from .models import User, Note

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
