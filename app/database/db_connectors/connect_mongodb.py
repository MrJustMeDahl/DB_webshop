from pymongo import MongoClient

def connect_mongodb():
    try:
        client = MongoClient("mongodb://mongodb-db:27017/")
        print("MongoDB connection successful.")
        return client
    except Exception as e:
        print(f"MongoDB connection error: {e}")
        return None
