import os
from flask import Flask
from .views import views
from .auth import auth
from .extensions import db, login_manager, bcrypt
from flask_migrate import Migrate

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SECRET_KEY'] = '2M1P'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'instance', 'database.db')

    migrate.init_app(app, db)
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app
