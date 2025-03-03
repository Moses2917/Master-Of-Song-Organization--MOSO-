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
        Retrieves a song from a JSON file based on the provided book and song number.
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
                # Store case-folded version for better matching
                processed_lyrics = self.preprocess_text(lyrics)
                all_lyrics.append(processed_lyrics)
                song_ids.append((section, song_id))

        return all_lyrics, song_ids
    
    def preprocess_text(self, text):
        """Standardize text for better matching"""
        # Convert to lowercase
        text = text.lower()
        # Remove specific Armenian punctuation
        text = re.sub(r'[՝՜]+', ' ', text, re.MULTILINE)
        # Remove other punctuation, digits, and normalize whitespace
        text = re.sub(r'[:։,.(0-9)\\n\s]+', ' ', text, re.MULTILINE)
        return text.strip()

    def create_tfidf_matrix(self, lyrics):
        # Use advanced TF-IDF vectorization with character n-grams for Armenian
        vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 3),  # Use word n-grams
            analyzer='word',
            min_df=2,            # Ignore very rare terms
            max_df=0.9           # Ignore very common terms
        )
        tfidf_matrix = vectorizer.fit_transform(lyrics)
        return vectorizer, tfidf_matrix
    
    def clean_query(self, query):
        """Clean and standardize query text"""
        # Handle numeric queries separately
        clean_query = re.sub(r'[՛:։,.\\n\s]+', ' ', query, re.MULTILINE)
        if clean_query.strip().isdigit():
            return clean_query.strip()
        
        # Apply same preprocessing as for stored lyrics
        return self.preprocess_text(query)

    def search_lyrics(self, query, top_k=10):
        results = []
        clean_query = self.clean_query(query)
        
        # If query is just a number, treat as song ID lookup
        if clean_query.isdigit():
            if self.is_valid('old', clean_query):
                results.append(('old', clean_query, 1.0))
            if self.is_valid('new', clean_query):
                results.append(('new', clean_query, 1.0))
            return results
        
        # For text search, use TF-IDF to get all possible matches
        query_vec = self.vectorizer.transform([clean_query])
        cosine_similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        # Create a list of (section, song_id, similarity) tuples for all songs
        all_matches = []
        for idx, similarity in enumerate(cosine_similarities):
            section, song_id = self.song_ids[idx]
            all_matches.append((section, song_id, float(similarity)))
        
        # Sort by similarity score in descending order
        all_matches.sort(key=lambda x: x[2], reverse=True)
        
        # Return top k results
        return all_matches[:top_k]
    
    def search(self, query, top_k=10):
        """Search for songs matching the query and return top k results"""
        return self.search_lyrics(query, top_k=top_k)
    
    def get_lyrics_by_id(self, section, song_id):
        """Retrieve original lyrics for a given song ID"""
        if section in self.song_lyrics and song_id in self.song_lyrics[section]:
            return self.song_lyrics[section][song_id]
        return None
    
    def search_and_display(self, query, top_k=10):
        """Search and display results with similarity scores"""
        results = self.search(query, top_k=top_k)
        
        print(f"Top {len(results)} results for: {query}")
        print("-" * 40)
        
        for i, (section, song_id, similarity) in enumerate(results):
            print(f"{i+1}. Section: {section}, Song ID: {song_id}")
            print(f"   Similarity: {similarity:.4f}")
            
            # Get a snippet of the lyrics
            lyrics = self.get_lyrics_by_id(section, song_id)
            if lyrics:
                snippet = lyrics[:100] + "..." if len(lyrics) > 100 else lyrics
                print(f"   Snippet: {snippet}")
            
            print()
        
        return results

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
    # lyr = "429 Տիրոջը նոր երգ երգենք Երգենք և օրհնենք Սաղմոսներով ցնծումով շեփորի ձայնով: Թող որ գոռան ծովերը լիությամբ անբավ: Գետերը թող ծափ տան ձեռքով Քանզի Տերն եկավ: (2)\nԻնչ անուն աշխարհ եկավ, Մեծ խաղաղության իշխան, Կարեկից ողջ մարդկության, Հիսուս: (2)"
    # search_engine = SearchEngine()
    # print(search_engine.search(lyr))
    Similer_Song_Matcher = SimilerSongMatcher()
    Similer_Song_Matcher.start()
    # combine()