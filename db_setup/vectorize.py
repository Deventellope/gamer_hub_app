# mongo dependencies
from pymongo import MongoClient

# node dependencies
from sentence_transformers import SentenceTransformer

import numpy as np
import faiss


print("setting up mongo db connection")

OMDB_API_KEY = "10f677ad"        # get free key at omdbapi.com
OMDB_URL     = "http://www.omdbapi.com/"
TYPE= "movie"

MONGO_URI    = "mongodb://localhost:27017"
DB_NAME      = "moviedb"
COLLECTION   = "movies"

client= MongoClient(MONGO_URI)
collection= client[DB_NAME][COLLECTION]


MODEL_NAME  = "all-mpnet-base-v2"
model = SentenceTransformer(MODEL_NAME)

# These two files are your "pre-built index" saved to disk.
# Once built you never need to re-embed unless your data changes.
INDEX_FILE_NAME_TO_SAVE_TO_DISK  = "docs.index"     # The FAISS binary index (vectors + HNSW graph)
NUMPY_INDEX_FILE_TO_SAVE = "id_map.npy"    # Parallel array: position i → MongoDB _id string



docs= list( collection.find({}) ) #cursor object return each document in our db

id_list= [] #an array containinsg id of each document in our database

stringified_doc=[] 

# create a string represention of the fields and value of each entry
for entry in docs:

    # first create and id array for each document to store
    id= str(entry["_id"])
    id_list.append(id)

    # define velevant variables to serialize    
    entries_to_string= f"""

     {entry.get('Title')}
        {entry.get('Year')}
        {entry.get('Genre')}
        {entry.get('Plot')}
        {entry.get('Director')}
        {entry.get('Actors')}
        {entry.get('Writer')}
        {entry.get('Production')}

    """
    stringified_doc.append(entries_to_string)

print("length of document loaded", len(stringified_doc))


# create a vector emdedding for stringified doc entries
print("creating vector embeddings for stringified_doc please wait")

vectors = model.encode(
    stringified_doc,
    show_progress_bar=True,
    convert_to_numpy=True,
    batch_size=32,
)


vectors = vectors.astype(np.float32)

print(f" → Vectors shape: {vectors.shape}")

print("normalizing vectors".upper())
# sets each vector to size of value 1
faiss.normalize_L2(vectors)

dim= vectors.shape[1]   # 768

#creates a graph of indexes with 32 nodes segmentatation  
print("Building HNSW index...")
index = faiss.IndexHNSWFlat(dim, 32)

# hnsw creates a sort of an index graph segmenting vectors on nodes based on similarities 
# it creates a speed tunnel loop for our database where search doesnt have to 
# compare user query with every piece of data but instead compare with node 
# similarity (a smaller semantic repr od our database) 

index.add(vectors) 
print(f"  → Index contains {index.ntotal} vectors")


print("saving faiss index file for subsequent search".upper())
faiss.write_index(index, INDEX_FILE_NAME_TO_SAVE_TO_DISK)

# SAVE ID LIST AS A NUMPY FILE
print("saving our id list as .npy file")
np.save( NUMPY_INDEX_FILE_TO_SAVE, np.array(id_list) )