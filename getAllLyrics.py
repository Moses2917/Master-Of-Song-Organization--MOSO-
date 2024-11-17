from time import time as today
from json import load
from os import environ as ENV
from docx import Document
from regex import D
basePth = ENV.get("OneDrive")
#open all files, get latest version and store lyrics in dict
# if songLyrics.get('latestChange',None) or do < today()

#templates for songLyrics
def template(songs_to_open_bool=True) -> dict:
    songLyrics = {
        'old': {},
        'new': {},
        'latestChange': today()
    }
    songs_to_open = {
        'old': {},
        'new': {}
    }
    return songs_to_open if songs_to_open_bool else songLyrics
def getAllLyricsDict() -> dict:
    with open('AllLyrics.json', 'r', encoding='utf-8') as f:
        return load(f)
        
def GetAllSongPths(songs_to_open,index:str, book = 'old'or'new',) -> dict:
    try:
        for songNum in index["SongNum"]:
            songPth_realative = index["SongNum"][songNum]['latestVersion']
            songPth_full = f"{basePth}\\{songPth_realative}"
            songs_to_open[book][songNum] = songPth_full
    except:
        print(f'This song threw an error: {index["SongNum"][songNum]}')
    return songs_to_open
def readLyrics(filePth:str) -> str:
    lyrics = ''
    doc = Document(filePth)
    for p in doc.paragraphs:
        lyrics += p.text
    
    if lyrics != '':
        return lyrics
    return None

def readLyrics(doc:Document) -> str:
    lyrics = ''
    # doc = Document(filePth)
    for p in doc.paragraphs:
        lyrics += p.text
    
    if lyrics != '':
        return lyrics
    return None

def updateSongLyrics(book:str, songNum:str, lyrics:Document):
    allLyrics = getAllLyricsDict()
    if book.lower() == 'old':
        allLyrics['old'][songNum] = readLyrics(lyrics)
    elif book.lower() == 'new':
        pass
    return None

def updateAllLyrics():
    #Gather all current songs.
    with open('AllLyrics.json', 'r', encoding='utf-8') as f:
        allLyrics = load(f)
    
    from os import environ as ENV

    onedrive = ENV.get('onedrive')

    from os import path

    

    return True

def getAllLyrics():
    songs_to_open = template()
    songLyrics = template(songs_to_open_bool=False)
    #Start from olds
    with open('wordSongsIndex.json', 'r', encoding='utf-8') as f:
        oldSongs = load(f)
        GetAllSongPths(oldSongs,'old')
    # Close file and continue with reading all red songs
    with open('REDergaran.json', 'r', encoding='utf-8') as f:
        newSongs = load(f)
        GetAllSongPths(newSongs,'new')
    # with open('test.json', 'w', encoding='utf-8') as f:
    #     from json import dump
    #     dump(songs_to_open,f,ensure_ascii=False,indent=4)
    for book in songs_to_open:
        for songNum in songs_to_open[book]:
            filePth = songs_to_open[book][songNum]
            lyrics = readLyrics(filePth)
            songLyrics[book][songNum] = lyrics
    with open('AllLyrics.json', 'w', encoding='utf-8') as f:
        from json import dump
        dump(songLyrics,f,ensure_ascii=False,indent=4)


if __name__ == "__main__":
    getAllLyrics()
