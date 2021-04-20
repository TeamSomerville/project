from flask import Blueprint, render_template, request
from flask_table import Table, Col,LinkCol, ButtonCol
from app.db import connect, call_sp, call_fn
from app.forms import UpdateRatingForm, SaveTripForm
from app.nosql import getCollection
import json
import requests
main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route("/item/int:userid> <int:tripid>", methods=["GET", "POST"])
def deleteusertrip(tripid):
    userid_=11
    query = {"userid":userid_,"tripid":tripid}
    response = requests.post("http://sp21-cs411-07.cs.illinois.edu/api/delete_usertrip", json=query)
    return profile()

@main.route("/profile")
def profile():
    userid_ = 11
    query = {"userid":userid_}
    response = requests.post("http://sp21-cs411-07.cs.illinois.edu/api/find_saved_trips", json=query)
    data = json.loads(response.text)
    ids = []
    for i in range(len(data["trips"])):
        ids.append(data["trips"][i]["tripid"])
    # Declare your table
    userid = Col("userid")
    class SubTable(Table):
        tripid = Col("Trip ID")
        delete = ButtonCol("delete","main.deleteusertrip",url_kwargs=dict(userid="userid",tripid="tripid"))
    #def update_rate()
    items = [dict(tripid=id_,userid=userid_) for id_ in ids]
    # Populate the table
    table = SubTable(items)
    return render_template("profile.html", table=table)

@main.route('/update_rating', methods=["POST", "GET"])
def ui_update_rating():
    form = UpdateRatingForm()
    if form.validate_on_submit():
       query = {"spotid": "96", "rating": form.rating.data}
       response = requests.post("http://sp21-cs411-07.cs.illinois.edu/api/update_rating", json=query)

    query = {"spotid":96}
    response = requests.post("http://sp21-cs411-07.cs.illinois.edu/api/find_spot_details", json=query)
    data = json.loads(response.text)
    items = [dict(spotid=data["spotid"],
	     spotname=data["spotname"],
	     cityname=data["cityname"],
	     address=data["address"],
	     rating=data["rating"])]
    # Declare your table
    class SubTable(Table):
       border = "Yes"
       spotid = Col("Spot ID")
       spotname = Col("Spot Name")
       cityname = Col("City Name")
       address = Col("Address")
       rating = Col("Rating")
           
       # Populate the table
    table = SubTable(items)
    return render_template("update.html", form=form, table=table)

@main.route('/save_trip', methods=["POST", "GET"])
def ui_save_trip():
    form = SaveTripForm()
    if form.validate_on_submit():
       query =  {
	      "userid": 11,
	      "totalduration": form.totalduration.data,
	      "totalcost": 96,
	      "activityduration": 96,
	      "activitycost": 96,
	      "transportationtime": 96,
	      "transportationcost": 96,
	      "staycost": 96,
	      "foodcost": 96,
	      "toflightid": 96,
	      "backflightid": 96,
	      "suggestdays": 96,
	      "suggestroutine": [96, 23, 34]
	    }
       response = requests.post("http://sp21-cs411-07.cs.illinois.edu/api/save_trip", json=query)

    query = {"userid": 11}
    response = requests.post("http://sp21-cs411-07.cs.illinois.edu/api/find_saved_trips", json=query)
    data = json.loads(response.text)
    items = []
    for trip in data["trips"]:
       item = dict(tripid=trip["tripid"],
                   totalduration=trip["totalduration"])
       items.append(item)
    # Declare your table
    class SubTable(Table):
       border = "Yes"
       tripid = Col("Trip ID")
       totalduration = Col("Total Duration")
           
       # Populate the table
    table = SubTable(items)
    return render_template("trip.html", form=form, table=table)

@main.route('/destination')
def destination():
    return render_template('destination.html')

@main.route('/map')
def map():
    return render_template('map.html')

@main.route('/activity')
def activity():
    query = {'city':'Honolulu, HI'}
    response = requests.post("http://sp21-cs411-07.cs.illinois.edu/api/find_city_spotids", json=query)
    data = json.loads(response.text)
    spotids = data['spotids']
    spotname = []
    for spotid in spotids[:5]:
      query = {'spotid':spotid}
      request = requests.post("http://sp21-cs411-07.cs.illinois.edu/api/find_spot_details", json=query)
      details = json.loads(request.text)
      spotname.append(details["spotname"])
    return render_template('activity.html',data = spotname)
    
@main.route("/front_savetrip")
def front_savetrip():
    query = {"userid":11,
         "totalduration":22,
         "totalcost":33,
         "activityduration":44,
         "activitycost":55,
         "transportationtime":11,
         "transportationcost":32,
         "staycost":12,
         "foodcost":32,
         "toflightid":226,
         "backflightid":2276,
         "suggestdays":4,
         "suggestroutine":[99,98,97]
        }
    response = requests.post("http://sp21-cs411-07.cs.illinois.edu/api/save_trip", json=query)
    return activity()

