from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_table import Table, Col,LinkCol, ButtonCol
from app.db import connect, call_sp, call_fn
from app.forms import UpdateRatingForm, SaveTripForm
from app.nosql import getCollection, saveDocument, deleteDocument
import heapq
import json
import requests
main = Blueprint('main', __name__)

@main.route('/')
def index():
    data = dict()
    data['username'] = "weix"
    return render_template('login.html',data = data)

@main.route("/item/int:userid> <int:tripid>", methods=["GET", "POST"])
def deleteusertrip(tripid):
    print("hear")
    userid_=12
    query = {"userid":userid_,"tripid":tripid}
    response = requests.post("http://sp21-cs411-07.cs.illinois.edu/api/delete_usertrip", json=query)
    return profile()

@main.route("/front_adduser", methods=["POST"])
def front_adduser():
    email = request.form["email"]
    username = request.form['username']
    password = request.form['password']
    query = {'username':username,
         'password':password,
         'createon':'2016-06-22 19:10:25-07',
         'gender':'male',
         'familyname':'dog',
         'givenname':'cat',
         'birthday':'1999-10-10',
         'homecityid':'500',
         'email':email
        }
    response = requests.post("http://sp21-cs411-07.cs.illinois.edu/api/add_new_user",json=query)
    return render_template("login.html")

