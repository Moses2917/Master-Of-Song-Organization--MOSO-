#load two json files
#old one has priority
#compare to see what nums old one doesn't have, and then add it
#celebrate

def unifiedErgaran():
    import json

    # Load JSON files
    with open('ergaran.json', 'r', encoding='utf-8') as f:
        ergaran = json.load(f)

    with open('REDergaran.json', 'r', encoding='utf-8') as f:
        REDergaran = json.load(f)

    # Sort song numbers least to greatest
    sorted_song_numbers = sorted(
        set(ergaran["SongNum"].keys()) | set(REDergaran["SongNum"].keys()), key=int
    )

    # Iterate through sorted song numbers
    for num in sorted_song_numbers:
        # Check if the entry exists in ergaran
        if num not in ergaran["SongNum"]:
            # Add the entry to ergaran from PPTSONGS
            ergaran["SongNum"][num] = REDergaran["SongNum"][num]

    ergaran["SongNum"] = dict(sorted(ergaran["SongNum"].items(), key=lambda x: int(x[0])))

    # Save the updated ergaran JSON file
    with open('updated_ergaran.json', 'w', encoding='utf-8') as f:
        json.dump(ergaran, f, ensure_ascii=False, indent=4)


#compareAttrs
#assume ergaran is base, and check if no attrs in it, then go to redergaran
import json
# Load JSON files
with open('updated_ergaran.json', 'r', encoding='utf-8') as f:
    ergaran = json.load(f)

with open('REDergaran.json', 'r', encoding='utf-8') as f:
    REDergaran = json.load(f)

#use the song attr 'key' to see if attrs and to know if switch necessary
for num in ergaran["SongNum"]:
    if not ('key' in ergaran["SongNum"][num]) or ergaran["SongNum"][num]['key'] == "":
        
        if 'key' in REDergaran["SongNum"][num]:
            ergaran["SongNum"][num]["key"] = REDergaran["SongNum"][num]["key"]
            ergaran["SongNum"][num]["speed"] = REDergaran["SongNum"][num]["speed"]
            ergaran["SongNum"][num]["style"] = REDergaran["SongNum"][num]["style"]
            ergaran["SongNum"][num]["song_type"] = REDergaran["SongNum"][num]["song_type"]
            ergaran["SongNum"][num]["timeSig"] = REDergaran["SongNum"][num]["timeSig"]
            ergaran["SongNum"][num]["Comments"] = REDergaran["SongNum"][num]["Comments"]
        
ergaran["SongNum"] = dict(sorted(ergaran["SongNum"].items(), key=lambda x: int(x[0])))

# Save the updated ergaran JSON file
with open('updated_ergaran.json', 'w', encoding='utf-8') as f:
    json.dump(ergaran, f, ensure_ascii=False, indent=4)