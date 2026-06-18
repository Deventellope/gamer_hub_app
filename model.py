from pymongo import MongoClient
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from bson import ObjectId



# Establish database connection
client = MongoClient("mongodb://localhost:27017")

# load database
database= client["mydb"] # database name
database_table= database["movies"] # like a database  table

# collection.find({}) returns a Cursor object
# {} means "no filter" — give me everything
cursor = database_table.find({})

# load database documents into a list
docs = list(cursor)

print(f"total movies entries in db {len(docs)}".upper())


def convert_doc_to_string(all_document):

    for doc in all_document:
        # define search paramters

        release_date= doc.get()
        year= str(doc.get())
        movie_name= doc.get()
        plot= doc.get()
        directors= doc.get()
        actors= doc.get()
        length= doc.get()
        rated_pg= doc.get()
        language= doc.get()
        movie_type= doc.get()
        genre= doc.get()
        platform= doc.get()
        dvd= doc.get()
        ratings= doc.get()
        awards= doc.get()
        
        stringified_doc=f"""
            release_date:{release_date} 
            year:{year} 
            movie_name:{movie_name}
            plot:{plot}
            directors:{directors}
            actors:{actors}
            length:{length}
            rated_pg:{rated_pg}
            language:{language}
            movie_type:{movie_type}
            genre:{genre}
            platform:{platform}
            dvd:{dvd}
            ratings:{ratings}
            awards:{awards}
        """


        yield stringified_doc



# converts each doc to a string representation(serialization)    
stringified_docs= [convert_doc_to_string(doc) for doc in docs ]

embedding_model = SentenceTransformer("all-mpnet-base-v2")

# batch_size=32 means it processes 32 strings at once
# GPU would use batch_size=128+ for much faster throughput
# show_progress_bar shows a tqdm bar so you know it's alive on 100k docs

# converts each stringified to a 768D vector 
vectors = embedding_model.encode(
    embedding_model,
    batch_size=32,
    show_progress_bar=True,
    convert_to_numpy=True,   # return np.ndarray not torch.Tensor
)


# FAISS requires float32 convert from numpy defaults float64 
vector_embedding = vectors.astype(np.float32)

print(vectors.shape)
# → (100000, 768)
# 100000 rows (one per doc), 768 columns (one per dimension)

# shows the vector embedding of the strinfied_doc
print(vectors[0])

# store each document id to return vector search results via ID
# id_map[i] corresponds to vectors[i] and docs[i]
id_map = [str(d["_id"]) for d in docs]


# Verify alignment
print(id_map[0])    # → "507f1f77bcf86cd799439011"
print(stringified_docs[0])     # → "Interstellar 2014 ..."
print(docs[0])      # → {"_id": ObjectId("507f..."), "name": "Interstellar", ...}
# All three point to the same document — this alignment is everything


# At search time:
#   FAISS returns index position 0
#   id_map[0] = "507f1f77bcf86cd799439011"
#   MongoDB finds the doc with _id = ObjectId("507f1f77bcf86cd799439011")


# WHY NORMALISE?
# --------------
# mpnet was trained to put similar meanings close together
# using cosine similarity — so we MUST use cosine similarity at search time
# Normalising makes inner product == cosine similarity

faiss.normalize_L2(vector_embedding)

length_of_first_vector = np.linalg.norm(vectors[0])
print(length_of_first_vector)
# → 1.0000001 (tiny float rounding error, effectively 1.0)

dim   = vector_embedding.shape[1]   # 768
index = faiss.IndexHNSWFlat(dim, 32)

# index.add() walks through all 100k vectors and:
#   1. Assigns each vector a position (0, 1, 2, ...)
#   2. Finds its M nearest neighbors
#   3. Creates edges in the graph to those neighbors
#   4. Does this for each layer of the hierarchy
# This is the slow part of build — O(N log N)

print("Adding vectors to index...")
index.add(vector_embedding)

print(index.ntotal)
# ntotal is how many vectors are currently in the index

faiss.write_index(index, "docs.index")

# np.save stores the id_map list as a numpy binary file (.npy)
# We wrap in np.array() first so numpy knows how to serialise it
# The file stores all 100k MongoDB ID strings
np.save("id_map.npy", np.array(id_map))

print("Saved docs.index and id_map.npy")


# Directory now contains:
# docs.index   ← ~200-400MB depending on doc count
# id_map.npy   ← small, just strings

# This replaces the entire build pipeline on every run after the first
# Takes milliseconds vs potentially 30 minutes to rebuild

vector_index_db  = faiss.read_index("docs.index")

# allow_pickle=True is required because we saved Python strings
# (object dtype array) — numpy needs permission to unpickle objects
id_map = np.load("id_map.npy", allow_pickle=True).tolist()
# .tolist() converts numpy array back to a plain Python list

print(f"Loaded {index.ntotal} vectors")
# → Loaded 100000 vectors


#   QUERY TESTING
query = "space travel adventure in the 1990s"

# Embed exactly like we embedded documents — same model, same process
# We wrap in a list [] because encode() expects a list of strings
# Result shape is (1, 768) — one query, 768 dimensions
query_vec = embedding_model.encode(
    [query],
    convert_to_numpy=True ).astype(np.float32)

# Normalise for the same reason as before — cosine similarity via inner product
faiss.normalize_L2(query_vec)

print("QUERY VECTOR SHAPE:", query_vec.shape)
# → (1, 768)

print("QUERY VECTOR SHAPE index(0-5):", query_vec[0][:5])
# → [ 0.0312  -0.4521   0.1123   0.7821  -0.0234 ]
# First 5 of 768 numbers encoding "space travel adventure in the 1990s"


# index.search(query_vectors, k)
# Navigates the HNSW graph starting from the top layer
# Finds the k vectors whose meaning is closest to the query vector
# Returns two arrays each of shape (n_queries, k)

#   distances : cosine similarity scores, higher = more similar
#   indices   : positions in the index (maps to id_map positions)
distances, indices = vector_index_db.search(query_vec, k=5)

# We only sent one query so unwrap the batch dimension [0]
distances = distances[0]   # → [0.91, 0.87, 0.81, 0.74, 0.71]
indices   = indices[0]     # → [1, 4, 892, 1204, 3301]

results = []

for dist, idx in zip(distances, indices):

    # FAISS returns -1 if it couldn't find enough neighbors
    # (only happens if index has fewer docs than k)
    if idx == -1:
        continue

    # idx is the position in the FAISS index
    # id_map[idx] is the MongoDB _id string at that position
    # ObjectId() converts string back to BSON type MongoDB expects
    mongo_id = id_map[idx]
    doc      = collection.find_one({"_id": ObjectId(mongo_id)})

    if doc:
        results.append({
            "score": float(dist),
            "doc"  : doc
        })

# Print results
for rank, hit in enumerate(results, start=1):
    doc = hit["doc"]
    print(f"#{rank}  Score: {hit['score']:.4f}")
    print(f"     Name : {doc.get('name')}")
    print(f"     Year : {doc.get('year')}")
    print(f"     Desc : {doc.get('description', '')[:100]}...")
    print()

# → #1  Score: 0.9134  Apollo 13 (1995)
# → #2  Score: 0.8701  The Right Stuff (1983)
# → #3  Score: 0.8123  Gravity (2013)