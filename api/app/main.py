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

@main.route("/api/find_spot_details", methods=["POST"])
def find_spot_details():
    """ 
    Input Json Example
    {
      "spotid": "96",
    }
    Return Json Example
    {
        "spotid": "96",
        "spotname": "Pearl Harbor Aviation Museum",
        "cityname": "Honolulu, HI",
        "address": "319 Lexington Blvd, Honolulu, HI 96818",
        "suggesthours": 8,
        "cost": 25,
        "autismfriendly": false,
        "openday": true,
        "opennight": false,
        "rating": 4.604,
        "introduction": "ctly to the attack on Pearl Harbor and World War II.",
        "lat": 21.359744,
        "lng": -157.961823,
        "imgurl": "https://lh5.googleusercontent.com/p/AF1QipOye_AyHpDXGHbe2nJo3nLeoRNlOI0iagq2sg3X=w1920-h1080-k-no",
        "website": "pearlharboraviationmuseum.org",
        "category": "Museum",
        "state": " HI"
    }
    """
    data  = request.json or {}
    query = "select spotname, cityname, address, suggesthours, cost, autismfriendly, openday, opennight, rating, introduction, lat, lng, imgurl, website, category, state from public.find_spot_details({})".format(data["spotid"])
    dataset= connect(query)
    datadict = {}
    datadict["spotid"] = data["spotid"]
    datadict["spotname"] = dataset[0][0]
    datadict["cityname"] = dataset[0][1]
    datadict["address"] = dataset[0][2]
    datadict["suggesthours"] = dataset[0][3]
    datadict["cost"] = dataset[0][4]
    datadict["autismfriendly"] = dataset[0][5]
    datadict["openday"] = dataset[0][6]
    datadict["opennight"] = dataset[0][7]
    datadict["rating"] = dataset[0][8]
    datadict["introduction"] = dataset[0][9]
    datadict["lat"] = dataset[0][10]
    datadict["lng"] = dataset[0][11]
    datadict["imgurl"] = dataset[0][12]
    datadict["website"] = dataset[0][13]
    datadict["category"] = dataset[0][14]
    datadict["state"] = dataset[0][15]
    json_data = json.dumps(datadict)
    print (json_data)
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

@main.route("/api/find_user_id", methods=["POST"])
def find_user_id():
    data  = request.json or {}
    query = "select userid from find_userid('{0}', '{1}')".format(data["username"], data["password"])
    dataset= connect(query)
    datadict = {}
    datadict["userid"] = dataset[0][0]
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
