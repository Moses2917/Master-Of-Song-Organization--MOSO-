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
    from json import load, dump
    with open('songs_cleaned.json', 'r', encoding='utf-8') as f:
        all_sang_songs = load(f)
    songs = {
        'New': {}, #add a bool val. To tell the algo to not pick it?
        'Old': {}
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
                        songs['New'][song] = {
                            'Known'  : False,
                            'Sang'   : False, # Kinda redundant, but I would rather have it than not, just in case future me decides to go in another direction
                            'isSunday': False,
                            'isHoliday': False,
                            'isWeekday': False,
                            'checked'    : False,
                            }
                    else:
                        songs['Old'][song] = {
                            'Known'    : False,
                            'Sang'     : False, # Kinda redundant, but I would rather have it than not, just in case future me decides to go in another direction
                            'isSunday' : False,
                            'isHoliday': False,
                            'isWeekday': False,
                            'checked'  : False,
                            }
                    # not_sang.append(song)
                
    # found = search_song(all_sang_songs,'360',"New",fast_method=True)
    print(songs)
    with open('known_songs.json', 'w', encoding='utf-8') as f:
        dump(songs, f, ensure_ascii=False, indent=4)
# get_all_unknown_songs()
def get_a_song():
    with open('known_songs.json', 'r', encoding='utf-8') as f:
        songs = load(f)
    for book in songs:
        for song in songs[book]:
            if (not songs[book][song]['checked']) and (not songs[book][song]["skipped"]):
                return (song, book)

def get_skipped_songs() -> list:
    with open('known_songs.json', 'r', encoding='utf-8') as f:
        songs = load(f)
    skipped_songs = []
    for book in songs:
        for song in songs[book]:
            if songs[book][song]["skipped"]:
                skipped_songs.append((song,book)) ## for dropdown 
    return skipped_songs

#TODO: Add a skiping feature, then in a dropdown menu show only the skipped values.

def update_known_songs(book:str, song:str, **kwargs):
    """
    Updates the known_songs.json file with information about a song.

    Args:
        book (str): The name of the book containing the song
        song (str): The name of the song to update
        **kwargs: Arbitrary keyword arguments that can include:
            Known (bool): Whether the song is known (default: False)
            Sang (bool): Whether the song has been sung (default: False)
            isSunday (bool): Whether it's a Sunday song (default: False)
            isHoliday (bool): Whether it's a holiday song (default: False)
            isWeekday (bool): Whether it's a weekday song (default: False)
            checked (bool): Whether the song has been checked (default: True)
            skipped (bool): Whether the song was skipped (default: False)

    Returns:
        None: The function writes directly to the JSON file

    Example:update_known_songs(book, songnum, isHoliday, isSunday, isWeekday, known)
        >>> update_known_songs("old", "1", Known=True, isSunday=True)
        >>> update_known_songs("new", "312", Known=True, isSunday)
    """
    defaults = {
        'Known': False,
        'Sang': False,
        'isSunday': False,
        'isHoliday': False,
        'isWeekday': False,
        'checked': True,
        'skipped': False
    }
    with open('known_songs.json', 'r', encoding='utf-8') as f:
        songs = load(f)

    # Update defaults with any provided kwargs
    song_data = defaults.copy()
    song_data.update(kwargs)
    songs[book][song] = song_data
    with open('known_songs.json', 'w', encoding='utf-8') as f:
        dump(songs, f, ensure_ascii=False, indent=4)

if "__main__" == __name__:
    print(get_skipped_songs())