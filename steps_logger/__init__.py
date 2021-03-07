from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_cors import CORS
from .models import db, db_drop_and_create_all, setup_db



def create_app():
    app = Flask(__name__)

    setup_db(app)
    CORS(app)
    '''
    Priya Note to the reviewer:
    Uncomment the following line to initialize the datbase on FIRST RUN
   '''
    db_drop_and_create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
