# A – Analyze: Analyze song data for relevance, popularity, or specific criteria (e.g., lyrics, genre).
# N – Narrow: Narrow down the list by filtering out songs that don't meet certain conditions (e.g., release date, lyrical content, or popularity threshold).
# I – Identify: Identify the top 6 or 8 songs from the filtered results based on an algorithm that evaluates quality or matching criteria (e.g., lyrical depth, mood).

# L – Lyrical: Focus on the lyrics' depth, meaning, and creativity.
# U – Understanding: Gain a deep understanding of how these lyrics connect with listeners emotionally and thematically.
# S – Song: Evaluate the song's overall structure, flow, and musical arrangement.
# O – Organization: Organize the songs based on lyrical strength and cohesion, making sure they fit the purpose (such as mood, message, or theme).

from ast import literal_eval
import datetime
from json import load
from operator import index
from pprint import pprint
from random import choice as choose
from random import choices
from time import time
from regex import F
from scanningDir import songCollector, songChecker,songSearch
from re import findall

with open("wordSongsIndex.json", 'r', encoding='utf-8') as f:
    wordSongs = load(f)["SongNum"]
with open("REDergaran.json", 'r', encoding='utf-8') as f:
    REDergaran = load(f)["SongNum"]

def sang_once(song_num, book = 'New'):
    return book

def getSong(book:str, songnum:str, batch = 0) -> dict:
    """
    Retrieves a song from a JSON file based on the provided book and song number. The options are 'old', 'new', 'redergaran', and 'wordsongsindex'.

    Args:
        book (str): The book from which to retrieve the song.
        songnum (str): The number of the song to retrieve.
        batch (int, optional): The batch number. Defaults to 0.

    Returns:
        dict: A dictionary containing the song data.
    """
    if batch == 0:
        from json import load
        if book.lower() == "old" or book.lower() == "wordsongsindex": return wordSongs[songnum]
        else: return REDergaran[songnum]
    else:
        pass
    
def collect_all_songs(only_sunday=False, include_sunday=False) -> dict:
    """Returns all songs sang before a 3-month period.

    Args:
        only_sunday (bool, optional): return only sunday songs. Defaults to False.
        include_sunday (bool, optional): All songs, so Tue Thur and Sunday. Defaults to False.

    Returns:
        found_songs (dict): Dict of only the sogns that meet the specified reqs
    """
    with open('songs_cleaned.json', 'r', encoding='utf-8') as f:
        data = load(f)
    
    found_songs = {}
    for key in data:
        file_date = key
        file_date = findall(r"(.*\d)", file_date)[0]
        date_format = "%m.%d.%y"
        current_date = datetime.date.today()
        file_date = datetime.datetime.strptime(file_date, date_format) # file_date is now a datetime object
        # search_window = (current_date + datetime.timedelta(days=-90))#.strftime('%m.%d.%y')
        search_window = datetime.datetime.combine(current_date + datetime.timedelta(days=-90), datetime.time.min)
        if include_sunday:
            if file_date < search_window:
                found_songs[key] = {
                        'songList': data[key]['songList'],
                        'basePth': data[key]['basePth'],
                    }
        elif not only_sunday:
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

def get_a_unknown_song():
    filtered_songs = {}
    with open("known_songs.json", 'r') as f:
        known_songs:dict = load(f)
        wanted_keys = ["isWeekday"]
        for songnum in known_songs['New']:
            for key in wanted_keys:
                if known_songs['New'][songnum][key]:
                    if filtered_songs.get(songnum,None) == None: ## To make an empty dir, and not to if it exists
                        filtered_songs[songnum] = {}
                    if not songSearch(songnum, 'New'):
                        filtered_songs[songnum][key] = known_songs['New'][songnum][key]
    
    # choices()
    print("Here are some unknowns that we could potentially sing today: ",choices(list(filtered_songs), k=2)) 

