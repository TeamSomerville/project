import pymongo

def getCollection(collection, queryFilter):
   client = pymongo.MongoClient("mongodb://localhost:27017/")
   
   db = client["geo"]
   
   col = db[collection]
   
   x = col.find(queryFilter, {"_id": 0, "userid":0, "tripid":0})
   
   return x

def saveDocument(document):
   client = pymongo.MongoClient("mongodb://localhost:27017/")
   
   db = client["geo"]
   col = db["userroutes"]

   col.insert_one(document)