@main.route("/api/find_mongo_collection", methods=["POST"])
def find_mongo_collection():
    """ 
    Input Json Example
    {
      "collection": "FeatureCollection",
    }
    Return Json Example
    {
       "type": "FeatureCollection",
       "features": [
           {
               "type": "Feature",
               "id": "7f7bef66-8957-406d-82a2-6aa1abe39f6d",
               "geometry": {
                   "type": "Point",
                   "coordinates": [
                       77.43785851,
                       45.18766302
                   ]
               },
               "properties": {
                   "name": "this is a test"
               }
           }
       ]
    }
    """
    data  = request.json or {}
    dataset= getCollection(data["collection"])
    datadict = {}
    datadict["type"] = "FeatureCollection"
    datadict["features"] = [x for x in dataset]
    json_data = json.dumps(datadict)
    return json_data

@main.route("/api/find_city_by_name", methods=["POST"])
def find_city_by_name():
    """ 
    Input Json Example
    {
      "city": "New York",
    }
    Return Json Example
    {
        "city": "New York",
        "cityid": "1"
    }
    """
    data  = request.json or {}
    query = "select cityid from public.find_cityid_byname('{}')".format(data["city"])
    dataset= connect(query)
    datadict = {}
    datadict["city"] = data["city"]
    datadict["cityid"] = dataset[0][0]
    json_data = json.dumps(datadict)
    return json_data

@main.route("/api/find_city_spotids", methods=["POST"])
def find_city_spotids():
    """ 
    Input Json Example
    {
      "city": "New York",
    }
    Return Json Example
    {
        "city": "New York",
        "spotids": ["1", "2"]
    }
    """
    data  = request.json or {}
    query = "select spotid from public.find_city_spotids('{}')".format(data["city"])
    dataset= connect(query)
    datadict = {}
    datadict["city"] = data["city"]
    datadict["spotids"] = [x[0] for x in dataset]
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
    """ 
    Input Json Example
    {
      "cityid": 12,
    }
    Return Json Example
    {
        "avghotelcost": 123,
        "avgmealcost": 1,
        "avgcarrental": 123
    }
    """
    data  = request.json or {}
    query = "select avghotelcost, avgmealcost, avgcarental from public.find_citycost({})".format(data["cityid"])
    dataset= connect(query)
    datadict = {}
    datadict["avghotelcost"] = dataset[0][0]
    datadict["avgmealcost"] = dataset[0][1]
    datadict["avgcarrental"] = dataset[0][2]
    json_data = json.dumps(datadict)
    return json_data

@main.route("/api/find_user_id", methods=["POST"])
def find_user_id():
    """ 
    Input Json Example
    {
      "username": "purvis",
      "password": "password"
    }
    Return Json Example
    {"userid": 3}
    """
    data  = request.json or {}
    query = "select userid from find_userid('{0}', '{1}')".format(data["username"], data["password"])
    dataset= connect(query)
    datadict = {}
    datadict["userid"] = dataset[0][0]
    json_data = json.dumps(datadict)
    return json_data

@main.route("/api/find_flight_id", methods=["POST"])
def find_flight_id():
    """ 
    Input Json Example
    {
      "fromcity": "Aberdeen, SD",
      "tocity": "Minneapolis, MN"
    }
    Return Json Example
    {"flightid": 3}
    """
    data  = request.json or {}
    query = "select flightid from find_flightid('{0}', '{1}')".format(data["fromcity"], data["tocity"])
    dataset= connect(query)
    datadict = {}
    datadict["flightid"] = dataset[0][0]
    json_data = json.dumps(datadict)
    return json_data

@main.route("/api/find_flight_duration", methods=["POST"])
def find_flight_duration():
    """ 
    Input Json Example
    {
      "flightid": "3",
    }
    Return Json Example
    {"duration": 3}
    """
    data  = request.json or {}
    query = "select duration from find_flight_duration('{0}')".format(data["flightid"])
    dataset= connect(query)
    datadict = {}
    datadict["duration"] = dataset[0][0]
    json_data = json.dumps(datadict)
    return json_data

@main.route("/api/find_flight_cost", methods=["POST"])
def find_flight_cost():
    """ 
    Input Json Example
    {
      "flightid": "3",
    }
    Return Json Example
    {"avgcost": 3}
    """
    data  = request.json or {}
    query = "select avgcost from find_flight_cost('{0}')".format(data["flightid"])
    dataset= connect(query)
    datadict = {}
    datadict["avgcost"] = dataset[0][0]
    json_data = json.dumps(datadict)
    return json_data