@main.route("/front_login", methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    query = {'username':username,'password':password}
    response = requests.post("http://sp21-cs411-07.cs.illinois.edu/api/find_user_id",json=query)
    data = json.loads(response.text)
    if data['userid']==None:
        data = dict()
        data['username'] = None
        return render_template("login.html",data=data)
    data['username'] = username
    session["userid"] = data["userid"]
    return render_template("destination.html",userid = data["userid"])

@main.route("/profile", methods=["POST", "GET"])
def profile():
    if "userid"  in session:
      print ("xxx")
      userid = session["userid"]
    else:
      return render_template("login.html")

    query = {"userid":userid}
    print ("query {}".format(query))
    response = requests.post("http://sp21-cs411-07.cs.illinois.edu/api/find_saved_trips", json=query)
    #response = requests.post("http://172.22.152.7:5000/api/find_saved_trips", json=query)
    if response.text == "no trips found":
      return render_template("profile.html", message="no trips found")	
    dataset = json.loads(response.text)
    print ("dataset is {}".format(dataset))
    dataset = dataset["trips"]
    return render_template("profile.html",trips = dataset, userid=userid)

@main.route('/update_rating', methods=["POST", "GET"])
def ui_update_rating():
    userid  = request.args.get('userid', None)
    tripid = request.args.get('tripid', None)
    print ("userid {0} and tripid {1}".format(userid, tripid))
    return render_template("update.html", userid=userid, tripid=tripid)

"""@main.route('/tripsummary', methods=["POST", "GET"])
def ui_tripsummary():
    userid  = request.args.get('userid', None)
    tripid = request.args.get('tripid', None)
    query = {"userid":userid}
    response = requests.post("http://sp21-cs411-07.cs.illinois.edu/api/find_saved_trips", json=query)
    if response.text == "no trips found":
      return render_template("profile.html", message="no trips found")	
    dataset = json.loads(response.text)
    dataset = dataset["trips"]
    print ("userid {0} and tripid {1}".format(userid, tripid))
    return render_template("tripsummary.html", trips = userid=userid, tripid=tripid)"""

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
	      "suggestroutine": [96, 97, 98]
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

@main.route('/destination', methods=["POST", "GET"])
def destination():
    if request.method == "POST":

       if "userid"  in session:
         print ("xxx")
         userid = session["userid"]
       else:
         return render_template("login.html")
       from_city = request.form["from_city"]
       to_city = request.form["to_city"]
       return redirect(url_for("main.activity", from_city=from_city, to_city=to_city, userid=userid))
    return render_template('destination.html')

@main.route('/api/get_trip_summary', methods=["POST"])
def get_trip_summary():
    """ 
    Input Json Example
    {
      "spotids": [96,97,98],
      "from_city": 96,
      "to_city": 96
    }
    Return Json Example
    {
	    "routine": [
		98,
		97,
		99
	    ],
	    "totalcost": 359.0,
	    "suggestdays": 2.0,
	    "avgrating": 4.29,
	    "totalactivities": 3,
	    "flightduration": 0,
	    "flightcost": 0.0,
	    "activitycost": 5.0,
	    "activityduration": 10.5,
	    "othercost": 354.0
    }
    """
    def optimizeroutine(spotposition): #spotposition type: {97: [21.2910619, -157.843481],..., 98: [21.2629444, -157.8041957]}
        edges = dict()
        ids = list(spotposition.keys())
        for i in range(len(ids)):
            edges[ids[i]] = dict()
        for i in range(len(ids)):
            for j in range(i+1,len(ids)):
                posi = spotposition[ids[i]]
                posj = spotposition[ids[j]]
                dis = abs(posi[0]-posj[0])*100**2+abs(posi[1]-posj[1])*100**2
                edges[ids[i]][ids[j]] = dis
                edges[ids[j]][ids[i]] = dis
        routine = []
        routine.append(ids[0])
        hq = []
        for edge in edges[ids[0]]:
            hq.append([edges[ids[0]][edge],edge])
        heapq.heapify(hq)
        while len(hq)>0:
            dis,nxt = heapq.heappop(hq)
            routine.append(nxt)
            for i in range(len(hq)):
                vertices = hq[i]
                if edges[nxt][vertices[1]]<vertices[0]:
                    hq[i][0] = edges[nxt][vertices[1]]
        return routine
    data  = request.json or {}
    print ("data from tripsummary {}".format(data))
    url = "http://sp21-cs411-07.cs.illinois.edu"
    query = { "city": data["to_city"] }
    response = requests.post("{}/api/find_city_by_name".format(url),json=query)
    trip_data = dict()
    city = json.loads(response.text)
    data['destination_cityid'] = city["cityid"]

    #calculate flight information
    query = {'from_city':data['from_city'],'to_city':data['to_city']}
    response = requests.post("{}/api/find_flight_details".format(url),json=query)
    flights = json.loads(response.text)
    flight_cost = 0
    flight_duration = 0
    for flight in flights:
        flight_cost += float(flight['avgcost'])
        flight_duration += float(flight['duration'])
    flight_cost =flight_cost/2*1.2

    #calculate spot information
    spotids = data['spotids']
    query = {'spotids': spotids}
    response = requests.post("{}/api/find_many_spot_details".format(url),json=query)
    details = json.loads(response.text)
    spotposition = dict()
    act_cost = 0
    act_duration = 0
    avgrating = 0
    n=0
    for spot in details:
        n+=1
        spotposition[spot['spotid']] = [float(spot['lat']),(spot['lng']),spot['suggesthours']]
        act_cost+=float(spot['cost'])
        act_duration+=(float(spot['suggesthours'])+0.5)
        avgrating+=float(spot['rating'])
    avgrating/=n
    routine = optimizeroutine(spotposition)
    suggestdays = 1 + (act_duration + flight_duration)//8

    #calculate accomendation cost
    query = {"cityid": data['destination_cityid']}
    response = requests.post("{}/api/find_city_cost".format(url),json=query)
    accomendation = json.loads(response.text)
    staycost = (suggestdays-1)*accomendation['avghotelcost']
    mealcost = suggestdays*accomendation['avgmealcost']*2
    rentalcost = (suggestdays-1)*accomendation['avgcarrental']

    #import information into a dict format
    trip_data['routine'] = routine
    trip_data['totalcost'] = round(act_cost+flight_cost+staycost+mealcost+rentalcost,2)
    trip_data['suggestdays'] = suggestdays
    trip_data['avgrating'] = round(avgrating,2)
    trip_data['totalactivities'] = n
    trip_data['flightduration'] = round(flight_duration,2)
    trip_data['flightcost'] = flight_cost
    trip_data['activitycost'] = act_cost
    trip_data['activityduration'] = round(act_duration,2)
    trip_data['othercost'] = staycost+mealcost+rentalcost

    json_data = json.dumps(trip_data)
    return json_data

@main.route('/map')
def map():
    return render_template('map.html')

@main.route('/activity', methods=["POST", "GET"])
def activity():
    from_city = request.args.get('from_city', None)
    to_city = request.args.get('to_city', None)
    userid = request.args.get('userid', None)
    query = {'city':'{}'.format(to_city)}
    response = requests.post("http://sp21-cs411-07.cs.illinois.edu/api/find_city_spotids", json=query)
    data = json.loads(response.text)
    spotids = data['spotids']
    spotname = []
    for spotid in spotids[:5]:
      query = {'spotid':spotid}
      resp = requests.post("http://sp21-cs411-07.cs.illinois.edu/api/find_spot_details", json=query)
      details = json.loads(resp.text)
      spotname.append(details["spotname"])
    return render_template('activity.html',data = spotname, from_city=from_city, to_city=to_city, userid=userid)
    
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
      "filter": {
		  "userid": 11,
		  "tripid": 33
		}
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
    print (data["filter"])
    dataset= getCollection(collection=data["collection"], queryFilter=data["filter"])
    if dataset.count == 0 :
      return {"msg": "no map in mongo"}
    json_data = json.dumps(dataset[0])
    return json_data

def get_features_from_route(route):
    #fetch the spots of the suggested routes
    spots = []
    features = []
    seq = 0
    for spotid in route:
        seq += 1
        spot = find_spot_details_db(spotid)
        dic = dict(lat=spot[0][10], lng=spot[0][11])
        spots.append(dic)
        #create spot geojson
        point = dict(type="Feature",
                     geometry=dict(type="Point",
                                   coordinates=[dic["lng"],dic["lat"]]),
                     properties=dict(name="{0}:{1}:{2}hrs".format(seq, spot[0][0], spot[0][3]))
                )
        features.append(point)

    #create geojson line
    line = dict(type="Feature",
                       geometry=dict(type="LineString",
                                     coordinates=[[x["lng"],x["lat"]] for x in spots]),
                       properties=dict(name="route")
                      ) 
    features.append(line) 
    return features

@main.route("/api/get_geojson_from_route", methods=["POST"])
def get_geojson_from_route():
    """ 
    Input Json Example
    [97,98]
    Return Json Example
	{
	    "type": "FeatureCollection",
	    "features": [
		{
		    "type": "Feature",
		    "geometry": {
			"type": "Point",
			"coordinates": [
			    -157.843481,
			    21.2910619
			]
		    },
		    "properties": {
			"name": "1:Ala Moana Center"
		    }
		},
		{
		    "type": "Feature",
		    "geometry": {
			"type": "Point",
			"coordinates": [
			    -157.8041957,
			    21.2629444
			]
		    },
		    "properties": {
			"name": "2:Diamond Head Crater Hike"
		    }
		},
		{
		    "type": "Feature",
		    "geometry": {
			"type": "LineString",
			"coordinates": [
			    [
				-157.843481,
				21.2910619
			    ],
			    [
				-157.8041957,
				21.2629444
			    ]
			]
		    },
		    "properties": {
			"name": "route"
		    }
		}
	    ]
	}
    """
    data  = request.json or {}
    print (data)
    features = get_features_from_route(data)

    geoDoc = dict(type="FeatureCollection",
                  features=features)
    json_data = json.dumps(geoDoc)
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

@main.route("/api/find_many_spot_details", methods=["POST"])
def find_many_spot_details():
    """ 
    Input Json Example
    {
      "spotids": [96,97,98]
      "userid": 11
    }
    Return Json Example
    {
        [
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
			},
	]
    }
    """
    data  = request.json or {}
    params = []
    params.append((data["spotids"], "array"))
    fn = "find_many_spot_details"
    dataset = call_fn(fn, params)

    ls = []
    for item in dataset:
       datadict = {}
       datadict["spotid"] = item[0]
       datadict["spotname"] = item[1]
       datadict["cityname"] = item[2]
       datadict["address"] = item[3]
       datadict["suggesthours"] = item[4]
       datadict["cost"] = item[5]
       datadict["autismfriendly"] = item[6]
       datadict["openday"] = item[7]
       datadict["opennight"] = item[8]
       datadict["rating"] = item[9]
       datadict["introduction"] = item[10]
       datadict["lat"] = item[11]
       datadict["lng"] = item[12]
       datadict["imgurl"] = item[13]
       datadict["website"] = item[14]
       datadict["category"] = item[15]
       datadict["state"] = item[16]
       datadict["covidfactor"] = item[17]
       ls.append(datadict)
    json_data = json.dumps(ls)
    return json_data

def find_spot_details_db(spotid):
    query = "select spotname, cityname, address, suggesthours, cost, autismfriendly, openday, opennight, rating, introduction, lat, lng, imgurl, website, category, state from public.find_spot_details({})".format(spotid)
    return connect(query)

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
    dataset = find_spot_details_db(data["spotid"])
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

@main.route("/api/find_flight_details", methods=["POST"])
def find_flight_details():
    """ 
    Input Json Example
    {
      "from_city": "xxx",
      "to_city": "yyy"
    }
    Return Json Example
    {
        "flightid": 96,
        "avgcost": 10,
        "duration": 10
    }
    """
    data  = request.json or {}
    query = "select flightid, avgcost, duration from public.find_flight_details('{0}', '{1}')".format(data["from_city"], data["to_city"])
    dataset= connect(query)
    datadict = [dict(flightid=x[0], avgcost=x[1], duration=x[2]) for x in dataset]
    json_data = json.dumps(datadict)
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
    try:
       dataset= connect(query)
    except Exception as ex:
       return "error when running query {}".format(query)

    if (len(dataset) == 0):
      return "no trips found"

    aha = dataset[0]
    datadict = {}
    trips = []
    for x in aha[0]:
      #get trip details
      details = find_trip_details(x)
      trip = {}
      if details is not None:
         trip["tripid"] = x
         trip["totalduration"] = details[1]
         trip["totalcost"] = details[2]
         trip["activityduration"] = details[3]
         trip["activitycost"] = details[4]
         trip["transportationtime"] = details[5]
         trip["transportationcost"] = details[6]
         trip["staycost"] = details[7]
         trip["foodcost"] = details[8]
         trip["to_cityname"] = details[9]
         trip["from_cityname"] = details[10]
         trip["suggestdays"] = details[11]
         trip["suggestroutine"] = details[12]
      else:
         trip["tripid"] = x
         trip["msg"] =  "no trip found"
        
      trips.append(trip)
    datadict["trips"] = trips
    json_data = json.dumps(datadict)
    return json_data

@main.route("/api/find_trip_details", methods=["GET","POST"])
def api_find_trip_details():
    """ 
    Input Json Example
    {
      "tripid": 3
    }
    Return Json Example
    {"avgcost": 3}
    """
    data  = request.json or {}
    #get trip details
    details = find_trip_details(data["tripid"])
    if details is not None:
	    trip = {}
	    trip["tripid"] = data["tripid"]
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
    else:
	    trip = {"msg": "no trip found"}    
    json_data = json.dumps(trip)
    return json_data

def find_trip_details(tripid):
    query = "select userid,totalduration,totalcost,activityduration,activitycost,transportationtime,transportationcost,staycost,foodcost,to_cityname,from_cityname,suggestdays,suggestroutine from find_tripdetail({})".format(tripid)
    print ("query {}".format(query))
    dataset= connect(query)
    if len(list(dataset)) > 0:
       returnList = [dataset[0][i] for i in range(13)] 
    else:
       returnList = None
    return returnList

@main.route("/api/cal_spots", methods=["POST"])
def cal_spots():
    """ 
    Inpuelect userid,totalduration,totalcost,activityduration,activitycost,transportationtime,transportationcost,staycost,foodcost,toflightid,backflightid,suggestdays,suggestroutine from find_tripdetail({}) Json Example
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
    print ("find destinations starting...")
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

    #Deleting the document from mongodb
    deleteDocument(params); 
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
      "to_cityname": Seattle, WA,
      "from_cityname": Honolulu, HI,
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
    params.append((data["to_cityname"], "text"))
    params.append((data["from_cityname"], "text"))
    params.append((data["suggestdays"], "text"))
    params.append((data["suggestroutine"], "array"))

    print("from city::")
    print(data["from_cityname"])

    fn = "save_trip"
    dataset= call_fn(fn, params)

    #calling add_usertrip
    tripid = dataset[0][0] 
    print ("trip id is {}".format(tripid))
    add_user_trip(data["userid"], tripid)

    features = get_features_from_route(data["suggestroutine"])

    geoDoc = dict(type="FeatureCollection",
                  userid=data["userid"],
                  tripid=tripid,
                  features=features)
                  
    #save the geojson in mongo
    saveDocument(geoDoc)

    datadict = {}
    datadict["ReturnCode"] = 200
    json_data = json.dumps(datadict)
    return json_data


