#load two json files
#old one has priority
#compare to see what nums old one doesn't have, and then add it
#celebrate


import json

# Load JSON files
with open('wordSongsIndex.json', 'r', encoding='utf-8') as f:
    wordsongs = json.load(f)

with open('pptsonginfo.json', 'r', encoding='utf-8') as f:
    PPTSONGS = json.load(f)

# Sort song numbers least to greatest
sorted_song_numbers = sorted(
    set(wordsongs["SongNum"].keys()) | set(PPTSONGS["SongNum"].keys()), key=int
)

# Iterate through sorted song numbers
for num in sorted_song_numbers:
    # Check if the entry exists in wordsongs
    if num not in wordsongs["SongNum"]:
        # Add the entry to wordsongs from PPTSONGS
        wordsongs["SongNum"][num] = PPTSONGS["SongNum"][num]

wordsongs["SongNum"] = dict(sorted(wordsongs["SongNum"].items(), key=lambda x: int(x[0])))

# Save the updated wordsongs JSON file
with open('updated_wordsongs.json', 'w', encoding='utf-8') as f:
    json.dump(wordsongs, f, ensure_ascii=False, indent=4)


