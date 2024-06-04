from pymongo import MongoClient
from os import environ as env
from docx import Document


uri = ""

# Create a new client and connect to the server
client = MongoClient(uri)
songDB = client.get_database("songs")
songDB = songDB.get_collection("allSongs")
from json import load
with open('REDergaran.json','r',encoding='utf-8') as f: #Do this one, and also "REDergaran"
    song_index = load(f)
    # book = 'Old'
didnt_find = []
for songNum in song_index['SongNum']:
    try:
        filePath = env.get("OneDrive")+"\\"+song_index['SongNum'][songNum]['latestVersion']
        doc = Document(filePath)
        word_doc = ""
        from random import random
        for p in doc.paragraphs:
            word_doc = word_doc + p.text
        songDB.insert_one({
            'lyrics': word_doc,
            'book': 'New',
            'songNum': songNum,
        })

    except:
        didnt_find.append(env.get("OneDrive")+"\\"+song_index['SongNum'][songNum]['latestVersion'])

with open("notFound.txt",'a',encoding='utf-8') as f:
    f.write(str(didnt_find))
print(songDB.count_documents())
