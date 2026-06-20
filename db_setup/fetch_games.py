import requests
from pymongo import MongoClient


OMDB_API_KEY = "10f677ad"        # get free key at omdbapi.com
OMDB_URL     = "http://www.omdbapi.com/"
TYPE= "movie"

MONGO_URI    = "mongodb://localhost:27017"
DB_NAME      = "Gamesdb"
COLLECTION   = "gamess"

client= MongoClient(MONGO_URI)
collection= client[DB_NAME][COLLECTION]

# while True:

#     found= collection.find_one( {"Title": "Interstellar"} )
#     print(found) if found else print(None)
#     break


print( "movie db connection established !".upper() )

fetched_movies= set()

done= False

# max requests per day is 1000 
# keywords= ["movie keyword of lenght 30"]
keywords = [
    "love",
    "war",
    "space",
    "crime",
    "family",
    "death",
    "revenge",
    "survival",
    "adventure",
    "mystery",
    "power",
    "freedom",
    "friendship",
    "betrayal",
    "justice",
    "hero",
    "dark",
    "lost",
    "escape",
    "future",
    "secret",
    "danger",
    "blood",
    "rise",
    "night",
    "evil",
    "dream",
    "fire",
    "last",
    "hunt",
    "storm",
    "kingdom",
    "shadow",
    "mission",
    "ghost",
]

# collection.create_index("imdbID", unique=True)
# print("creating title index")
# collection.create_index("Title")
# print("imdbID index has been set !".upper() )

# search for movies via keywords return 30 movies per request
for keyword in keywords:

    print( "keyword being extracted:", keyword )

    if done== True:
        print("breaking outer loop!".upper())
        break


    # pages= [4,5,6]
    pages= [7,8,9]

    # for page in range(1, 4):   # 3 pages × 10 results = 30 per keyword
    for page in pages:   # 3 pages × 10 results = 30 per keyword


        print("current page :".upper(), page)

        movie_sample_response = requests.get(OMDB_URL, params={
            "apikey": OMDB_API_KEY,
            "s"     : keyword,
            "type"  : TYPE,
            "page"  : page,
        }).json()

        if movie_sample_response.get("Response")== "True":

            print( "sample movie data request succesfull".upper() ) 

            searches= movie_sample_response.get("Search")

            for result in searches :

                if result.get("imdbID", None) not in fetched_movies and not collection.find_one({"Title": result.get("Title") }) :

                    # collection.fincd 

                    print( "fetching full movie data for :" , f"{result.get('Title')}".upper() )

                    print( result.get("Title", None)," movie does not exist in db adding now !".upper())
                    
                    fetched_movies.add(result.get("imdbID"))
                    
                    # if len(fetched_movies) > 950:
                    if collection.count_documents({}) == 2500:

                        done= True
                        print("breaking inner loop!".upper())
                        break

                    # print("result", result)

                    print( "fetching full movie data for :" , f"{result.get('Title')}".upper() )
                    full_movie_data= requests.get(OMDB_URL, params={
                        "apikey": OMDB_API_KEY,
                        "i"     : result["imdbID"],
                        "plot"  : "full",
                    }).json()

                    full_movie_data.pop("Response", None)
                    print("response field removed, adding full movie data to collection")

                    # print( "id", full_movie_data.get("imdbID") )
                    # print( "full movie data", full_movie_data )


                    collection.update_one(
                        {"imdbID": full_movie_data["imdbID"]},
                        {"$set": full_movie_data},
                        upsert=True
                    )

                else:
                    print(result.get("Title"), "movie, already exists!".upper())

        else:
            print( "sample movie data request unsuccesfull".upper() ) 
            print( "request status:", movie_sample_response.get("Response") )
            

print(f"stored number of {collection.count_documents({})} movies")