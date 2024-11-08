from json import load, dump
from ast import literal_eval
import datetime

def collect_all_songs(only_sunday=False) -> dict:
    from re import findall
    with open('songs_cleaned.json', 'r', encoding='utf-8') as f:
        data = load(f)
    
    found_songs = {}
    for key in data:
        file_date = key
        file_date = findall(r"(.*\d)", file_date)[0]
        date_format = "%m.%d.%y"
        file_date = datetime.datetime.strptime(file_date, date_format) # file_date is now a datetime object
        if not only_sunday:
            if file_date.strftime('%A') != "Sunday":
                found_songs[key] = {
                    'songList': data[key]['songList'],
                    'basePth': data[key]['basePth'],
                }
        else:
            if file_date.strftime('%A') == "Sunday":
                found_songs[key] = {
                    'songList': data[key]['songList'],
                    'basePth': data[key]['basePth'],
                }
    return found_songs
# The logic here is that if we have sang that song before, then we know it.
def get_all_unknown_songs():
    with open('songs_cleaned.json', 'r', encoding='utf-8') as f:
        all_sang_songs = load(f)
    songs = {
        'old': {}, #add a bool val. To tell the algo to not pick it?
        'new': {}
    }
    not_sang = []
    from scanningDir import search_song
    for book in ["REDergaran.json", "wordSongsIndex.json"]:
        with open(book, 'r', encoding='utf-8') as SongIndex:
            from json import load
            SongIndex: dict = load(SongIndex)
        for song in SongIndex["SongNum"]:
            # with concurrent.futures.ThreadPoolExecutor() as exec:
                # future = exec.submit(search_song,all_sang_songs,song,"New",fast_method=True)
                # found = future.result()
                found = search_song(all_sang_songs,song,"New",fast_method=True)
                if not found:
                    if "REDergaran" in book:
                        songs['new'][song] = {
                            'Known'  : False,
                            'Sang'   : False # Kinda redundant, but I would rather have it than not, just in case future me decides to go in another direction
                            }
                    else:
                        songs['old'][song] = {
                            'Known'  : False,
                            'Sang'   : False # Kinda redundant, but I would rather have it than not, just in case future me decides to go in another direction
                            }
                    # not_sang.append(song)
                
    # found = search_song(all_sang_songs,'360',"New",fast_method=True)
    print(songs)
    with open('known_songs.json', 'w', encoding='utf-8') as f:
        dump(songs, f, ensure_ascii=False, indent=4)

def get_a_song():
    with open('known_songs.json', 'r', encoding='utf-8') as f:
        songs = load(f)
    for book in songs:
        for song in songs[book]:
            if not songs[book][song]['Known']:
                return (song, book)

# def get_a_song(skip):
#     #skip is a song number to skip
#     with open('known_songs.json', 'r', encoding='utf-8') as f:
#         songs = load(f)
#     for book in songs:
#         for song in songs[book]:
#             if not songs[book][song]['Known'] and songs[book][song] != skip:
#                 return song

def update_known_songs(book, song):
    with open('known_songs.json', 'r', encoding='utf-8') as f:
        songs = load(f)
    songs[book][song]['Known'] = True
    with open('known_songs.json', 'w', encoding='utf-8') as f:
        dump(songs, f, ensure_ascii=False, indent=4)