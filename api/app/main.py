from flask import Blueprint, render_template, request
from app.db import connect, call_sp
import json
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
def profile():
    return render_template('profile.html')

@main.route('/destination')
def destination():
    return render_template('destination.html')

@main.route('/activity')
def activity():
    return render_template('activity.html')

@main.route("/api/find_city_by_name", methods=["POST"])
def find_city_by_name():
    data  = request.json or {}
    query = "select cityid from public.find_cityid_byname('{}')".format(data["City"])
    dataset= connect(query)
    datadict = {}
    datadict["City"] = data["City"]
    datadict["CityId"] = dataset[0][0]
    json_data = json.dumps(datadict)
    return json_data

@main.route("/api/find_city_spotids", methods=["POST"])
def find_city_spotids():
    data  = request.json or {}
    query = "select spotid from public.find_city_spotids('{}')".format(data["City"])
    dataset= connect(query)
    datadict = {}
    datadict["City"] = data["City"]
    datadict["SpotIds"] = [x[0] for x in dataset]
    json_data = json.dumps(datadict)
    return json_data

@main.route("/api/find_city_cost", methods=["POST"])
def find_city_cost():
    data  = request.json or {}
    query = "select avghotelcost, avgmealcost, avgcarental from public.find_citycost({})".format(data["CityId"])
    dataset= connect(query)
    datadict = {}
    datadict["CityId"] = data["CityId"]
    datadict["AvgHotelCost"] = dataset[0][0]
    datadict["AvgMealCost"] = dataset[0][1]
    datadict["AvgCarRental"] = dataset[0][2]
    json_data = json.dumps(datadict)
    return json_data

@main.route("/api/add_new_user", methods=["POST"])
def add_new_user():
    """ 
    Input Json Example
    {
      "username": "purvis",
      "password": "password",
      "createon": "2021/04/05T12:00:00",
      "gender": "male",
      "familyname": "test",
      "givenname": "purvis",
      "birthday": "1990-01-01",
      "homecityid": "123",
      "email": "test@test.com"
    }
    Return Json Example
    {"ReturnCode": 200}
    """
    data  = request.json or {}
    params = []
    params.append((data["username"], "text"))
    params.append((data["password"], "text"))
    params.append((data["createon"], "text"))
    params.append((data["gender"], "text"))
    params.append((data["familyname"], "text"))
    params.append((data["givenname"], "text"))
    params.append((data["birthday"], "text"))
    params.append((data["homecityid"], "text"))
    params.append((data["email"], "text"))
    sp = "add_new_user"
    dataset= call_sp(sp, params)
    datadict = {}
    if dataset is not None:
       datadict["ReturnCode"] = dataset[0][0]
    else:
       datadict["ReturnCode"] = 200
    json_data = json.dumps(datadict)
    return json_data

@main.route("/api/update_rating", methods=["POST"])
def update_rating():
    """ 
    Input Json Example
    {
      "spotid": "96",
      "rating": "5.0",
    }
    Return Json Example
    {"ReturnCode": 200}
    """
    data  = request.json or {}
    params = []
    params.append((data["spotid"], "text"))
    params.append((data["rating"], "text"))
    sp = "update_rating"
    dataset= call_sp(sp, params)
    datadict = {}
    if dataset is not None:
       datadict["ReturnCode"] = dataset[0][0]
    else:
       datadict["ReturnCode"] = 200
    json_data = json.dumps(datadict)
    return json_data
