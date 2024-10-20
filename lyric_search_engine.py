import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def extract_lyrics(song_lyrics):
    all_lyrics = []
    song_ids = []

    for section in ['old', 'new']:
        for song_id, lyrics in song_lyrics[section].items():
            lyrics = re.sub(r'[՛:։,.(0-9)]+','',lyrics)
            all_lyrics.append(lyrics)
            song_ids.append((section, song_id))

    return all_lyrics, song_ids

def create_tfidf_matrix(lyrics):
    vectorizer = TfidfVectorizer(lowercase=True)#, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(lyrics)
    return vectorizer, tfidf_matrix

def search_lyrics(query, vectorizer, tfidf_matrix, song_ids, all_lyrics, top_k=10):
    results = []
    # First, check for exact phrase match
    # exact_matches = []
    for idx, lyric in enumerate(all_lyrics):
        if re.search(query, lyric):
            section, song_id = song_ids[idx]
            results.append((section, song_id, 1.0))  # Assign highest similarity score for exact match
    
    
    # If no exact match, proceed with cosine similarity (TF-IDF)
    query_vec = vectorizer.transform([query])
    cosine_similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    top_indices = cosine_similarities.argsort()[-top_k:][::-1]

    ct = 1 #because of the exact match
    
    for idx in top_indices:
        if ct == top_k - 1:
            break
        section, song_id = song_ids[idx]
        results.append((section, song_id, cosine_similarities[idx]))
        ct += 1
    if len(results) > top_k:
        return results[:top_k]
    return results

# def load_into_mem():
#     file_path = 'AllLyrics.json'
#     song_lyrics = load_json_data(file_path)
    
#     all_lyrics, song_ids = extract_lyrics(song_lyrics)
#     vectorizer, tfidf_matrix = create_tfidf_matrix(all_lyrics)

def main(query):
    file_path = 'AllLyrics.json'
    song_lyrics = load_json_data(file_path)
    
    all_lyrics, song_ids = extract_lyrics(song_lyrics)
    vectorizer, tfidf_matrix = create_tfidf_matrix(all_lyrics)
    # while True:
        # query = input("Enter your search query (or 'quit' to exit): ")
        # if query.lower() == 'quit':
        #     break
    
    results = search_lyrics(query, vectorizer, tfidf_matrix, song_ids, all_lyrics)
    return results    
    # for section, song_id, similarity in results:
    #     print(f"Section: {section}")
    #     print(f"Song ID: {song_id}")
    #     print(f"Similarity: {similarity:.4f}")
    #     lyrics = song_lyrics[section][song_id]
    #     print(f"Lyrics excerpt: {lyrics[:100]}...")
    #     print("---")

if __name__ == "__main__":
    print(main("աս"))