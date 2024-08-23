
from regex import F


def attributeSearch() -> dict:
    """This inputs a list of attributes and the finds songs whose attributes match the input attributes.
    
    Input:
        list: A list of attributes
        example:
                Before:
                {key: false, speed: false, style: false, song_type: false, timeSig: false}
                After:
                {key: true, speed: true, style: false, song_type: false, timeSig: true}
    
    Returns:
        dict: A dictionary where the keys are the song numbers and the values are the dictionaries of the respective songs

    """
    ###TODO: NEED TO PASS THE ACTUAL VALS TO COMPARE AGAINST SMH <:>
    attributes = {'key': False, 'speed': True, 'style': False, 'song_type': False, 'timeSig': False}
    from json import load
    with open("wordSongsIndex.json", 'r', encoding='utf-8') as f:
        wordSongs = load(f)["SongNum"]
    returnSongs = []
    songnum = 1
    book = "New" # not needed 
    songattrs = {
    "Comments": "Dance-P5-5",
    "Title": "Եղբայրնե՛ր, ցնծացե՛ք",
    "Worship_Song": "",
    "key": "Em",
    "latestVersion": "Երգարան Word Files/1 Եղբայրնե՛ր, ցնծացե՛ք.docx",
    "opening_Song": "",
    "song_type": "Opening Song",
    "speed": "105",
    "style": "Disco",
    "timeSig": "4/4",
    "v1": "Երգարան Word Files/1 Եղբայրնե՛ր, ցնծացե՛ք.docx"
    }
    true_ct = 0
    for x in attributes:
        if attributes[x]:
            true_ct += 1
    from json import load
    with open("wordSongsIndex.json", 'r', encoding='utf-8') as f:
        wordSongs = load(f)["SongNum"]
    returnSongs = {}
    returnSongs["WordSongsIndex"] = {}
    returnSongs["REDergaran"] = {}
    for songNum in wordSongs:
        song = wordSongs[songNum]
        for attribute in attributes: #TODO: Figure out how to make it filter for attr 1 U attr 2 U etc. Use "culling" where you just keep on filtering the attributes finer and finer
            if attributes[attribute]:
                if attribute in song and song[attribute].lower() == songattrs[attribute].lower():
                    print(f'{song[attribute]} == {songattrs[attribute]}', songNum)
                    # returnSongs["WordSongsIndex"] = songNum
                    returnSongs["WordSongsIndex"][songNum] = song
                    returnSongs["REDergaran"][songNum]["book"] = "WordSongsIndex"
                    break
    with open("REDergaran.json", 'r', encoding='utf-8') as f:
        REDergaran = load(f)["SongNum"]
    for songNum in REDergaran:
        song = REDergaran[songNum]
        for attribute in attributes:
            if attributes[attribute]:
                if attribute in song and song[attribute].lower() == songattrs[attribute].lower():
                    print(f'{song[attribute]} == {songattrs[attribute]}', songNum)
                    # returnSongs["REDergaran"] = songNum
                    returnSongs["REDergaran"][songNum] = song
                    returnSongs["REDergaran"][songNum]["book"] = "REDergaran"
                    break
    return returnSongs



# print(attributeSearch())
attributes = {'key': False, 'speed': True, 'style': False, 'song_type': False, 'timeSig': True}
true_ct = 0
for x in attributes:
    if attributes[x]:
       true_ct += 1 
       
print(true_ct)