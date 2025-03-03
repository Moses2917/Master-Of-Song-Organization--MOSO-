import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from concurrent.futures import ThreadPoolExecutor

class SearchEngine:
    def __init__(self):
        self.song_lyrics = self.load_json_data('AllLyrics.json')
        self.all_lyrics, self.song_ids = self.extract_lyrics(self.song_lyrics)
        self.vectorizer, self.tfidf_matrix = self.create_tfidf_matrix(self.all_lyrics)

    def load_json_data(self, file_path) -> dict:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def is_valid(self, book:str, songnum:str) -> bool:
        """
        Retrieves a song from a JSON file based on the provided book and song number. The options are 'old', 'new', 'redergaran', and 'wordsongsindex'.

        Args:
            book (str): The book from which to retrieve the song.
            songnum (str): The number of the song to retrieve.
            batch (int, optional): The batch number. Defaults to 0.

        Returns:
            bool: True if exists or False if not.
        """
        
        from json import load
        if book.lower() == "old" or book.lower() == "wordsongsindex":
            with open("wordSongsIndex.json", 'r', encoding='utf-8') as f:
                wordSongs:dict = load(f)["SongNum"]
                return True if wordSongs.get(songnum, False) else False
        else:
            with open("REDergaran.json", 'r', encoding='utf-8') as f:
                REDergaran:dict = load(f)["SongNum"]
                return True if REDergaran.get(songnum, False) else False

    def extract_lyrics(self, song_lyrics:dict):
        all_lyrics = []
        song_ids = []

        for section in ['old', 'new']:
            for song_id, lyrics in song_lyrics[section].items():
                lyrics = lyrics.lower()
                lyrics = re.sub(r'[՝՜]+', ' ', lyrics, re.MULTILINE)
                lyrics = re.sub(r'[:։,.(0-9)\\n\s]+', ' ', lyrics, re.MULTILINE)
                all_lyrics.append(lyrics+song_id)
                song_ids.append((section, song_id))

        return all_lyrics, song_ids

    def create_tfidf_matrix(self, lyrics):
        vectorizer = TfidfVectorizer(lowercase=True)#, stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(lyrics)
        return vectorizer, tfidf_matrix

    def search_lyrics(self, query, vectorizer, tfidf_matrix, song_ids, all_lyrics, top_k=10):
        results = []
        clean_query = re.sub(r'[՛:։,.\\n\s]+',' ',query,re.MULTILINE)
        if clean_query.isdigit():
            if self.is_valid('old', clean_query):
                results.append(('old', clean_query, 1.0))
            if self.is_valid('new', clean_query):
                results.append(('new', clean_query, 1.0))
            return results
        clean_query=clean_query.lower()
        clean_query = re.sub(r'[՝՜]+',' ',query,re.MULTILINE)
        clean_query = re.sub(r'[՛:։,.(0-9)\\n\s]+',' ',query,re.MULTILINE)
        # First, check for exact phrase match
        for idx, lyric in enumerate(all_lyrics):
            if len(results) < top_k:
                if re.search(clean_query, lyric):
                    section, song_id = song_ids[idx]
                    results.append((section, song_id, 1.0))  # Assign highest similarity score for exact match
        
        # If we haven't reached top_k results, proceed with cosine similarity (TF-IDF)
        if len(results) < top_k:
            query_vec = vectorizer.transform([clean_query])
            cosine_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
            top_indices = cosine_similarities.argsort()[::-1]  # Get all indices sorted by similarity
            
            for idx in top_indices:
                section, song_id = song_ids[idx]
                # Skip if this song_id is already in results (from exact match)
                if any(song_id == r[1] for r in results):
                    continue
                    
                # Add new match if not already present
                results.append((section, song_id, cosine_similarities[idx]))
                if len(results) == top_k:
                    break
        
        return results
    
    def search(self, query):
        return self.search_lyrics(query, self.vectorizer, self.tfidf_matrix, self.song_ids, self.all_lyrics)

