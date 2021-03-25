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
    #datadict = {}
    #datadict["City"] = data[0]
    #datadict["Country"] = data[1]
    cityid = dataset[0][0]
    return str(cityid)
