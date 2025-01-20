
class MusicalCompatibility:
    def __init__(self):
        # Define key relationships in circle of fifths (C is center)
        self.circle_of_fifths = {
            'C': 0,
            'G': 1,  'F': -1,
            'D': 2,  'Bb': -2,
            'A': 3,  'Eb': -3,
            'E': 4,  'Ab': -4,
            'B': 5,  'Db': -5,
            'F#': 6, 'Gb': -6
        }
        
        # Define relative minor/major relationships
        self.relative_keys = {
            'C': 'Am',   'Am': 'C',
            'G': 'Em',   'Em': 'G',
            'D': 'Bm',   'Bm': 'D',
            'A': 'F#m',  'F#m': 'A',
            'E': 'C#m',  'C#m': 'E',
            'B': 'G#m',  'G#m': 'B',
            'F#': 'D#m', 'D#m': 'F#'
        }
        
        # Define common time signature groupings
        self.meter_groups = {
            'simple': ['4/4', '2/4', '2/2'],
            'compound': ['6/8', '12/8', '9/8'],
            'waltz': ['3/4', '6/4']
        }
    
    def calculate_key_compatibility(self, key1: str, key2: str) -> float:
        """
        Calculate how well two keys work together.
        Returns score from 0 (clash) to 1 (perfect compatibility)
        """
        # Direct match is perfect
        if key1 == key2:
            return 1.0
            
        # Relative major/minor is nearly perfect
        if key1 in self.relative_keys and self.relative_keys[key1] == key2:
            return 0.95
            
        # Calculate distance in circle of fifths
        try:
            distance = abs(self.circle_of_fifths[key1] - self.circle_of_fifths[key2])
            # Convert distance to compatibility score (closer = higher score)
            return max(0, 1 - (distance * 0.15))
        except KeyError:
            return 0.0
    
    def calculate_tempo_compatibility(self, tempo1: int, tempo2: int) -> float:
        """
        Calculate how well two tempos work together.
        Returns score from 0 (clash) to 1 (perfect compatibility)
        """
        # Calculate ratio between tempos
        ratio = max(tempo1, tempo2) / min(tempo1, tempo2)
        
        # Perfect matches and common ratios
        if ratio == 1:  # Same tempo
            return 1.0
        elif 1.95 < ratio < 2.05:  # Double/half tempo
            return 0.9
        elif 1.45 < ratio < 1.55:  # 3:2 ratio
            return 0.8
        
        # Calculate general compatibility based on closeness
        tempo_diff = abs(tempo1 - tempo2)
        if tempo_diff <= 5:
            return 0.95
        elif tempo_diff <= 10:
            return 0.85
        elif tempo_diff <= 20:
            return 0.7
        else:
            return max(0, 1 - (tempo_diff * 0.01))
    
    def calculate_meter_compatibility(self, time1: str, time2: str) -> float:
        """
        Calculate how well two time signatures work together.
        Returns score from 0 (clash) to 1 (perfect compatibility)
        """
        # Same time signature
        if time1 == time2:
            return 1.0
            
        # Find which groups each time signature belongs to
        groups1 = [group for group, sigs in self.meter_groups.items() if time1 in sigs]
        groups2 = [group for group, sigs in self.meter_groups.items() if time2 in sigs]
        
        # Same meter group (e.g., both simple meters)
        if any(group in groups1 for group in groups2):
            return 0.8
            
        # Convert to beats per measure for comparison
        def get_beats(time_sig):
            num, denom = map(int, time_sig.split('/'))
            return num
        
        beats1 = get_beats(time1)
        beats2 = get_beats(time2)
        
        # Related meters (e.g., 3/4 to 6/8)
        if beats1 * 2 == beats2 or beats2 * 2 == beats1:
            return 0.7
            
        return 0.5  # Different but not necessarily incompatible
    
    def get_transition_recommendation(self, song1, song2) -> dict:
        """
        Analyze two songs and provide detailed compatibility information
        """
        key_score = self.calculate_key_compatibility(song1['key'], song2['key'])
        tempo_score = self.calculate_tempo_compatibility(song1['tempo'], song2['tempo'])
        meter_score = self.calculate_meter_compatibility(
            song1['time_signature'], 
            song2['time_signature']
        )
        
        # Weight the scores (you can adjust these weights)
        weighted_score = (
            key_score * 0.4 +
            tempo_score * 0.4 +
            meter_score * 0.2
        )
        
        recommendations = {
            'overall_compatibility': weighted_score,
            'key_compatibility': key_score,
            'tempo_compatibility': tempo_score,
            'meter_compatibility': meter_score,
            'transition_tips': []
        }
        
        # Generate specific recommendations
        if key_score < 0.7:
            recommendations['transition_tips'].append(
                f"Consider using a musical bridge or modulation to transition between "
                f"{song1['key']} and {song2['key']}"
            )
            
        if tempo_score < 0.7:
            recommendations['transition_tips'].append(
                f"Gradual tempo change recommended from {song1['tempo']} to {song2['tempo']} BPM"
            )
            
        if meter_score < 0.7:
            recommendations['transition_tips'].append(
                f"Be careful with the meter change from {song1['time_signature']} to "
                f"{song2['time_signature']}. Consider a clear rhythmic transition."
            )
            
        return recommendations

# Example usage
if __name__ == "__main__":
    compatibility = MusicalCompatibility()
    
    song1 = {
        'key': 'C',
        'tempo': 75,
        'time_signature': '4/4'
    }
    
    song2 = {
        'key': 'Dm',
        'tempo': 113,
        'time_signature': '4/4'
    }
    
    result = compatibility.get_transition_recommendation(song1, song2)
    # print("\nCompatibility Analysis:")
    print(f"Overall Score: {result['overall_compatibility']:.2f}")
    # print(f"Key Compatibility: {result['key_compatibility']:.2f}")
    # print(f"Tempo Compatibility: {result['tempo_compatibility']:.2f}")
    # print(f"Meter Compatibility: {result['meter_compatibility']:.2f}")
    # print(result)
    # if result['transition_tips']:
    #     print("\nTransition Tips:")
    #     for tip in result['transition_tips']:
    #         print(f"- {tip}")
