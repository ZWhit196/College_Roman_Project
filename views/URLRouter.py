import traceback
import time

from flask import Blueprint, request, json, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask.templating import render_template

from helpers.error_helper import Get_error
from models import User

from helpers.Data_Interface import DBInterface
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
        DBInterface().Create_new_user(email, name, password)
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
    name = current_user.Name
    data = request.data
    data = data.decode("utf-8")
    data = json.loads(data)
    print(data)
    
    number = request.args.get("number",None,type=str)
    ts = time.time()
    
    print(name, number, ts)
    # So, add to db first
    # Then return to user
    
    return json.dumps( {"lol": "no"} )



@url_router.route("/stats", methods=['GET','POST'])
def stats():
	if request.method == "POST":
		data = DBInterface().Get_all_data()
		print(data)
		
        # Sort out the pull
        
		item_dict = {}
		number_dict = {}
		for item in data:
			it = datetime.datetime.strftime( datetime.datetime.fromtimestamp(item['Time'] ) , "%d/%m/%Y")
			if it in item_dict:
				item_dict[ it ] += 1
			else:
				item_dict[ it ] = 1
			num = item['Number']
			if num in number_dict:
				number_dict[ num ] += 1
			else:
				number_dict[ num ] = 1
		days_list = []
		nums_list = []
		day_sort = sorted( list(item_dict.keys()) )
		num_sort = sorted( list(number_dict.keys()) )
		for day in day_sort:
			l = []
			l.append( day )
			l.append( item_dict[day] )
			days_list.append(l)
		for num in num_sort:
			n = []
			n.append( num )
			n.append( number_dict[num] )
			nums_list.append(n)
		ret = {'Numbers': nums_list, 'Times': days_list}
		return json.dumps( ret )
	return render_template('stats.html')