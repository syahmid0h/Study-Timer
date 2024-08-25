from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '2M1P'

    from .views import views
    from .auth import auth

    return app