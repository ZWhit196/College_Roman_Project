import traceback

from flask import Blueprint, request, json
from flask_login import login_user, logout_user, current_user, login_required
from flask.templating import render_template

from helpers.error_helper import Get_error
from models import User

from processes.GetData import Retrieve_data
from processes.InsertData import Insert_data
from processes.UpdateData import Update_data

url_router = Blueprint('url_router', __name__, template_folder='templates')


@url_router.route("/", methods=["GET"])
def Home():
    return render_template("index.html")


@url_router.route("/get", methods=["GET"])
@authorised_request
def Get_Data_URL():
    try:
        query_args = dict( request.args )
        ret = Retrieve_data(query_args)
        return ret
    except Exception as e:
        print("Error:", e)
        return Get_error()


@url_router.route("/post", methods=["POST"])
@authorised_request
def Send_Data_URL():
    data = request.data
    data = data.decode("utf-8")
    try:
        data = json.loads(data)
        ret = Insert_data(data)
        return ret
    except Exception as e:
        print("Error:",e,data)
        return Get_error()
    
    
@url_router.route("/update", methods=["POST"])
@authorised_request
def Update_Data_URL():
    data = request.data
    data = data.decode("utf-8")
    try:
        data = json.loads(data)
        ret = Update_data(data)
        return ret
    except Exception as e:
        print("Error:",e,data)
        return Get_error()