@main.route("/api/find_saved_trips", methods=["GET","POST"])
def find_saved_trips():
    """ 
    Input Json Example
    {
      "userid": 3
    }
    Return Json Example
    {"avgcost": 3}
    """
    data  = request.json or {}
    print ("debug: data is {}".format(data))
    query = "select savedtripids from find_saved_trips({0})".format(data["userid"])
    dataset= connect(query)
    aha = dataset[0]
    datadict = {}
    trips = []
    for x in aha[0]:
      #get trip details
      details = find_trip_details(x)
      trip = {}
      trip["tripid"] = x
      trip["totalduration"] = details[1]
      trip["totalcost"] = details[2]
      trip["activityduration"] = details[3]
      trip["activitycost"] = details[4]
      trip["transportationtime"] = details[5]
      trip["transportationcost"] = details[6]
      trip["staycost"] = details[7]
      trip["foodcost"] = details[8]
      trip["toflightid"] = details[9]
      trip["backflightid"] = details[10]
      trip["suggestdays"] = details[11]
      trip["suggestroutine"] = details[12]
      trips.append(trip)
        
    datadict["trips"] = trips
    json_data = json.dumps(datadict)
    return json_data

def find_trip_details(tripid):
    query = "select userid,totalduration,totalcost,activityduration,activitycost,transportationtime,transportationcost,staycost,foodcost,toflightid,backflightid,suggestdays,suggestroutine from find_tripdetail({})".format(tripid)
    dataset= connect(query)
    returnList = [dataset[0][i] for i in range(13)] 
    return returnList

@main.route("/api/cal_spots", methods=["POST"])
def cal_spots():
    """ 
    Input Json Example
    {
      "spotids": [3,4,5]
    }
    Return Json Example
    {"totalcost": 3,
     "totalhours": 4}
    """
    data  = request.json or {}
    temp = [str(z) for z in data["spotids"]]
    converted = ",".join(temp)
    query = "select totalcost, totalhours from cal_spots('{{{}}}')".format(converted)
    dataset= connect(query)
    datadict = {}
    datadict["totalcost"] = dataset[0][0]
    datadict["totalhours"] = dataset[0][1]
    json_data = json.dumps(datadict)
    return json_data

@main.route("/api/find_destinations", methods=["GET"])
def find_destinations():
    """ 
    Return Json Example
    {"cities": ["New York", "Boston"]}
    """
    query = "select names from find_destinations()"
    dataset= connect(query)
    datadict = {}
    converted = [x[0] for x in dataset]
    datadict["cities"] = converted
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

def add_user_trip(userid, tripid):
    params = []
    params.append((userid, "text"))
    params.append((tripid, "text"))
    sp = "add_usertrip"
    dataset= call_sp(sp, params)

@main.route("/api/delete_usertrip", methods=["POST"])
def delete_usertrip():
    """ 
    Input Json Example
    {
      "userid": 96,
      "tripid": 12,
    }
    Return Json Example
    {"ReturnCode": 200}
    """
    data  = request.json or {}
    params = []
    params.append((data["userid"], "text"))
    params.append((data["tripid"], "text"))
    sp = "delete_usertrip"
    dataset= call_sp(sp, params)
    datadict = {}
    if dataset is not None:
       datadict["ReturnCode"] = dataset[0][0]
    else:
       datadict["ReturnCode"] = 200
    json_data = json.dumps(datadict)
    return json_data

@main.route("/api/delete_trip", methods=["POST"])
def delete_trip():
    """ 
    Input Json Example
    {
      "tripid": 1
    }
    Return Json Example
    {"ReturnCode": 200}
    """
    data  = request.json or {}
    params = []
    params.append((data["tripid"], "text"))
    sp = "delete_trip"
    dataset= call_sp(sp, params)
    datadict = {}
    if dataset is not None:
       datadict["ReturnCode"] = dataset[0][0]
    else:
       datadict["ReturnCode"] = 200
    json_data = json.dumps(datadict)
    return json_data

@main.route("/api/save_trip", methods=["POST"])
def save_trip():
    """ 
    Input Json Example
    {
      "userid": 96,
      "totalduration": 96,
      "totalcost": 96,
      "activityduration": 96,
      "activitycost": 96,
      "transportationtime": 96,
      "transportationcost": 96,
      "staycost": 96,
      "foodcost": 96,
      "toflightid": 96,
      "backflightid": 96,
      "suggestdays": 96,
      "suggestroutine": [96, 23, 34]
    }
    Return Json Example
    {"ReturnCode": 200}
    """
    data  = request.json or {}
    params = []
    params.append((data["userid"], "text"))
    params.append((data["totalduration"], "text"))
    params.append((data["totalcost"], "text"))
    params.append((data["activityduration"], "text"))
    params.append((data["activitycost"], "text"))
    params.append((data["transportationtime"], "text"))
    params.append((data["transportationcost"], "text"))
    params.append((data["staycost"], "text"))
    params.append((data["foodcost"], "text"))
    params.append((data["toflightid"], "text"))
    params.append((data["backflightid"], "text"))
    params.append((data["suggestdays"], "text"))
    params.append((data["suggestroutine"], "array"))
    fn = "save_trip"
    dataset= call_fn(fn, params)

    #calling add_usertrip
    tripid = dataset[0][0]
    add_user_trip(data["userid"], tripid)

    #create geojson
    

    datadict = {}
    datadict["ReturnCode"] = 200
    json_data = json.dumps(datadict)
    return json_data
