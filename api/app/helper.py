import pymongo
import psycopg2

def saveDocument(document):
   client = pymongo.MongoClient("mongodb://localhost:27017/")
   
   db = client["geo"]
   col = db["userroutes"]

   col.insert_one(document)

def find_spot_details_db(spotid):
    query = "select spotname, cityname, address, suggesthours, cost, autismfriendly, openday, opennight, rating, introduction, lat, lng, imgurl, website, category, state from public.find_spot_details({})".format(spotid)
    return connect(query)

def populateMongoFromTrips():
   client = pymongo.MongoClient("mongodb://localhost:27017/")
   
   db = client["geo"]
   col = db["userroutes"]
   query = "select * from trip where userid=6;"
   dataset = connect(query)
   for row in dataset:
     geoJson = createGeoJson(row)
     saveDocument(geoJson)

def createGeoJson(data):
   spots = []
   features = []
   seq = 0
   for spotid in data[13]:
       seq += 1
       spot = find_spot_details_db(spotid)
       if len(spot) == 0:
         print ("spot is empty for spotid {}".format(spotid))
         continue
       dic = dict(lat=spot[0][10], lng=spot[0][11])
       spots.append(dic)
       #create spot geojson
       point = dict(type="Feature",
                    geometry=dict(type="Point",
                                  coordinates=[dic["lng"],dic["lat"]]),
                    properties=dict(name="{0}:{1}:{2}hrs".format(seq, spot[0][0], spot[0][4]))
               )
       features.append(point)

   #create geojson line
   line = dict(type="Feature",
                      geometry=dict(type="LineString",
                                    coordinates=[[x["lng"],x["lat"]] for x in spots]),
                      properties=dict(name="route")
                     ) 
   features.append(line) 

   geoDoc = dict(type="FeatureCollection",
                 userid=data[1],
                 tripid=data[0],
                 features=features) 

   return geoDoc

def connect(query):
    """ connect to the db"""
    conn  = None
    returnRow = None
    try:
        conn = psycopg2.connect(
            host = "172.22.152.7",
            database = "postgres",
            user = "admin",
	    password = "admin"
        )

        cur  = conn.cursor()
        cur.execute(query)
        returnRow = cur.fetchall()
        cur.close()
    except Exception as ex:
        print (ex)
    finally:
        if conn is not None:
            conn.close()

    return returnRow 

if __name__ == '__main__':
    populateMongoFromTrips()
