import chromadb
from os import environ as env
client = chromadb.PersistentClient(path="{}\\documents\\code\\python\\.chroma".format(env.get("OneDrive")))
collection = client.get_collection(name="songs")
search = collection.query(
    query_texts="Շալոմ բարեկամներ Տիրոջմով շալոմ Շալոմ Աստծո մարդիկ",
    n_results=10,
    # where={"metadata_field": "is_equal_to_this"},
    # where_document={"$contains":"search_string"}
)

print('Song Words',search['documents'],"\nSongNum, Book:",search['metadatas'])