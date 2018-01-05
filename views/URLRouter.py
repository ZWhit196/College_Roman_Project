import traceback
import datetime

from flask import Blueprint, request, json, jsonify, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask.templating import render_template

from helpers.error_helper import Get_error
from models import User

from helpers import Data_Interface
from helpers import Value_interpreter
from flask.helpers import url_for

url_router = Blueprint('url_router', __name__, template_folder='templates')

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Home page
#
@url_router.route("/", methods=["GET"])
def home():
    return render_template("front/index.html")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Account pages
#
@url_router.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for("url_router.menu"))
        return render_template('login/login.html')
    
    email = request.form['email']
    password = request.form['password']
    registered_user = User.query.filter_by(Email=email.lower()).first()
    if registered_user is None:
        flash('Email or Password is invalid.', 'error')
        return redirect(url_for('url_router.login'))
    
    if registered_user.verify_password(password):
        login_user(registered_user, remember=True)
        return redirect(url_for('url_router.menu'))
    
    flash('Email or Password is invalid.', 'error')
    return redirect(url_for('url_router.login'))
    

@url_router.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('url_router.home'))
    

@url_router.route("/register/", methods=['GET','POST'])
def register():
    if request.method == "GET":
        return render_template("login/register.html")
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    existing_user = User.query.filter_by(Email=email.lower()).first()
    if existing_user is None:
        Data_Interface.Interface().Create_new_user(email, name, password)
        return redirect(url_for('url_router.login'))
    flash("User email is already taken.")
    return redirect(url_for('url_router.register'))
    
@url_router.route("/settings", methods=["GET","POST"])
def settings():
    if request.method == "GET":
        return render_template("user/settings.html")
    form = dict( request.form )
    current_user.update_details( form['name'][0], form['password'][0], form['theme'][0] )
    flash("User details updated.")
    return redirect(url_for("url_router.settings"))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Convert & stats pages
#
@url_router.route("/menu", methods=['GET'])
@login_required
def menu():
    return render_template("user/user_menu.html")


@url_router.route("/convert",methods=["GET","POST"])
@login_required
def convert():
    if request.method == "GET":
        return render_template("user/convert.html")

    data = request.data
    data = data.decode("utf-8")
    data = json.loads(data)
    number = data.get("val")
    try:
        number = int(number)
    except:
        pass
    ts = datetime.date.today().strftime("%d/%m/%Y")
    
    # convert
    VI = Value_interpreter.Translator()
    conv = VI.Evaluate_value(number)
    if conv is None:
        return Get_error("DATA")
    
    # then, add to db first
    DB = Data_Interface.Interface()
    DB.Create_result(current_user, ts, conv)
    
    # then return to user
    if conv['Base_value'] == "Roman":
        return jsonify( {"base": conv.get("Base_value"), "val": conv.get('Value') } )
    else:
        return jsonify( {"base": conv.get("Base_value"), "val": conv.get('Roman') } )

@url_router.route("/stats", methods=['GET','POST'])
def stats():
    if request.method == "POST":
        data = Data_Interface.Interface().Get_stats_data()
        print(data)
        return jsonify( data )
    return render_template('user/stats.html')

@url_router.route("/all_results", methods=["GET","POST"])
def all_results():
    if request.method == "POST":
        data = request.data
        data = data.decode("utf-8")
        data = json.loads(data)
        page = data.get("get")
        ret = Data_Interface.Interface().Get_all_data( 20, page )
        return jsonify(ret)
    return render_template('user/all_results.html')