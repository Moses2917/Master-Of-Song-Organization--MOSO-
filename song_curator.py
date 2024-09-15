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
print("Bugging A.N.I. Quyr...")
print("Awakening A.N.I. Quyr...\nAnalyzing, Narrowing, and Identifying the perfect worship setlist...")
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
    # Only for sunday songs
    if only_first_two_songs:
        return opening_songs
    elif only_worship_songs:
        return latter_half_songs[0]
    elif only_last_two_songs:
        return latter_half_songs[1]
    else:
        possible_sunday_redos = []
        sang_in_last_3months = songCollector(sunday_only=True)
        sang_in_last_year = songCollector(sunday_only=True,three_month_window=False, search_range=360)
        for key in sang_in_last_year:
            if not sang_in_last_3months.get(key, None):
                possible_sunday_redos.append(literal_eval(sang_in_last_year[key]["songList"]))

        return choose(possible_sunday_redos)

print(f"Haven't sang this in a while!\n{find_song()}")