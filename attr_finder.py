from json import load
from re import sub

class attrFinder:
    def __init__(self, attributes:dict, songattrs:dict):
        self.attributes = attributes
        self.songattrs = songattrs

    def attributeSearch(self) -> dict:
        """This inputs a list of attributes and finds songs whose attributes match the input attributes.
        
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
        # Define the attributes that need to be matched
        attributes = self.attributes#{'key': True, 'speed': True, 'style': False, 'song_type': False, 'timeSig': True}
        
        # Define the example song attributes to match against
        # songattrs = {
        #     "key": "Em",
        #     "speed": "105",
        #     "style": "Disco",
        #     "song_type": "Opening Song",
        #     "timeSig": "4/4"
        # }
              
        songattrs = self.songattrs
        temp = {}
        for attribute in songattrs:
            if attributes.get(attribute):#Check if the attribute is in the dictionary
                if attributes[attribute]:
                    temp[attribute] = songattrs[attribute]
        songattrs = temp
        print(songattrs)
        # Load songs from JSON files
        with open("wordSongsIndex.json", 'r', encoding='utf-8') as f:
            wordSongs = load(f)["SongNum"]
            
        with open("REDergaran.json", 'r', encoding='utf-8') as f:
            REDergaran = load(f)["SongNum"]
        
        returnSongs = {
            "WordSongsIndex": {},
            "REDergaran": {}
        }
        
        # Filter songs based on attributes
        def filter_songs(songs):        

            for songNum, song in songs.items():
                matched =True
                for attr in songattrs:
                    foundSongAttr = song.get(attr)
                    if foundSongAttr != songattrs[attr]: matched = False
                
                if matched:
                    returnSongs[songNum] = song
            
            return returnSongs
            
        

        
        # Filter songs from both sources
        returnSongs["WordSongsIndex"] =filter_songs(wordSongs)
        returnSongs["REDergaran"]=filter_songs(REDergaran)
        
        #print(returnSongs)
        
        return returnSongs
    


