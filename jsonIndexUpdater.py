import json, re

oldBook = False # if True then song is from old book, if False then song is from new book

oldBook_pth = "wordSongsIndex.json"
Ergaran_pth = "ergaran.json"
redErgaran_pth = "REDergaran.json"

songNum = "371"

def latestVer(jsonIndex, songNum:str):
    """Finds latest version of given songNum in given json index, 
    if can't find it creates one with empty Title, Version/Latest Version"""

    try:
        for attr in jsonIndex["SongNum"][songNum]:
            print(re.search(r"(v[\d*])", attr))
    except:
        print("This song number has not been indexed yet")
        print("Adding index...")
        jsonIndex['SongNum'][songNum] = {} #create a directory with that song number, and empty values
        jsonIndex['SongNum'][songNum]["Title"] = ""        
        jsonIndex['SongNum'][songNum]["latestVersion"] = ""
        jsonIndex['SongNum'][songNum]["v1"] = ""

#had to make a seperate functions bc python does not support function overloading :(
def latestVerErg(jsonIndex, songNum:str):
    """Finds latest version of given songNum in given json index, 
    if can't find it creates one with empty Title, Version/Latest Version"""

    try:
        for attr in jsonIndex["SongNum"][songNum]:
            print(re.search(r"(v[\d*])", attr))
    except:
        print("This song number has not been indexed yet")
        print("Loading another index...")
        ##Put a try loop just in a case the song is not in here!!!
        with open(redErgaran_pth, "r", encoding='utf-8') as f:
            redErgaran_Index = json.load(f)
            # latestVerErg(redErgaran_Index)   #lol imagine making this recursive
        jsonIndex['SongNum'][songNum] = redErgaran_Index['SongNum'][songNum] #create a directory with that song number, and empty values
        # jsonIndex['SongNum'][songNum]["Title"] = ""        
        # jsonIndex['SongNum'][songNum]["latestVersion"] = ""
        # jsonIndex['SongNum'][songNum]["v1"] = ""

# this part it made to update the indexes
# method logic:
# 1. check if song exists in relevant book/index
# 2. if so, append to index, "version", and "latestVersion"
# 2.1 Based on this info the program needs to generate a suitable filepath to be logged and saved.
# 2.5 if not, append to index, "SongNum", "Title", "version", and "latestVersion"

if oldBook:
    #no matter if indexed or not, I have to open the file, however I can check its existence with a simple [songnum][num]
    with open(oldBook_pth, "r", encoding='utf-8') as f:
        oldBook_Index = json.load(f)

    # filepth = "relative filepath" + latestVer(jsonIndex=oldBook_pth, songNum=songNum) # type: ignore
    latestVer(jsonIndex=oldBook_Index, songNum=songNum)
    print(oldBook_Index["SongNum"][songNum])
    print("Debug String..")
    # if oldBook_pth["SongNum"][songNum]: #this means, if the song exists in the old book then ...
    #     oldBook_pth["SongNum"][songNum]["version"] = filepth
    #     oldBook_pth["SongNum"][songNum]["latestVersion"] = filepth

if not oldBook:
    #compare songNum with ergaran.json index, if not there pull info from REDergarn.json
    with open(Ergaran_pth, "r", encoding='utf-8') as f:
        Book_Index = json.load(f)

    # filepth = "relative filepath" + latestVer(jsonIndex=oldBook_pth, songNum=songNum) # type: ignore
    latestVerErg(jsonIndex=Book_Index, songNum=songNum)
    print(Book_Index["SongNum"][songNum])
    print("Debug String..")
