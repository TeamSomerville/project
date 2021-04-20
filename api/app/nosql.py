import pymongo

def getCollection(collection):
   client = pymongo.MongoClient("mongodb://localhost:27017/")
   
   db = client["geo"]
   
   col = db[collection]
   
   x = col.find({}, {"_id": 0})
   
   return x

def saveDocument(document):
   client = pymongo.MongoClient("mongodb://localhost:27017/")
   
   db = client["geo"]
   col = db["userroutes"]

   col.insert_one(document)
