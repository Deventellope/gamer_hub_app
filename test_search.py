import requests
from pymongo import MongoClient


OMDB_API_KEY = "10f677ad"        # get free key at omdbapi.com
OMDB_URL     = "http://www.omdbapi.com/"
TYPE= "movie"

MONGO_URI    = "mongodb://localhost:27017"
DB_NAME      = "moviedb"
COLLECTION   = "movies"

client= MongoClient(MONGO_URI)
collection= client[DB_NAME][COLLECTION]


# found= collection.find_one( {"Title": "Interstellar"} )
# found= collection.find_one( {"Title": "Crazy, Stupid, love"} )
# found= collection.find_one( {"Title": "Ghost Stories"} )
found= collection.count_documents({}) 
print(found) if found else print(None)

