import pymongo

def getCollection(collection, user):
   client = pymongo.MongoClient("mongodb://localhost:27017/")
   
   db = client["geo"]
   
   col = db[collection]
   
   x = col.find({"userid":user}, {"_id": 0, "userid":0})
   
   return x

def saveDocument(document):
   client = pymongo.MongoClient("mongodb://localhost:27017/")
   
   db = client["geo"]
   col = db["userroutes"]

   col.insert_one(document)
