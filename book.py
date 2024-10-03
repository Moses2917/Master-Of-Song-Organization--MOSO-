class Song:
    def __init__(self, book, songnum) -> None:
        self.book = book
        self.songnum = songnum

    def getAttrs(self,index:dict):
        self.title = index[self.songnum]['Title']
        self.key = index[self.songnum].get("key", None)
    
    def getSongAttrs(self):
        from json import load
        if self.book.lower() == "old" or self.book.lower() == "wordsongsindex":
            with open("wordSongsIndex.json", 'r', encoding='utf-8') as f:
                index:dict = load(f)["SongNum"]
                return index[self.songnum]
        else:
            with open("REDergaran.json", 'r', encoding='utf-8') as f:
                index = load(f)["SongNum"]
                return index[self.songnum]
    
# mySong = print(Song('Old','312').songnum)