def find_weekday_songs() -> dict:
    """
    Finds middle day songs by analyzing and narrowing down the list of songs 
    that have not been sung in the last 3 months, and then identifies the top 
    songs based on certain criteria.

    Returns:
        dict: A dictionary of the top songs that have not been sung in the last 3 months.
    """
    # TODO: Check to see if a song has been sung more than once, in a not so computationally expensive way
    # print("M.O.S.O. is annoying A.N.I. Quyr...")
    # print("Begin Analyzing, Narrowing, and Identifying the perfect worship list...")
    # sang_in_last_3months = songCollector(ignore_sundays=True)
    sang_in_last_3months = songCollector(ignore_sundays=True, three_month_window=False, search_range=180) # increasing search range to get songs sang longer ago
    sang_in_last_year = songCollector(three_month_window=False, search_range=360, ignore_sundays=True)
    all_songs_sang = collect_all_songs(include_sunday=True)
    # Just read the first two songs as the opening songs instead of looking for them
    # maybe, just maybe, filter out sundays
    # also add a date checking so no 
    possible_opening_songs = []
    possible_latter_half_songs = []
    for key in all_songs_sang:
        if not sang_in_last_3months.get(key, None): #Filters for songs that are not in the last 3 months
            possible_songs: list = literal_eval(all_songs_sang[key]["songList"]) # gets a list of songs sang on that day
            try:
                if not ("Old" in possible_songs[0] and "Old" in possible_songs[1]):
                    possible_opening_songs.append(possible_songs[0:2])
                    possible_opening_songs.append(possible_songs[2:4]) # only wor
                    possible_opening_songs.append(possible_songs[4:6])
            except:
                print(possible_songs)
    temp = []
    for song_pairs in possible_opening_songs:
        try:
            song_pair1 = song_pairs[0]
            song_pair2 = song_pairs[1]
        except:
            # no two pair, sometimes its only 5 not 6
            # so no even pair found, therefore just pass
            pass
            
        # The issue here is that I am checking tuesday & thursdayfiles
        # ofc its not going to apear in the last 3 months
        # because I am checking only for sundays
        song_1_sang_in_last_3months = songChecker(book=song_pair1[0], songNum=song_pair1[1], ignore_sundays=True) #and songChecker(book=song_pair1[0], songNum=song_pair1[1], ignore_sundays=False)
        song_2_sang_in_last_3months = songChecker(book=song_pair2[0], songNum=song_pair2[1], ignore_sundays=True) #and songChecker(book=song_pair2[0], songNum=song_pair2[1], ignore_sundays=False)
        if not ( song_1_sang_in_last_3months or song_2_sang_in_last_3months ):
            temp.append(song_pairs)

    latter_half_songs: list = choices(temp, k=3)
    # print(f"This is today's song order:\n{latter_half_songs}")
    # print("This is today's song order:")
    # print("The A.N.I. algorithm thinks this should be today's song order:")
    with open("REDergaran.json", 'r', encoding="utf-8") as f:
        REDergaran = load(f)
    songlist = {}
    ct = 1
    for song_pairs in latter_half_songs:
        # must do songs, bc as of now its a pair of two
        for song in song_pairs: # song = (book,songNum), song_pairs = [(book,songNum),(book,songNum)]
            song_check = songChecker(book=song[0], songNum=song[1],three_month_window=False)
            songlist[ct] = {
                'songnum': song[1],
                'title': REDergaran['SongNum'][song[1]]['Title'],
                'date': song_check[1] if isinstance(song_check, tuple) else "N/A"
            }
            # try:
            #     print(f"{song[1]} {REDergaran['SongNum'][song[1]]['Title']}\n\tThis song was last sang on {song_check[1]}")
            # except:
            #     pass
            # songlist.append([f"{song[1]} {REDergaran['SongNum'][song[1]]['Title']}\n\tThis song was last sang on {song_check[1]}",(datetime.datetime.strptime(song_check[1], '%m.%d.%y')).strftime('%A')])
            try:
                songlist[ct]['weekday'] = (datetime.datetime.strptime(song_check[1], '%m.%d.%y')).strftime('%A')
                # print(f"This song was last sang on a {songlist[ct]['weekday']}")
            except:
                pass
            ct += 1
        # compatibility.get_transition_recommendation(song_pairs)
        # print(f"This has an approx. musical compatability of ...")

    
    return songlist

