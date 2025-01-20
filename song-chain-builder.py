# Shopuld be able to choose songs and order them absed soley off of musical similarity
# import musical_compatibility.MusicalCompatibility as MusicalCompatibility
from json import load
from musical_compatibility import MusicalCompatibility
class SongChainBuilder:
    def __init__(self, compatibility_threshold: float = 0.75):
        """
        Initialize the chain builder with a compatibility threshold.
        
        Args:
            compatibility_threshold: Minimum compatibility score to consider songs matchable
                                   (default 0.75 or 75% compatible)
        """
        self.compatibility_calculator = MusicalCompatibility()
        self.threshold = compatibility_threshold
    
    def is_compatible(self, current_song: dict, candidate_song: dict) -> tuple[bool, float, dict]:
        """
        Check if two songs are compatible enough to be played sequentially.
        
        Args:
            current_song: Current song in the chain
            candidate_song: Potential next song
            
        Returns:
            tuple: (is_compatible, compatibility_score, detailed_results)
        """
        results = self.compatibility_calculator.get_transition_recommendation(
            current_song, candidate_song
        )
        
        is_compatible = results['overall_compatibility'] >= self.threshold
        return is_compatible, results['overall_compatibility'], results
    
    def build_song_chain(self, 
                        start_song: dict, 
                        candidate_pool: list[dict], 
                        chain_length: int = 6,
                        max_attempts: int = 1000) -> tuple[list[dict], list[float]]:
        """
        Build a chain of compatible songs starting from a given song.
        
        Args:
            start_song: First song in the chain
            candidate_pool: List of songs to choose from
            chain_length: Desired length of the song chain
            max_attempts: Maximum attempts to find compatible songs before giving up
            
        Returns:
            tuple: (list of songs in chain, list of transition scores)
        """
        import random
        
        # Initialize chain with start song
        song_chain = [start_song]
        transition_scores = []
        attempts = 0
        
        while len(song_chain) < chain_length and attempts < max_attempts:
            current_song = song_chain[-1]
            
            # Randomly select a candidate from remaining songs
            remaining_songs = [song for song in candidate_pool 
                             if song not in song_chain]
            
            if not remaining_songs:
                break
                
            candidate = random.choice(remaining_songs)
            is_compatible, score, details = self.is_compatible(current_song, candidate)
            
            if is_compatible:
                song_chain.append(candidate)
                transition_scores.append(score)
                attempts = 0  # Reset attempts when we find a match
            else:
                attempts += 1
        
        if len(song_chain) < chain_length:
            raise ValueError(
                f"Could not build chain of length {chain_length}. "
                f"Only found {len(song_chain)} compatible songs."
            )
            
        return song_chain, transition_scores
    
    def print_chain_analysis(self, song_chain: list[dict], transition_scores: list[float]):
        """Print detailed analysis of the song chain"""
        print("\nSong Chain Analysis:")
        print("-" * 50)
        
        for i, song in enumerate(song_chain):
            print(f"\nSong {i + 1}:")
            print(f"Key: {song['key']}")
            print(f"Tempo: {song['tempo']} BPM")
            print(f"Time Signature: {song['time_signature']}")
            
            if i < len(song_chain) - 1:
                next_song = song_chain[i + 1]
                print(f"\nTransition to next song (compatibility: {transition_scores[i]:.2f}):")
                
                # Get detailed transition info
                _, _, details = self.is_compatible(song, next_song)
                print(f"Key compatibility: {details['key_compatibility']:.2f}")
                print(f"Tempo compatibility: {details['tempo_compatibility']:.2f}")
                print(f"Meter compatibility: {details['meter_compatibility']:.2f}")
                
                if details['transition_tips']:
                    print("\nTransition tips:")
                    for tip in details['transition_tips']:
                        print(f"- {tip}")
                print("-" * 50)

