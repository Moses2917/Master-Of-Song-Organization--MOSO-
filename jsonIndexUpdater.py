import json, re

oldBook = True # if True then song is from old book, if False then song is from new book

oldBook_pth = "wordSongsIndex.json"
Ergaran_pth = "ergaran.json"
redErgaran_pth = "REDergaran.json"

songNum = "151"

def latestVer(jsonIndex, songNum:str):
    """Finds latest version of given songNum in given json index, 
    if can't find it creates one with empty Title, Version/Latest Version"""
    latestV = 0
    try:
        for attr in jsonIndex["SongNum"][songNum]:
            if "v" in attr:
                v = int(re.findall(r"([\d].*)", attr)[0])
                if v > latestV:
                    latestV = v            
        print("The latest version is:", latestV)
        return latestV
    except:
        print("This song number has not been indexed yet")
        print("Adding index...")
        jsonIndex['SongNum'][songNum] = {} #create a directory with that song number, and empty values
        jsonIndex['SongNum'][songNum]["Title"] = ""        
        jsonIndex['SongNum'][songNum]["latestVersion"] = ""
        jsonIndex['SongNum'][songNum]["v1"] = ""
        return None

#had to make a seperate functions bc python does not support function overloading :(
def latestVerErg(jsonIndex, songNum:str):
    """Finds latest version of given songNum in given json index, 
    if can't find it creates one with empty Title, Version/Latest Version"""
    latestV = 0
    try:
        for attr in jsonIndex["SongNum"][songNum]:
            if "v" in attr:
                v = int(re.findall(r"([\d].*)", attr)[0])
                if v > latestV:
                    latestV = v
        
        print("The latest version is:", latestV)
        return latestV
    except:
        print("This song number has not been indexed yet")
        print("Loading another index...")
        with open(redErgaran_pth, "r", encoding='utf-8') as f:
            redErgaran_Index = json.load(f)
            # latestVerErg(redErgaran_Index)   #lol imagine making this recursive
        if songNum in redErgaran_Index['SongNum']:
            jsonIndex['SongNum'][songNum] = redErgaran_Index['SongNum'][songNum] #create a directory with that song number, and values from REDergaran.json
            
            #This for loop is a bit redundent, however I want to cover 100% of all cases, 
            for attr in redErgaran_Index["SongNum"][songNum]:
                if "v" in attr:
                    v = int(re.findall(r"([\d].*)", attr)[0])
                    if v > latestV:
                        latestV = v            
            print("The latest version is:", latestV)
            return latestV
        else:
            jsonIndex['SongNum'][songNum] = {} #create a directory with that song number, and empty values
            jsonIndex['SongNum'][songNum]["Title"] = ""        
            jsonIndex['SongNum'][songNum]["latestVersion"] = ""
            jsonIndex['SongNum'][songNum]["v1"] = ""  
            return None


# this part it made to update the indexes
# method logic:
# 1. check if song exists in relevant book/index
# 2. if so, append to index, "version", and "latestVersion"
# 2.1 Based on this info the program needs to generate a suitable filepath to be logged and saved.
# 2.5 if not, append to index, "SongNum", "Title", "version", and "latestVersion"

if oldBook:
    with open(oldBook_pth, "r", encoding='utf-8') as f:
        oldBook_Index = json.load(f)

    # filepth = "relative filepath" + latestVer(jsonIndex=oldBook_pth, songNum=songNum) # type: ignore
    lv = latestVer(jsonIndex=oldBook_Index, songNum=songNum)
    print(oldBook_Index["SongNum"][songNum])
    print("Debug String..")


if not oldBook:
    #compare songNum with ergaran.json index, if not there pull info from REDergarn.json
    with open(Ergaran_pth, "r", encoding='utf-8') as f:
        Book_Index = json.load(f)

    # filepth = "relative filepath" + latestVer(jsonIndex=oldBook_pth, songNum=songNum) # type: ignore
    lv = latestVerErg(jsonIndex=Book_Index, songNum=songNum)
    print(Book_Index["SongNum"][songNum])
    print("Debug String..") # Note: Funny enough the test num I used does not have a corresponding title, which does not really matter that much, however I could add some functionality to fill it later on
    #However I'm not so sure about just saving files in ergaran as songnum.docx like I already do in red ergaran
