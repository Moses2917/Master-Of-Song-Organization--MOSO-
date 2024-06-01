import chromadb
from chromadb.utils import embedding_functions
#sentance_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L12-v2")
from os import environ as env
client = chromadb.PersistentClient(path="{}\\documents\\code\\python\\.chroma".format(env.get("OneDrive")))
print(client.list_collections())
collection = client.get_collection(name="indivPara")#,embedding_function=sentance_transformer_ef)
search = collection.query(
    query_texts="Աստված մարդ չէ որ սուտ խոսի",
    n_results=10,
    # where={"metadata_field": "is_equal_to_this"},
    # where_document={"$contains":"search_string"}
)

print('Song Words',search['documents'],"\nSongNum, Book:",search['metadatas'])