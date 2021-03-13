from app import app
from app.db import connect
import json

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
