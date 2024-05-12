import chromadb
from os import environ as env
from docx import Document
client = chromadb.PersistentClient(path="{}\\documents\\code\\python\\.chroma".format(env.get("OneDrive")))
# try:
#     pass
#     collection = client.create_collection(name="songs")
# except:
#     collection = client.get_collection(name="songs")
# collection = client.get_collection(name="songs")
collection = client.create_collection(name="indivPara")
from json import load
with open('wordSongsindex.json','r',encoding='utf-8') as f: #Do this one, and also "REDergaran"
    song_index = load(f)
    # book = 'Old'
didnt_find = []
for songNum in song_index['SongNum']:
    try:
        filePath = env.get("OneDrive")+"\\"+song_index['SongNum'][songNum]['latestVersion']
        doc = Document(filePath)
        word_doc = ""
        for p in doc.paragraphs:
            word_doc = word_doc + p.text
        word_doc = word_doc + songNum + "Old"
        from hashlib import sha256
        id = sha256(word_doc.encode()).hexdigest()
        collection.add(
            documents=word_doc,
            metadatas=[{
                'book': "Old",
                'songnum': songNum,
            }],
            ids=id
        )
    except:
        didnt_find.append(env.get("OneDrive")+"\\"+song_index['SongNum'][songNum]['latestVersion'])

with open("notFound.txt",'a',encoding='utf-8') as f:
    f.write(str(didnt_find))
print(collection.peek())

