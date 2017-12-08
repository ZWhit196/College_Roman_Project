# -*- coding: utf-8 -*-

import os
import traceback

from flask import Flask, request, jsonify, session
from flask.templating import render_template

from Database import db
from URLRouter import url_router


#Secret Key Generation
def createNewKey():
    return os.urandom(64)


errorMsgs = {400: "There was an issue with the request.", 
             403: "Access is denied.", 
             404: "This page/resource was not found.", 
             500: "An internal server error occured."}


# set up and configure app
def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ConvAndUser.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
	# login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = ''
    @login_manager.user_loader # keeps the user in the session
    def load_user(id):
        return User.query.get(int(id))
	
    @app.errorhandler(400) # error handlers
    @app.errorhandler(500)
    def error_loading(ex):
        return str(ex)
    
    app.register_blueprint(url_router) # blueprints
    app.secret_key = createNewKey()
    return app

def setup_database(app):
    # creates the tables in the database
    with app.app_context():
        db.create_all()

		
if __name__ == "__main__":
    app = create_app()
    if not os.path.isfile('ConvAndUser.db'):
        setup_database(app)
    app.run(host="0.0.0.0", port=8000, debug=True)