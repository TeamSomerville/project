from app import app
from app.db import connect
import json
from flask import request

@app.route("/")
@app.route("/index")
def index():
    return "Hello World!"

@app.route("/api/users")
def get_users():
    """ This returns users """
    data = {
        "id": 123,
        "username": "test"
    }
    return data

@app.route("/api/city")
def get_cities():
    """ This returns cities """
    data = connect()
    datadict = {}
    datadict["City"] = data[0]
    datadict["Country"] = data[1]
    json_data = json.dumps(datadict)
    return json_data

@app.route("/api/find_city_by_name", methods=["POST"])
def find_city_by_name():
    data  = request.json or {}
    query = "select cityid from public.find_cityid_byname('{}')".format(data["City"])
    dataset= connect(query)
    datadict = {}
    datadict["City"] = data["City"]
    datadict["CityId"] = dataset[0][0]
    json_data = json.dumps(datadict)
    return json_data

@app.route("/api/find_city_spotids", methods=["POST"])
def find_city_spotids():
    data  = request.json or {}
    query = "select spotid from public.find_city_spotids('{}')".format(data["City"])
    dataset= connect(query)
    datadict = {}
    datadict["City"] = data["City"]
    datadict["SpotIds"] = [x[0] for x in dataset]
    json_data = json.dumps(datadict)
    return json_data

@app.route("/api/find_city_cost", methods=["POST"])
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
