from pymongo import MongoClient


# connect to the mongodb server
client = MongoClient("mongodb://localhost:27017/")
# connect to a database 
DATABASE_NAME= "gamesdb" 
db = client[DATABASE_NAME]

# connect to a collection
COLLECTION_NAME= "games"
games_collection = db[COLLECTION_NAME]

# connect to a collection
COLLECTION_NAME= "game_news"
news_collection = db[COLLECTION_NAME]