## TODO: Add a check to make sure that the song has been sang at least once
def find_sunday_song(only_first_two_songs=False, only_worship_songs=False, only_last_two_songs=False):
    """
    Finds a song or a list of songs based on the given parameters.

    Args:
        only_first_two_songs (bool): If True, returns only the first two songs. Defaults to False.
        only_worship_songs (bool): If True, returns only the worship songs (3rd to 5th songs). Defaults to False.
        only_last_two_songs (bool): If True, returns only the last two songs. Defaults to False.

    Returns:
        list: A list of reccommended songs based on the given parameters.
    """
    # Only for sunday songs
    sang_in_last_3months = songCollector(sunday_only=True)
    all_songs_sang = collect_all_songs(only_sunday=True)
    possible_sunday_songs = []
    for key in all_songs_sang: # only doing this so I don't have to make another list
        if not sang_in_last_3months.get(key, None):
            possible_songs: list = literal_eval(all_songs_sang[key]["songList"])
            if only_first_two_songs:
                possible_sunday_songs.append(possible_songs[0:2])
            elif only_worship_songs:
                possible_sunday_songs.append(possible_songs[2:6])
            elif only_last_two_songs:
                possible_sunday_songs.append(possible_songs[6:8])
            else:
                # In this option, all we do is choose an exact order from a past sunday
                possible_sunday_songs.append(possible_songs)
    ## TODO: Add a feature to check that this not a one off and not sang as first song
    choice = choose(possible_sunday_songs)
    temp = []
    for song in choice:
        index = getSong(book=song[0], songnum=song[1])
        temp.append([song[0], song[1], index["Title"]])
    choice = temp
    # Keep picking until we get a list of 8 songs
    # while len(choice) < 8:
    #     choice = choose(possible_sunday_songs)
    # Return the final list of songs
    return choice
    # return choose(possible_sunday_songs)

# print(f"Haven't sang this in a while!\nOpening:{find_sunday_song(only_first_two_songs=True)}\nWorship:{find_sunday_song(only_worship_songs=True)}\nLast:{find_sunday_song(only_last_two_songs=True)}")

def get_weekday_song():
    available_songs = collect_all_songs() # Songs not sang 3mths ago
    possible_songs: dict[str, dict[dict, datetime.datetime]] = {
        "Old": {},
        "New": {},
    } # Used for date verification
    songs = []#used for random pick

    # Assemble all songs into a long list then pick some random ones from there.
    for date, song_info in available_songs.items():
        # print(date, literal_eval(song_info["songList"]))
        song_list = literal_eval(song_info["songList"])
        file_date = findall(r"(.*\d)", date)[0]
        date_format = "%m.%d.%y"
        file_date = datetime.datetime.strptime(file_date, date_format) # file_date is now a datetime object
        for song in song_list:
            book: str = song[0]
            song_num: str = song[1]
            exists: datetime.datetime | bool = possible_songs[book].get(song_num, False)
            if exists:
                # does not account for alt songs with same words, but different numbers
                if exists < file_date:
                    # simple logic to get the most recent date
                    possible_songs[book][song_num] = file_date
            else:
                # could store it as a string, but this is eaiser for future comaprisons
                possible_songs[book][song_num] = file_date
                songs.append(f"{song_num}_{book}")

    # Generate the list of weights:
    # make weights more skewing toward files
    # that are older sucha s 1.5-2yrs older.
    # btw: need to do this after the for loop above
    # so that we will have the most recent song date
    weights = []
    YR_IN_SECONDS = 31540000
    two_yrs_ago = datetime.datetime.fromtimestamp(time()-YR_IN_SECONDS*2)
    one_yr_ago = datetime.datetime.fromtimestamp(time()-YR_IN_SECONDS)
    three_mths_ago = datetime.datetime.fromtimestamp(time()-YR_IN_SECONDS*0.25)#12/4=3Time for 3mths
    for song in collected_songs:
        base_weight = 1
        (song_num, book) = song.split('_')
        # get the latest date sang
        song_date = possible_songs[book][song_num]
        if two_yrs_ago > song_date:
            base_weight = 10
        elif one_yr_ago > song_date:
            base_weight = 5
        elif three_mths_ago > song_date:
            # Song date is smaller than 3 mth date, then it was longer than 3 mth ago
            weights.append(base_weight)
        else:
            collected_songs.remove(song)


        # pprint(song_date if song_date < datetime.datetime(year=2023, month=12, day=30) else None)

    results: list[str] = choices(songs, weights=weights, k=6)
    songlist = {}
    ct = 1
    for result in results:
        (song_num, book) = result.split('_')
        song_data = getSong(book, song_num)
        songlist[ct] = {
            'songnum': song_num,
            'title': song_data['Title'],
            'date': possible_songs[book][song_num].strftime("%m.%d.%Y"),
            'book': book,
             'weekday': possible_songs[book][song_num].strftime('%A')
        }
        ct+=1

    return songlist


if "__main__" == __name__:
    # find_weekday_songs()
    # get_a_unknown_song()
    # pprint(collect_all_songs())
    pprint(get_weekday_song())