class SimilerSongMatcher(SearchEngine):
    def __init__(self):
        super().__init__()
        self.open_indexes()

    def find_match(self, lyrics, song_num, book, match_count=1) -> list:
        try:
            if song_num == "114" and book == "new":
                print()
            results = self.search(lyrics)[:2] # gets two first matches
            if results[1][2] > 0.45: # check probability
                if results[1][0] != book: #and results[1][1] != songnum: # If they are of the same book and num, NO return
                    # print(results[1])
                    return [results[1]]
                elif results[1][1] != song_num:
                    # print(results[1])
                    return [results[1]]
                else:
                    # print(results[0])
                    return [results[0]]
        except:
            return [None]

    def open_indexes(self):
        try:
            with open('REDergaran.json', mode='r', encoding='utf-8') as json_file:
                self.REDergaran:dict = json.load(json_file)
            with open('wordSongsIndex.json', mode='r', encoding='utf-8') as json_file:
                self.wordSongsIndex:dict = json.load(json_file)
        except Exception as e:
            raise e

    def comapre(self, song_num:str, book:str):
        try:
            match = self.find_match(self.song_lyrics[book][song_num], song_num, book)
            if book.lower() == 'old' or book.lower() == 'wordsongsindex':
                self.wordSongsIndex["SongNum"][song_num]["match"] = match
            else:
                self.REDergaran["SongNum"][song_num]["match"] = match
        except Exception as e:
            pass
    
    def load_data_and_run(self, book:str, index:dict):
        for song_num in index["SongNum"]:
            self.comapre(song_num, book)

    def save_files(self, book:str):
        try:
            if book == 'new':
                with open('REDergaran.json', mode='w', encoding='utf-8') as json_file:
                    json.dump(self.REDergaran, json_file, ensure_ascii=False, indent=4)
            elif book == 'old':
                with open('wordSongsIndex.json', mode='w', encoding='utf-8') as json_file:
                    json.dump(self.wordSongsIndex, json_file, ensure_ascii=False, indent=4)
                
        except Exception as e:
            raise e

    def start(self):
        with ThreadPoolExecutor() as futures:
            futures.submit(self.load_data_and_run,'old', self.wordSongsIndex)
            futures.submit(self.load_data_and_run,'new', self.REDergaran)
        # self.load_data_and_run('new', self.REDergaran)
        self.save_files('new')
        self.save_files('old')

def combine():
    with open('REDergaran.json', mode='r', encoding='utf-8') as json_file:
        REDergaran:dict = json.load(json_file)
    with open('wordSongsIndex.json', mode='r', encoding='utf-8') as json_file:
        wordSongsIndex:dict = json.load(json_file)
    matched_songs = {}
    for song_num in wordSongsIndex["SongNum"]:
        try:
            match = list(wordSongsIndex["SongNum"][song_num]["match"])
            matched_book = match[0][0]
            matched_num = match[0][1]
            if matched_book == 'old':
                matched_songs
                ...
            elif matched_book == 'new':
                ...
            # print(match)
        except:
            pass
        # REDergaran["SongNum"][song_num]["match"] = wordSongsIndex["SongNum"][song_num]["match"]
    
    # with open('matched_songs.json', mode='w', encoding='utf-8') as json_file:
        # json.dump(REDergaran, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    lyr = "429 Տիրոջը նոր երգ երգենք Երգենք և օրհնենք Սաղմոսներով ցնծումով շեփորի ձայնով: Թող որ գոռան ծովերը լիությամբ անբավ: Գետերը թող ծափ տան ձեռքով Քանզի Տերն եկավ: (2)\nԻնչ անուն աշխարհ եկավ, Մեծ խաղաղության իշխան, Կարեկից ողջ մարդկության, Հիսուս: (2)"
    search_engine = SearchEngine()
    print(search_engine.search(lyr))
    # Similer_Song_Matcher = SimilerSongMatcher()
    # Similer_Song_Matcher.start()
    # combine()