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
from random import choice as choose
from random import choices
from scanningDir import songCollector, songChecker
from re import findall

def collect_all_songs() -> dict:
    with open('songs_cleaned.json', 'r', encoding='utf-8') as f:
        data = load(f)
    
    found_songs = {}
    for key in data:
        file_date = key
        file_date = findall(r"(.*\d)", file_date)[0]
        date_format = "%m.%d.%y"
        file_date = datetime.datetime.strptime(file_date, date_format) # file_date is now a datetime object
        if file_date.strftime('%A') != "Sunday":
            found_songs[key] = {
                'songList': data[key]['songList'],
                'basePth': data[key]['basePth'],
            }
    # if date2.strftime('%A') != "Sunday"


print("Annoying A.N.I. Quyr...")
print("Begin Analyzing, Narrowing, and Identifying the perfect worship list...")
sang_in_last_3months = songCollector(ignore_sundays=True)
sang_in_last_year = songCollector(three_month_window=False, search_range=360, ignore_sundays=True)
all_songs_sang = collect_all_songs()
# Just read the first two songs as the opening songs instead of looking for them
# maybe, just maybe, filter out sundays
# also add a date checking so no 
possible_opening_songs = []
possible_latter_half_songs = []
for key in sang_in_last_year:
    if not sang_in_last_3months.get(key, None): #Filters for songs that are not in the last 3 months
        possible_songs: list = literal_eval(sang_in_last_year[key]["songList"]) # gets a list of songs sang on that day
        if not ("Old" in possible_songs[0] or "Old" in possible_songs[1]):
            possible_opening_songs.append(possible_songs[0:2])
            possible_opening_songs.append(possible_songs[2:4]) # only wor
            possible_opening_songs.append(possible_songs[4:6])
temp = []


for song_pairs in possible_opening_songs:
    # must do songs, bc as of now its a pair of two
    last_3_months = True
    # for song in song_pairs:
    # if not(song_pairs[0] in sang_in_last_3months and song_pairs[1] in sang_in_last_3months):
    song_pair1 = song_pairs[0]
    song_pair2 = song_pairs[1]
    # Could also add a reroller for a specific pair
    if not (songChecker(book=song_pair1[0], songNum=song_pair1[1]) and songChecker(book=song_pair2[0], songNum=song_pair2[1])):
        temp.append(song_pairs)
            
# print(sang_in_last_3months)
# opening_songs: list = choose(possible_opening_songs)
# latter_half_songs: list = choices(possible_latter_half_songs, k=2)
# possible_latter_half_songs.remove(latter_half_songs[0])#.remove(latter_half_songs[1])
# latter_half_songs.append(choices(possible_latter_half_songs, k=2))
# print(f"This is today's song order:\n{opening_songs}{latter_half_songs}")
latter_half_songs: list = choices(temp, k=3)
# print(f"This is today's song order:\n{latter_half_songs}")
print("This is today's song order:")
with open("REDergaran.json", 'r', encoding="utf-8") as f:
    REDergaran = load(f)
for song_pairs in latter_half_songs:
    # must do songs, bc as of now its a pair of two
    for song in song_pairs:
        print(f"{song[1]} {REDergaran['SongNum'][song[1]]['Title']}\n\tThis song was last sang in the last 3 months {songChecker(book=song[0], songNum=song[1])}")

def find_song(only_first_two_songs=False, only_worship_songs=False, only_last_two_songs=False):
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
    sang_in_last_year = songCollector(sunday_only=True,three_month_window=False, search_range=360)
    possible_sunday_songs = []
    for key in sang_in_last_year: # only doing this so I don't have to make another list
        if not sang_in_last_3months.get(key, None):
            possible_songs: list = literal_eval(sang_in_last_year[key]["songList"])
            if only_first_two_songs:
                possible_sunday_songs.append(possible_songs[0:2])
                # return opening_songs
            elif only_worship_songs:
                # return latter_half_songs[0]
                possible_sunday_songs.append(possible_songs[2:6])
            elif only_last_two_songs:
                possible_sunday_songs.append(possible_songs[6:8])
            else:
                # In this option, all we do is choose an exact order from a past sunday
                possible_sunday_songs.append(possible_songs)
                
                #DO NOTHING JUST SEND possible_songs
                
                # for key in sang_in_last_year:
                #     if not sang_in_last_3months.get(key, None):
                # possible_sunday_full_redos.append(literal_eval(sang_in_last_year[key]["songList"]))
                
    choice = choose(possible_sunday_songs)
    # Keep picking until we get a list of 8 songs
    # while len(choice) < 8:
    #     choice = choose(possible_sunday_songs)
    # Return the final list of songs
    return choice
    # return choose(possible_sunday_songs)

# print(f"Haven't sang this in a while!\nOpening:{find_song(only_first_two_songs=True)}\nWorship:{find_song(only_worship_songs=True)}\nLast:{find_song(only_last_two_songs=True)}")