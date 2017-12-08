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
@login_required
def Get_Data_URL():
    try:
        query_args = dict( request.args )
        ret = Retrieve_data(query_args)
        return ret
    except Exception as e:
        print("Error:", e)
        return Get_error()
    
    
@router.route("/convert/",methods=["GET","POST"])
@login_required
def convert():
    name = request.args.get("name",None,type=str)
    number = request.args.get("number",None,type=str)
    base = request.args.get("base",None,type=int)
    sendDown = request.args.get("sendDown",None,type=bool)
    ts = time.time()
    print(number.isdigit(), number.isnumeric(),number)
    if isnumber(number):
        to = True
    else:
        to =False
    if to:
        try:
            number =int(str(number) [:str(number).index(".")])
            output = roman.toRoman(number)
        except:
            output = None
    else:
        try:
            output = roman.fromRoman(number)
        except:
            output = None
    if output != None :
        out = saveJSON(name,to,base,number,output,ts,root)
    return json.dumps(out)


@router.route("/stats/", methods=['GET','POST'])
def stats():
	if request.method == "POST":
		data = openJSON()
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
	return render_template(root+'/stats.html',root=root)