class SequenceAnalyzer:
    def __init__(self):
        self.compatibility_calculator = MusicalCompatibility()
    
    def analyze_sequence(self, songs: list[dict]) -> dict:
        """
        Analyze compatibility between each adjacent pair in a sequence of songs.
        
        Args:
            songs: List of dictionaries, each containing 'key', 'tempo', and 'time_signature'
            
        Returns:
            Dictionary containing overall and pair-wise analysis
        """
        if len(songs) < 2:
            return {"error": "Need at least 2 songs to analyze sequence"}
            
        analysis = {
            "pair_transitions": [],
            "overall_score": 0.0,
            "problem_transitions": []
        }
        
        # Analyze each adjacent pair
        total_score = 0
        for i in range(len(songs) - 1):
            current_song = songs[i]
            next_song = songs[i + 1]
            
            # Get detailed compatibility analysis
            results = self.compatibility_calculator.get_transition_recommendation(
                current_song, next_song
            )
            
            transition_info = {
                "position": f"Songs {i+1} → {i+2}",
                "keys": f"{current_song['key']} → {next_song['key']}",
                "tempos": f"{current_song['tempo']} → {next_song['tempo']} BPM",
                "time_signatures": f"{current_song['time_signature']} → {next_song['time_signature']}",
                "compatibility_scores": {
                    "overall": results['overall_compatibility'],
                    "key": results['key_compatibility'],
                    "tempo": results['tempo_compatibility'],
                    "meter": results['meter_compatibility']
                },
                "transition_tips": results['transition_tips']
            }
            
            analysis["pair_transitions"].append(transition_info)
            total_score += results['overall_compatibility']
            
            # Flag problematic transitions (below 70% compatibility)
            if results['overall_compatibility'] < 0.7:
                analysis["problem_transitions"].append({
                    "position": f"Songs {i+1} → {i+2}",
                    "score": results['overall_compatibility'],
                    "issues": results['transition_tips']
                })
        
        # Calculate overall sequence compatibility
        analysis["overall_score"] = total_score / (len(songs) - 1)
        analysis["is_sequence_recommended"] = analysis["overall_score"] >= 0.75
        
        return analysis

from itertools import combinations, permutations
import time
import random
from multiprocessing import Pool, cpu_count
from functools import partial
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

