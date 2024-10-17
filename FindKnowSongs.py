# import concurrent.futures
# with concurrent.futures.ThreadPoolExecutor() as exec:
#     future = exec.submit(openWord,songnum,book)
#     lyrics = future.result()

def getSong(book:str, songnum:str, batch = 0) -> dict:
    """
    Retrieves a song from a JSON file based on the provided book and song number. The options are 'old', 'new', 'redergaran', and 'wordsongsindex'.

    Args:
        book (str): The book from which to retrieve the song.
        songnum (str): The number of the song to retrieve.
        batch (int, optional): The batch number. Defaults to 0.

    Returns:
        dict: A dictionary containing the song data.
    """
    if batch == 0:
        from json import load
        if book.lower() == "old" or book.lower() == "wordsongsindex":
            with open("wordSongsIndex.json", 'r', encoding='utf-8') as f:
                wordSongs = load(f)["SongNum"]
                return wordSongs[songnum]
        else:
            with open("REDergaran.json", 'r', encoding='utf-8') as f:
                REDergaran = load(f)["SongNum"]
                return REDergaran[songnum]
    else:
        pass

with open('songs_cleaned.json', 'r', encoding='utf-8') as f:
    from json import load
    allSongs: dict = load(f)

full_songList = []
for date in allSongs:
    songlist = eval(allSongs[date]["songList"])