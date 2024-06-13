import json

def check_simil():
    """ basicly count and store in a dict all of the the songs that song number N has been with. Then sort by which has the most hits

    Args:
        songnum (str): a str object that represents a song number
        book (str): 'Old' or 'New'
        occr (dict): amt of occurrences, structure: occr = {'Old':{},'New':{}}
    """

    # foundBook = 'New'
    # occr[book][songnum] = {
    # occr = {
    #     'Old':{
    #         '312':{
    #             ('12','Old'):{
    #                 'occr': 123
    #             },
    #             ('13','New'):{
    #                 'occr': 1
    #             }
    #         }
    #     }
    # }

    occr = {
        'Old':{},
        'New':{}
    }

    with open('songs_cleaned.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open('wordSongsIndex.json', 'r', encoding='utf-8') as f:
        wordSongsIndex = json.load(f)

    with open('REDergaran.json', 'r', encoding='utf-8') as f:
        REDergaran = json.load(f)

    for songnum in wordSongsIndex['SongNum']:
        occr['Old'][songnum] = {}
    for songnum in REDergaran['SongNum']:
        occr['New'][songnum] = {}
    # print(occr)


    # print(data)

    # occr[book][songnum] = {}
    for book in occr:
        for songnum in occr[book]:
            for item in data:
                songList = eval(data[item]['songList'])
                pair = (book, songnum) #song to lookup
                if pair in songList:
                    for song in songList:
                        if not (pair == song):
                            #maybe stor in ('New','279','3')
                            if str(song) in occr[book][songnum]:
                                occr[book][songnum][str(song)]['occur'] += 1
                            else:
                                occr[book][songnum][str(song)] = {
                                    'occur': 1
                                }
    print(occr)

    with open('song_occurrences.json', 'w', encoding='utf-8') as f:
        json.dump(occr,f,ensure_ascii=False,indent=4)





with open('song_occurrences.json', 'r',encoding='utf-8') as f:
    occr = json.load(f)


for book in occr:
    for songnum in occr[book]:
        # for song in occr[book][songnum]:
        print(occr[book][songnum])
        print(sorted(occr[book][songnum]))
        break