class OptimalSubsetFinder:
    def __init__(self):
        self.compatibility_calculator = MusicalCompatibility()
        # Queue to store results from permutation calculations
        self.result_queue = Queue()
        
    def calculate_sequence_score(self, sequence: list[dict]) -> float:
        """Calculate overall compatibility score for a sequence"""
        total_score = 0
        for i in range(len(sequence) - 1):
            results = self.compatibility_calculator.get_transition_recommendation(
                sequence[i], sequence[i + 1]
            )
            total_score += results['overall_compatibility']
        return total_score / (len(sequence) - 1)
    
    def _process_permutations(self, subset: tuple) -> None:
        """Process all permutations of a subset in a separate thread.
        
        This method runs in its own thread and pushes results to the queue
        for the main thread to process."""
        best_score = 0
        best_sequence = None
        
        # Calculate scores for all permutations of this subset
        for sequence in permutations(subset):
            sequence = list(sequence)
            score = self.calculate_sequence_score(sequence)
            
            if score > best_score:
                best_score = score
                best_sequence = sequence
        
        # Put the result in the queue for the main thread to process
        self.result_queue.put((best_sequence, best_score))
    
    def find_optimal_subset(self, 
                          songs: list[dict], 
                          subset_size: int = 6,
                          max_combinations: int = 100,
                          time_limit: int = 60,
                          n_processes: int = None) -> tuple[list[dict], float, dict]:
        """Find the optimal subset and sequence of songs using threaded processing for permutations."""
        # Validate inputs
        if not all('song_num' in song for song in songs):
            raise ValueError("All songs must have a 'song_num' key")
            
        if len(songs) < subset_size:
            raise ValueError(f"Need at least {subset_size} songs (got {len(songs)})")
        
        start_time = time.time()
        
        # Generate combinations and sample if needed
        all_combinations = list(combinations(songs, subset_size))
        total_possible = len(all_combinations)
        
        if total_possible > max_combinations:
            print(f"Large song pool detected. Sampling {max_combinations} combinations out of {total_possible} possible.")
            all_combinations = random.sample(all_combinations, max_combinations)
        
        # Create a thread pool for processing combinations
        # We'll use a smaller number of threads since each thread handles multiple permutations
        n_threads = min(32, len(all_combinations))  # Cap at 32 threads to prevent overhead
        print(f"Processing combinations using {n_threads} threads...")
        
        best_sequence = None
        best_score = 0
        combinations_checked = 0
        active_threads = []
        
        try:
            with ThreadPoolExecutor(max_workers=n_threads) as executor:
                # Submit all combinations for processing
                future_to_combination = {
                    executor.submit(self._process_permutations, combination): combination 
                    for combination in all_combinations
                }
                
                # Process results as they come in
                while combinations_checked < len(all_combinations):
                    # Get result from queue (blocks until a result is available)
                    sequence, score = self.result_queue.get()
                    combinations_checked += 1
                    
                    if score > best_score:
                        best_score = score
                        best_sequence = sequence
                    
                    if combinations_checked % 100 == 0:
                        elapsed = time.time() - start_time
                        print(f"Checked {combinations_checked}/{len(all_combinations)} combinations. "
                              f"Best score: {best_score:.3f}")
                    
                    if time.time() - start_time > time_limit:
                        print(f"Time limit reached after checking {combinations_checked} combinations.")
                        break
                    
                    # Mark this task as done in the queue
                    self.result_queue.task_done()
                        
        except KeyboardInterrupt:
            print("\nSearch interrupted by user.")
            # Clear the queue and stop processing
            while not self.result_queue.empty():
                self.result_queue.get()
                self.result_queue.task_done()
        
        if best_sequence is None:
            raise ValueError("Could not find a valid sequence")
        
        return best_sequence, best_score, self._analyze_sequence(best_sequence)
    
    def _analyze_sequence(self, sequence: list[dict]) -> dict:
        """Generate detailed analysis of a sequence"""
        analysis = {
            "transitions": [],
            "overall_score": self.calculate_sequence_score(sequence),
            "problem_spots": [],
            "song_numbers": [song['song_num'] for song in sequence]
        }
        
        for i in range(len(sequence) - 1):
            current = sequence[i]
            next_song = sequence[i + 1]
            results = self.compatibility_calculator.get_transition_recommendation(
                current, next_song
            )
            
            transition = {
                "position": f"Songs {i+1} → {i+2}",
                "song_numbers": f"#{current['song_num']} → #{next_song['song_num']}",
                "transition": f"{current['key']} ({current['tempo']} BPM) → {next_song['key']} ({next_song['tempo']} BPM)",
                "scores": {
                    "overall": results['overall_compatibility'],
                    "key": results['key_compatibility'],
                    "tempo": results['tempo_compatibility'],
                    "meter": results['meter_compatibility']
                },
                "tips": results['transition_tips']
            }
            
            analysis["transitions"].append(transition)
            
            if results['overall_compatibility'] < 0.7:
                analysis["problem_spots"].append(transition)
        
        return analysis
    
    def print_detailed_analysis(self, sequence: list[dict], score: float, analysis: dict):
        """Print detailed analysis of the optimal sequence"""
        print("\nOptimal Song Sequence Found")
        print("=" * 60)
        print(f"Overall Sequence Score: {score:.3f}")
        
        print("\nOptimal Song Order (by song number):")
        print(f"→ ".join(f"#{song['song_num']}" for song in sequence))
        
        print("\nDetailed Song Order:")
        for i, song in enumerate(sequence, 1):
            print(f"\n{i}. Song #{song['song_num']}")
            print(f"   Key: {song['key']}")
            print(f"   Tempo: {song['tempo']} BPM")
            print(f"   Time Signature: {song['time_signature']}")
        
        print("\nTransition Analysis:")
        print("-" * 60)
        for transition in analysis["transitions"]:
            print(f"\n{transition['position']} ({transition['song_numbers']})")
            print(f"Transition: {transition['transition']}")
            scores = transition["scores"]
            print(f"Compatibility Scores:")
            print(f"  Overall: {scores['overall']:.2f}")
            print(f"  Key: {scores['key']:.2f}")
            print(f"  Tempo: {scores['tempo']:.2f}")
            print(f"  Meter: {scores['meter']:.2f}")
            
            if transition["tips"]:
                print("Transition Tips:")
                for tip in transition["tips"]:
                    print(f"  - {tip}")
        
        if analysis["problem_spots"]:
            print("\nAreas Needing Attention:")
            print("-" * 60)
            for problem in analysis["problem_spots"]:
                print(f"\n{problem['position']}: {problem['song_numbers']}")
                print(f"Transition: {problem['transition']}")
                print("Suggested improvements:")
                for tip in problem["tips"]:
                    print(f"  - {tip}")
