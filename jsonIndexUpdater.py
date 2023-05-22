import json, re

oldBook = True # if True then song is from old book, if False then song is from new book

oldBook_pth = "wordSongsIndex.json"
Ergaran_pth = "ergaran.json"
redErgaran_pth = "REDergaran.json"

songNum = "312"

def latestVer(jsonIndex, songNum):
    # for x in jsonIndex["SongNum"][songNum]:
    print(str(jsonIndex["SongNum"][songNum]))
    # print(re.search(r"(v[/d*])", jsonIndex["SongNum"][songNum]))



# this part it made to update the indexes
# method logic:
# 1. check if song exists in relevant book/index
# 2. if so, append to index, "version", and "latestVersion"
# 2.1 Based on this info the program needs to generate a suitable filepath to be logged and saved.
# 2.5 if not, append to index, "SongNum", "Title", "version", and "latestVersion"

if oldBook:
    #no matter if in or not in old book yet, I have to open the file, however I can check its existence with a simple [songnum][num]
    with open(oldBook_pth, "r", encoding='utf-8') as f:
        oldBook_pth = json.load(f)

    # filepth = "relative filepath" + latestVer(jsonIndex=oldBook_pth, songNum=songNum) # type: ignore
    latestVer(jsonIndex=oldBook_pth, songNum=songNum)

    # if oldBook_pth["SongNum"][songNum]: #this means, if the song exists in the old book then ...
    #     oldBook_pth["SongNum"][songNum]["version"] = filepth
    #     oldBook_pth["SongNum"][songNum]["latestVersion"] = filepth
