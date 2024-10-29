from json import load, dump
# Get a list of songs unknown.
# Pass those to the site
# mark off the ones that are now known
# Gather a list/dict of all the songs that have not been sang at all.
# Then based on that, ask user if we know it or not.
# Then mark it as ok to use. 

# load sang songs
with open('songs_cleaned.json', 'r', encoding='utf-8') as f:
    all_sang_songs = load(f)

# Create a dict of songs that have been sang
# Write a help func, that reads and writes to dict per book
songs = {
    'old': {},
    'new': {}
}
def readSongs(book:str, all_sang_songs:dict):
    for date in all_sang_songs:
        for songList in all_sang_songs[date]:
            songList = eval(songList) #cnvts str(list) -> list object
            