# Example usage
if __name__ == "__main__":
    # Example larger song pool
    # songs = [
    #     {'key': 'G', 'tempo': 120, 'time_signature': '4/4'},
    #     {'key': 'D', 'tempo': 116, 'time_signature': '4/4'},
    #     {'key': 'Em', 'tempo': 122, 'time_signature': '3/4'},
    #     {'key': 'C', 'tempo': 126, 'time_signature': '4/4'},
    #     # ... more songs ...
    # ]
    songs = []
    with open("REDergaran.json", 'r', encoding='utf-8') as f:
        ergaran:dict = load(f)
        for song in ergaran["SongNum"]:
            try:
                songs.append({
                    'song_num': int(song),
                    'key': ergaran["SongNum"][song]["key"],
                    'tempo': int(ergaran["SongNum"][song]["speed"]),
                    'time_signature': ergaran["SongNum"][song]["timeSig"]
                    })
            except:
                pass

            
    finder = OptimalSubsetFinder()
    
    try:
        # Find optimal subset and sequence
        optimal_sequence, score, analysis = finder.find_optimal_subset(
            songs=songs,
            subset_size=6,  # How many songs you want in the final sequence
            max_combinations=100,  # Limit combinations for large song pools
            time_limit=60,  # Maximum seconds to search
            n_processes=None  # Will use all available CPU cores
        )
        
        # Print the detailed analysis
        finder.print_detailed_analysis(optimal_sequence, score, analysis)
        
    except ValueError as e:
        print(f"Error: {e}")
# if __name__ == "__main__":
#     # Example song pool
#     song_pool = [
#         {'key': 'G', 'tempo': 120, 'time_signature': '4/4'},
#         {'key': 'D', 'tempo': 116, 'time_signature': '4/4'},
#         {'key': 'C', 'tempo': 122, 'time_signature': '4/4'},
#         {'key': 'Em', 'tempo': 118, 'time_signature': '3/4'},
#         {'key': 'A', 'tempo': 124, 'time_signature': '4/4'},
#         {'key': 'F', 'tempo': 115, 'time_signature': '6/8'},
#         {'key': 'G', 'tempo': 130, 'time_signature': '4/4'},
#         {'key': 'Dm', 'tempo': 110, 'time_signature': '4/4'},
#         {'key': 'E', 'tempo': 126, 'time_signature': '4/4'},
#         {'key': 'Am', 'tempo': 112, 'time_signature': '3/4'},
#     ]
#     # with open("REDergaran.json", 'r', encoding='utf-8') as f:
#     #     song_pool = load(f)
#     #     song_pool = song_pool["SongNum"].tolist()
#     # Initialize chain builder
#     chain_builder = SongChainBuilder(compatibility_threshold=0.75)
    
#     # Build a chain starting with the first song
#     try:
#         chain, scores = chain_builder.build_song_chain(
#             start_song=song_pool[0],
#             candidate_pool=song_pool,
#             chain_length=6
#         )
        
#         # Print the analysis
#         chain_builder.print_chain_analysis(chain, scores)
        
#     except ValueError as e:
#         print(f"Error: {e}")
# if __name__ == "__main__":
#     # Example sequence of songs
#     song_sequence = [
#         {'key': 'G', 'tempo': 120, 'time_signature': '4/4'},
#         {'key': 'D', 'tempo': 116, 'time_signature': '4/4'},
#         {'key': 'Em', 'tempo': 122, 'time_signature': '3/4'},
#         {'key': 'C', 'tempo': 126, 'time_signature': '4/4'},
#         {'key': 'Am', 'tempo': 118, 'time_signature': '4/4'},
#         {'key': 'D', 'tempo': 114, 'time_signature': '6/8'}
#     ]
    
#     analyzer = SequenceAnalyzer()
#     analysis = analyzer.analyze_sequence(song_sequence)
    
#     # Print results
#     print("\nSequence Analysis Results")
#     print("=" * 50)
#     print(f"Overall Sequence Compatibility: {analysis['overall_score']:.2f}")
#     print(f"Recommended Sequence: {analysis['is_sequence_recommended']}")
    
#     print("\nDetailed Transition Analysis:")
#     print("-" * 50)
#     for transition in analysis["pair_transitions"]:
#         print(f"\n{transition['position']}:")
#         print(f"Keys: {transition['keys']}")
#         print(f"Tempos: {transition['tempos']}")
#         print(f"Time Signatures: {transition['time_signatures']}")
#         print("\nCompatibility Scores:")
#         scores = transition['compatibility_scores']
#         print(f"Overall: {scores['overall']:.2f}")
#         print(f"Key: {scores['key']:.2f}")
#         print(f"Tempo: {scores['tempo']:.2f}")
#         print(f"Meter: {scores['meter']:.2f}")
        
#         if transition['transition_tips']:
#             print("\nTransition Tips:")
#             for tip in transition['transition_tips']:
#                 print(f"- {tip}")
#         print("-" * 50)
    
#     if analysis["problem_transitions"]:
#         print("\nProblem Transitions:")
#         for problem in analysis["problem_transitions"]:
#             print(f"\n{problem['position']} (Score: {problem['score']:.2f})")
#             for issue in problem['issues']:
#                 print(f"- {issue}")