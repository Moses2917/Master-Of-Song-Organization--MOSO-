"""This file is just a proof of concept that was made a while back and is useless now
"""
import json
with open("ergaran.json", mode = 'r', encoding='utf-8') as f:
    file = json.load(f)
# if song num DNE in ergaran transfer it in from "REDergaran.json"
song_num = "10"
# if file['SongNum'][song_num]:
#     print(file['SongNum'][song_num])

try:
    file['SongNum'][song_num] # yes an I could just put an if statement here, but ask yourself why, why would I?
    print(file['SongNum'][song_num])
except:
    print("print(file['SongNum'][song_num])")