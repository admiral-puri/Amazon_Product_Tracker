import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["trackerdb"]

myclient.drop_database("trackerdb")
