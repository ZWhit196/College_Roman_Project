# -*- coding: utf-8 -*-

import os
import traceback

from flask import Flask, request, jsonify, session
from flask_login import LoginManager
from flask.templating import render_template

from Database import db
from models import User
from helpers.error_helper import Get_error
from views.URLRouter import url_router


def createNewKey():
    return os.urandom(64)


# set up and configure app
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ConvAndUser.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    login_manager = LoginManager() # login manager
    login_manager.init_app(app)
    login_manager.login_view = ''
    @login_manager.user_loader # keeps the user in the session
    def load_user(Email):
        return User.query.get( Email )
    @app.errorhandler(400)
    @app.errorhandler(401)
    @app.errorhandler(404)
    @app.errorhandler(500)
    def error_loading(ex):
        errs = {400: "There was an issue with the request.", 401: "Access is denied.", 404: "This page/resource was not found.", 410: "This page/resource has been removed or has expired.", 500: "An internal server error occured."}
        if request.method == "POST":
            return Get_error('SERVER')
        return render_template("error.html", err=ex.code, msg=errs[ex.code])
    app.register_blueprint(url_router) # blueprints
    app.secret_key = "a"#createNewKey()
    return app

def setup_database(app):
    with app.app_context():
        db.create_all()

		
if __name__ == "__main__":
    app = create_app()
    if not os.path.isfile('ConvAndUser.db'):
        setup_database(app)
    app.run(host="0.0.0.0", port=8910, debug=True)