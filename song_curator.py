# A – Analyze: Analyze song data for relevance, popularity, or specific criteria (e.g., lyrics, genre).
# N – Narrow: Narrow down the list by filtering out songs that don't meet certain conditions (e.g., release date, lyrical content, or popularity threshold).
# I – Identify: Identify the top 6 or 8 songs from the filtered results based on an algorithm that evaluates quality or matching criteria (e.g., lyrical depth, mood).

# L – Lyrical: Focus on the lyrics' depth, meaning, and creativity.
# U – Understanding: Gain a deep understanding of how these lyrics connect with listeners emotionally and thematically.
# S – Song: Evaluate the song's overall structure, flow, and musical arrangement.
# O – Organization: Organize the songs based on lyrical strength and cohesion, making sure they fit the purpose (such as mood, message, or theme).

from ast import literal_eval
from operator import index
from random import choice as choose
from random import choices
from scanningDir import songCollector
# attr_finder.attrFinder.attributeSearch()
print("Annoying A.N.I. Quyr...")
print("Begin Analyzing, Narrowing, and Identifying the perfect worship list...")
sang_in_last_3months = songCollector(ignore_sundays=True)
sang_in_last_year = songCollector(three_month_window=False, search_range=360, ignore_sundays=True)

# Just read the first two songs as the opening songsinstead of looking for them
# maybe, just maybe, filter out sundays
# also add a date checking so no 
possible_opening_songs = []
possible_latter_half_songs = []
for key in sang_in_last_year:
    if not sang_in_last_3months.get(key, None): #Filters for songs that are not in the last 3 months
        possible_songs: list = literal_eval(sang_in_last_year[key]["songList"]) # gets a list of songs sang on that day
        if not ("Old" in possible_songs[0] or "Old" in possible_songs[1]):
            possible_opening_songs.append(possible_songs[0:2])
        # possible_residual_songs.append(possible_songs[2:])
        for residual_song in possible_songs[2:]:
            if residual_song[0] != "Old":
                possible_latter_half_songs.append(residual_song)
        # From here I could do two things:
        # 1. Randomly select 2 songs from the list
        # 2. Randomly select 1 song pair from the list
        
        # Going to implement 2 for now
        # Randomly select 1 song pair from the list
opening_songs: list = choose(possible_opening_songs)
# print(possible_residual_songs, possible_opening_songs[-1])
latter_half_songs: list = choices(possible_latter_half_songs, k=2)
possible_latter_half_songs.remove(latter_half_songs[0])#.remove(latter_half_songs[1])
latter_half_songs.append(choices(possible_latter_half_songs, k=2))
print(f"This is today's song order:\n{opening_songs}{latter_half_songs}")


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

print(f"Haven't sang this in a while!\nOpening:{find_song(only_first_two_songs=True)}\nWorship:{find_song(only_worship_songs=True)}\nLast:{find_song(only_last_two_songs=True)}")