import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import ast
from collections import defaultdict, Counter
import random
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import re
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SongDataset(Dataset):
    """PyTorch Dataset for song sequences"""
    def __init__(self, X, y):
        self.X = torch.FloatTensor(X)
        self.y = torch.LongTensor(y)
        
    def __len__(self):
        return len(self.X)
    
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

class SongLSTM(nn.Module):
    """PyTorch LSTM model for song sequence prediction"""
    def __init__(self, input_size, hidden_size, output_size, num_layers=2, dropout=0.2):
        super(SongLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, 
                           batch_first=True, dropout=dropout)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, output_size)
        
    def forward(self, x):
        # Initialize hidden state and cell state
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        # Forward propagate LSTM
        out, _ = self.lstm(x, (h0, c0))
        
        # Get output from the last time step
        out = self.dropout(out[:, -1, :])
        
        # Fully connected layer
        out = self.fc(out)
        return out
    
    def predict(self, x):
        """Predict probabilities for next song"""
        self.eval()
        with torch.no_grad():
            x_tensor = torch.FloatTensor(x)
            output = self.forward(x_tensor)
            return torch.softmax(output, dim=1).numpy()

class MultiSongbookProcessor:
    def __init__(self, new_songs_path, old_songs_path, order_data_path):
        """
        Initialize the processor with paths to song data from multiple songbooks and order files
        
        Args:
            new_songs_path: Path to JSON with "New" song attributes (REDergaran.json)
            old_songs_path: Path to JSON with "Old" song attributes (wordSongsIndex.json)
            order_data_path: Path to JSON with order data
        """
        self.new_songs_path = new_songs_path
        self.old_songs_path = old_songs_path
        self.order_data_path = order_data_path
        self.new_songs = None
        self.old_songs = None
        self.song_data = None  # Will contain combined songs with prefixed IDs
        self.order_data = None
        self.song_features = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
    def load_data(self):
        """Load song data from both songbooks and order data from JSON files"""
        try:
            # Load new songs
            with open(self.new_songs_path, 'r', encoding='utf-8') as f:
                self.new_songs = json.load(f)
                
            # Load old songs
            with open(self.old_songs_path, 'r', encoding='utf-8') as f:
                self.old_songs = json.load(f)
                
            # Load order data
            with open(self.order_data_path, 'r', encoding='utf-8') as f:
                self.order_data = json.load(f)
            
            # Create combined dictionary with prefixed IDs
            self.song_data = {}
            
            # Add prefix to song IDs to make them unique across songbooks
            for song_id, details in self.new_songs.items():
                combined_id = f"New_{song_id}"
                details['source'] = 'New'
                details['original_id'] = song_id
                self.song_data[combined_id] = details
                
            for song_id, details in self.old_songs.items():
                combined_id = f"Old_{song_id}"
                details['source'] = 'Old'
                details['original_id'] = song_id
                self.song_data[combined_id] = details
                
            logger.info(f"Loaded {len(self.new_songs)} new songs, {len(self.old_songs)} old songs, "
                       f"and {len(self.order_data)} order sets")
            return True
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False
        
    def parse_musical_key(self, key_str):
        """Parse musical key into more useful features"""
        if not key_str or not isinstance(key_str, str):
            return {'root': 'Unknown', 'is_minor': False, 'capo': 0, 'position': 0}
        
        # Extract capo information
        capo = 0
        if '(' in key_str:
            capo_match = re.search(r'\(([-+]?\d+)\)', key_str)
            if capo_match:
                capo = int(capo_match.group(1))
        
        # Clean the key string
        clean_key = re.sub(r'\(.*?\)', '', key_str).strip()
        
        # Determine if minor
        is_minor = 'm' in clean_key or 'minor' in clean_key.lower()
        
        # Extract root note
        root_match = re.match(r'^([A-G][b#]?)', clean_key)
        root = root_match.group(1) if root_match else 'C'
        
        # Map to circle of fifths position (0 = C, 1 = G, etc.)
        circle_map = {
            'C': 0, 'G': 1, 'D': 2, 'A': 3, 'E': 4, 'B': 5, 'F#': 6, 'C#': 7,
            'F': -1, 'Bb': -2, 'Eb': -3, 'Ab': -4, 'Db': -5, 'Gb': -6, 'Cb': -7
        }
        position = circle_map.get(root, 0)
        
        return {
            'root': root,
            'is_minor': is_minor,
            'capo': capo,
            'position': position
        }
        
    def extract_song_features(self):
        """Extract and preprocess features from song data with improved musical understanding"""
        # Create a DataFrame from song data
        songs = []
        for combined_id, details in self.song_data.items():
            # Parse musical key
            key_info = self.parse_musical_key(details.get('key', ''))
            
            # Parse tempo/speed
            speed = 0
            speed_str = details.get('speed', '')
            if isinstance(speed_str, str) and speed_str.isdigit():
                speed = int(speed_str)
            elif isinstance(speed_str, (int, float)):
                speed = int(speed_str)
                
            # Create song info dictionary
            song_info = {
                'id': combined_id,
                'source': details.get('source', 'Unknown'),
                'original_id': details.get('original_id', combined_id),
                'title': details.get('Title', 'Unknown'),
                'root_key': key_info['root'],
                'is_minor': key_info['is_minor'],
                'capo': key_info['capo'],
                'key_position': key_info['position'],
                'speed': speed,
                'style': details.get('style', 'Unknown'),
                'song_type': details.get('song_type', 'Unknown'),
                'timeSig': details.get('timeSig', '4/4')
            }
            songs.append(song_info)
            
        # Convert to DataFrame
        self.songs_df = pd.DataFrame(songs)
        
        # Handle missing values
        self.songs_df['speed'] = self.songs_df['speed'].fillna(0)
        for col in ['root_key', 'style', 'song_type', 'timeSig']:
            self.songs_df[col] = self.songs_df[col].fillna('Unknown')
        
        # One-hot encode categorical features
        categorical_features = ['root_key', 'style', 'song_type', 'timeSig', 'source']
        self.encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        encoded_features = self.encoder.fit_transform(self.songs_df[categorical_features])
        
        # Scale numerical features
        numerical_features = self.songs_df[['speed', 'key_position', 'capo']].values
        self.scaler = StandardScaler()
        scaled_numerical = self.scaler.fit_transform(numerical_features)
        
        # Combine binary, encoded, and numerical features
        binary_features = self.songs_df[['is_minor']].astype(int).values
        self.song_features = np.hstack([encoded_features, scaled_numerical, binary_features])
        
        # Create a mapping from song ID to feature index
        self.song_id_to_index = {song_id: i for i, song_id in enumerate(self.songs_df['id'])}
        self.index_to_song_id = {i: song_id for song_id, i in self.song_id_to_index.items()}
        
        # Create mapping from original IDs to combined IDs
        self.original_to_combined = {}
        for _, row in self.songs_df.iterrows():
            key = f"{row['source']}_{row['original_id']}"
            self.original_to_combined[(row['source'], row['original_id'])] = row['id']
        
        logger.info(f"Extracted features with shape: {self.song_features.shape}")
        return True
        
    def process_order_data(self):
        """Process order data to extract song sets with prefixed IDs"""
        # Extract song sets from order data
        song_sets = []
        date_infos = []
        
        for order_id, order_info in self.order_data.items():
            try:
                # Parse the songList string into a list of tuples
                song_list_str = order_info.get('songList', '[]')
                song_list = ast.literal_eval(song_list_str)
                
                # Convert to combined IDs
                combined_ids = []
                for source, original_id in song_list:
                    # Map to combined ID format
                    combined_id = f"{source}_{original_id}"
                    
                    # Check if this ID exists in our combined dictionary
                    if combined_id in self.song_data:
                        combined_ids.append(combined_id)
                    else:
                        logger.warning(f"Song {source} {original_id} not found in song data")
                
                if combined_ids:
                    song_sets.append(combined_ids)
                    # Extract date information if available
                    if 'dateMod' in order_info:
                        date_infos.append({
                            'order_id': order_id,
                            'date': order_info['dateMod'],
                            'song_count': len(combined_ids)
                        })
            except (SyntaxError, ValueError) as e:
                logger.warning(f"Error processing order {order_id}: {e}")
                
        self.song_sets = song_sets
        self.date_infos = date_infos if date_infos else None
        logger.info(f"Processed {len(song_sets)} valid song sets")
        
        # Build transition matrix and co-occurrence matrix
        self.build_transition_matrices()
        return True
        
    def build_transition_matrices(self):
        """Build matrices for song transitions and co-occurrences"""
        n_songs = len(self.song_data)
        self.co_occurrence = np.zeros((n_songs, n_songs))
        self.transitions = np.zeros((n_songs, n_songs))
        
        # Track transitions and co-occurrences
        for song_set in self.song_sets:
            indices = [self.song_id_to_index[song_id] 
                      for song_id in song_set 
                      if song_id in self.song_id_to_index]
            
            # Process co-occurrences
            for i in indices:
                for j in indices:
                    if i != j:
                        self.co_occurrence[i, j] += 1
            
            # Process direct transitions (song order matters)
            for i in range(len(indices) - 1):
                self.transitions[indices[i], indices[i+1]] += 1
                        
        # Normalize transition probabilities
        row_sums = self.transitions.sum(axis=1, keepdims=True)
        self.transition_probs = np.divide(self.transitions, row_sums, 
                                         out=np.zeros_like(self.transitions), 
                                         where=row_sums!=0)
        
        logger.info("Built transition and co-occurrence matrices")
        return True
        
    def analyze_song_keys(self):
        """Analyze key relationships between songs in sets"""
        key_transitions = defaultdict(int)
        source_transitions = {
            ('New', 'New'): 0,
            ('New', 'Old'): 0,
            ('Old', 'New'): 0,
            ('Old', 'Old'): 0
        }
        
        for song_set in self.song_sets:
            for i in range(len(song_set) - 1):
                if song_set[i] in self.song_data and song_set[i+1] in self.song_data:
                    # Get key information
                    current_song = self.song_data[song_set[i]]
                    next_song = self.song_data[song_set[i+1]]
                    
                    key1 = self.parse_musical_key(current_song.get('key', ''))
                    key2 = self.parse_musical_key(next_song.get('key', ''))
                    
                    # Calculate key distance on circle of fifths
                    key_distance = key2['position'] - key1['position']
                    key_transitions[key_distance] += 1
                    
                    # Track source transitions (New to Old, Old to New, etc.)
                    source1 = current_song.get('source', 'Unknown')
                    source2 = next_song.get('source', 'Unknown')
                    if (source1, source2) in source_transitions:
                        source_transitions[(source1, source2)] += 1
        
        self.key_transitions = dict(key_transitions)
        self.source_transitions = source_transitions
        
        logger.info("Analyzed key and source transitions")
        
        # Calculate most common key changes
        if key_transitions:
            total = sum(key_transitions.values())
            self.key_transition_probs = {k: v/total for k, v in key_transitions.items()}
            
        # Calculate source transition probabilities
        total_source_transitions = sum(source_transitions.values())
        if total_source_transitions > 0:
            self.source_transition_probs = {k: v/total_source_transitions 
                                          for k, v in source_transitions.items()}
            logger.info(f"Source transitions: {self.source_transition_probs}")
        
        return True
        
    def create_sequence_data(self):
        """Create sequence data for training a PyTorch LSTM model"""
        # Create sequences from song sets
        sequences = []
        targets = []
        
        sequence_length = 3  # Number of songs to consider as context
        
        for song_set in self.song_sets:
            if len(song_set) > sequence_length:
                indices = [self.song_id_to_index[song_id] 
                          for song_id in song_set 
                          if song_id in self.song_id_to_index]
                
                for i in range(len(indices) - sequence_length):
                    seq = indices[i:i+sequence_length]
                    target = indices[i+sequence_length]
                    
                    # Convert indices to feature vectors
                    seq_features = [self.song_features[idx] for idx in seq]
                    sequences.append(seq_features)
                    targets.append(target)
        
        # Convert to numpy arrays
        if sequences:
            self.X = np.array(sequences)
            self.y = np.array(targets)
            
            logger.info(f"Created {len(sequences)} training sequences")
            return True
        else:
            logger.warning("Not enough data to create sequences")
            self.X = None
            self.y = None
            return False
            
    def build_pytorch_model(self):
        """Build a PyTorch LSTM model for song sequence prediction"""
        if self.X is not None and len(self.X) > 10:  # Only if we have enough data
            input_size = self.X.shape[2]  # Feature dimension
            hidden_size = 128
            output_size = len(self.song_id_to_index)
            
            self.model = SongLSTM(
                input_size=input_size,
                hidden_size=hidden_size,
                output_size=output_size,
                num_layers=2,
                dropout=0.3
            ).to(self.device)
            
            logger.info(f"Built PyTorch LSTM model with {output_size} output classes")
            return True
        else:
            logger.warning("Not enough data to build LSTM model, using similarity-based approach instead")
            return False
            
    def train_model(self, epochs=50, batch_size=16, learning_rate=0.001):
        """Train the PyTorch LSTM model if available"""
        if self.model is not None and self.X is not None:
            # Create PyTorch dataset and dataloader
            dataset = SongDataset(self.X, self.y)
            
            # Split into training and validation sets (80/20)
            train_size = int(0.8 * len(dataset))
            val_size = len(dataset) - train_size
            train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
            
            train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
            val_loader = DataLoader(val_dataset, batch_size=batch_size)
            
            # Define loss function and optimizer
            criterion = nn.CrossEntropyLoss()
            optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
            scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=5)
            
            # Training loop
            best_val_loss = float('inf')
            for epoch in range(epochs):
                # Training
                self.model.train()
                train_loss = 0
                for inputs, targets in train_loader:
                    inputs, targets = inputs.to(self.device), targets.to(self.device)
                    
                    # Forward pass
                    outputs = self.model(inputs)
                    loss = criterion(outputs, targets)
                    
                    # Backward pass and optimize
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                    
                    train_loss += loss.item() * inputs.size(0)
                
                # Validation
                self.model.eval()
                val_loss = 0
                correct = 0
                total = 0
                with torch.no_grad():
                    for inputs, targets in val_loader:
                        inputs, targets = inputs.to(self.device), targets.to(self.device)
                        outputs = self.model(inputs)
                        loss = criterion(outputs, targets)
                        val_loss += loss.item() * inputs.size(0)
                        
                        # Calculate accuracy
                        _, predicted = torch.max(outputs.data, 1)
                        total += targets.size(0)
                        correct += (predicted == targets).sum().item()
                
                # Calculate average losses and accuracy
                train_loss = train_loss / len(train_dataset)
                val_loss = val_loss / len(val_dataset)
                accuracy = 100 * correct / total
                
                # Adjust learning rate
                scheduler.step(val_loss)
                
                # Save best model
                if val_loss < best_val_loss:
                    best_val_loss = val_loss
                    torch.save(self.model.state_dict(), 'best_song_model.pt')
                
                if (epoch + 1) % 5 == 0:
                    logger.info(f"Epoch {epoch+1}/{epochs}, Train Loss: {train_loss:.4f}, "
                               f"Val Loss: {val_loss:.4f}, Accuracy: {accuracy:.2f}%")
            
            # Load best model
            self.model.load_state_dict(torch.load('best_song_model.pt'))
            logger.info("Trained PyTorch LSTM model")
            return True
        else:
            logger.warning("No model or training data available")
            return False
    
    def generate_song_set(self, num_songs=6, seed_song_id=None, balance_sources=True, temperature=1.0):
        """
        Generate a new compatible song set with improved inference
        
        Args:
            num_songs: Number of songs to include in the set
            seed_song_id: Starting song ID (if None, one will be randomly selected)
            balance_sources: Whether to try to balance Old and New songs
            temperature: Controls randomness (higher = more random)
            
        Returns:
            List of song IDs forming a compatible set
        """
        # If no seed song provided, select a random one
        if seed_song_id is None:
            seed_song_id = random.choice(list(self.song_data.keys()))
        else:
            # Check if the seed is in the format "New_123" or just "123"
            if "_" not in seed_song_id and (seed_song_id in self.new_songs or seed_song_id in self.old_songs):
                # Determine the source based on which songbook contains this ID
                source = "New" if seed_song_id in self.new_songs else "Old"
                seed_song_id = f"{source}_{seed_song_id}"
            
        # Check if seed song exists in our data
        if seed_song_id not in self.song_id_to_index:
            logger.warning(f"Seed song {seed_song_id} not found. Selecting a random song.")
            seed_song_id = random.choice(list(self.song_id_to_index.keys()))
            
        seed_index = self.song_id_to_index[seed_song_id]
        song_set = [seed_song_id]
        
        # Helper function to apply temperature to probabilities
        def apply_temperature(probs, temp=1.0):
            if temp == 0:
                # Return one-hot with the max probability (greedy)
                max_idx = np.argmax(probs)
                one_hot = np.zeros_like(probs)
                one_hot[max_idx] = 1.0
                return one_hot
            else:
                # Apply temperature scaling
                probs = np.power(probs, 1.0/temp)
                probs = probs / np.sum(probs)
                return probs
        
        # Track source counts for balancing
        source_counts = {'New': 0, 'Old': 0}
        for song_id in song_set:
            source = self.song_data[song_id]['source']
            source_counts[source] += 1
        
        # If we have an LSTM model, use it; otherwise use improved similarity-based approach
        if self.model is not None and self.X is not None:
            # Use LSTM for prediction
            sequence = []
            current_index = seed_index
            
            # For the first few predictions, use similarity until we have enough context
            while len(sequence) < 3:
                # Get song transitions from transition matrix
                transitions = self.transition_probs[current_index]
                
                # Filter out songs already in the set
                for idx in [self.song_id_to_index[s] for s in song_set if s in self.song_id_to_index]:
                    transitions[idx] = 0
                    
                # Apply source balancing if requested
                if balance_sources and sum(source_counts.values()) > 0:
                    # Calculate current ratio
                    current_ratio = source_counts['New'] / sum(source_counts.values())
                    
                    # If we're off balance, boost the probability of the less-represented source
                    if current_ratio < 0.4:  # Need more New songs
                        target_source = 'New'
                    elif current_ratio > 0.6:  # Need more Old songs
                        target_source = 'Old'
                    else:
                        target_source = None
                    
                    if target_source:
                        for i, prob in enumerate(transitions):
                            if prob > 0 and i in self.index_to_song_id:
                                song_id = self.index_to_song_id[i]
                                if self.song_data[song_id]['source'] == target_source:
                                    transitions[i] *= 1.5  # Boost probability
                
                # Select next song based on transition probabilities with temperature
                if np.sum(transitions) > 0:
                    # Apply temperature to control randomness
                    prob = apply_temperature(transitions, temperature)
                    next_index = np.random.choice(len(transitions), p=prob)
                else:
                    # If no transitions, use feature similarity
                    feature_similarities = cosine_similarity([self.song_features[current_index]], self.song_features)[0]
                    # Filter out songs already in the set
                    for idx in [self.song_id_to_index[s] for s in song_set if s in self.song_id_to_index]:
                        feature_similarities[idx] = 0
                    # Apply temperature
                    probs = apply_temperature(feature_similarities, temperature)
                    next_index = np.random.choice(len(feature_similarities), p=probs/np.sum(probs))
                    
                next_song_id = self.index_to_song_id[next_index]
                song_set.append(next_song_id)
                
                # Update source counts
                source = self.song_data[next_song_id]['source']
                source_counts[source] += 1
                
                sequence.append(self.song_features[current_index])
                current_index = next_index
                
            # Now use LSTM for remaining predictions
            while len(song_set) < num_songs:
                # Prepare input sequence
                input_seq = np.array([sequence[-3:]])  # Last 3 songs as context
                
                # Get model prediction
                prediction = self.model.predict(input_seq)[0]
                
                # Filter out songs already in the set
                for idx in [self.song_id_to_index[s] for s in song_set if s in self.song_id_to_index]:
                    prediction[idx] = 0
                    
                # Apply source balancing if requested
                if balance_sources and sum(source_counts.values()) > 0:
                    # Calculate current ratio
                    current_ratio = source_counts['New'] / sum(source_counts.values())
                    
                    # If we're off balance, boost the probability of the less-represented source
                    if current_ratio < 0.4:  # Need more New songs
                        target_source = 'New'
                    elif current_ratio > 0.6:  # Need more Old songs
                        target_source = 'Old'
                    else:
                        target_source = None
                    
                    if target_source:
                        for i, prob in enumerate(prediction):
                            if prob > 0 and i in self.index_to_song_id:
                                song_id = self.index_to_song_id[i]
                                if self.song_data[song_id]['source'] == target_source:
                                    prediction[i] *= 1.5  # Boost probability
                
                # If all predictions filtered out, use similarity
                if np.sum(prediction) == 0:
                    feature_similarities = cosine_similarity([self.song_features[current_index]], self.song_features)[0]
                    for idx in [self.song_id_to_index[s] for s in song_set if s in self.song_id_to_index]:
                        feature_similarities[idx] = 0
                    probs = apply_temperature(feature_similarities, temperature)
                    if np.sum(probs) > 0:
                        next_index = np.random.choice(len(feature_similarities), p=probs/np.sum(probs))
                    else:
                        # Fallback to random unselected song
                        available_indices = [i for i in range(len(self.song_features)) 
                                           if self.index_to_song_id[i] not in song_set]
                        next_index = random.choice(available_indices)
                else:
                    # Apply temperature to model predictions
                    prediction = apply_temperature(prediction, temperature)
                    if np.sum(prediction) > 0:
                        next_index = np.random.choice(len(prediction), p=prediction/np.sum(prediction))
                    else:
                        # If all zero after temperature, select max
                        next_index = np.argmax(prediction)
                    
                next_song_id = self.index_to_song_id[next_index]
                song_set.append(next_song_id)
                
                # Update source counts
                source = self.song_data[next_song_id]['source']
                source_counts[source] += 1
                
                sequence.append(self.song_features[next_index])
                current_index = next_index
                
        else:
            # Use improved similarity-based approach with key progression
            current_index = seed_index
            current_key_info = self.parse_musical_key(self.song_data[seed_song_id].get('key', ''))
            current_source = self.song_data[seed_song_id]['source']
            
            while len(song_set) < num_songs:
                # Blend transitions and co-occurrence
                if np.sum(self.transition_probs[current_index]) > 0:
                    blend = 0.7 * self.transition_probs[current_index] + 0.3 * self.co_occurrence[current_index]
                else:
                    blend = self.co_occurrence[current_index]
                
                # Filter out songs already in the set
                for idx in [self.song_id_to_index[s] for s in song_set if s in self.song_id_to_index]:
                    blend[idx] = 0
                    
                # Apply source balancing if requested
                if balance_sources and sum(source_counts.values()) > 0:
                    # Calculate current ratio
                    current_ratio = source_counts['New'] / sum(source_counts.values())
                    
                    # If we're off balance, boost the probability of the less-represented source
                    if current_ratio < 0.4:  # Need more New songs
                        target_source = 'New'
                    elif current_ratio > 0.6:  # Need more Old songs
                        target_source = 'Old'
                    else:
                        target_source = None
                    
                    if target_source:
                        for i, prob in enumerate(blend):
                            if prob > 0 and i in self.index_to_song_id:
                                song_id = self.index_to_song_id[i]
                                if self.song_data[song_id]['source'] == target_source:
                                    blend[i] *= 1.5  # Boost probability
                    
                # Apply musical key preference if available
                if hasattr(self, 'key_transition_probs') and self.key_transition_probs:
                    # Apply key transition preference
                    for i in range(len(blend)):
                        if blend[i] > 0 and i in self.index_to_song_id:
                            song_id = self.index_to_song_id[i]
                            next_key_info = self.parse_musical_key(self.song_data[song_id].get('key', ''))
                            key_distance = next_key_info['position'] - current_key_info['position']
                            
                            # Boost songs with common key transitions
                            key_boost = self.key_transition_probs.get(key_distance, 0.1)
                            blend[i] *= (1 + key_boost)
                
                # Apply source transition preference if available
                if hasattr(self, 'source_transition_probs'):
                    for i in range(len(blend)):
                        if blend[i] > 0 and i in self.index_to_song_id:
                            song_id = self.index_to_song_id[i]
                            next_source = self.song_data[song_id]['source']
                            
                            # Get transition probability for this source pair
                            source_prob = self.source_transition_probs.get((current_source, next_source), 0.25)
                            blend[i] *= (1 + source_prob)
                
                # If no valid next songs, use feature similarity
                if np.sum(blend) == 0:
                    # Use cosine similarity of song features
                    feature_similarities = cosine_similarity([self.song_features[current_index]], self.song_features)[0]
                    
                    # Filter out songs already in the set
                    for idx in [self.song_id_to_index[s] for s in song_set if s in self.song_id_to_index]:
                        feature_similarities[idx] = 0
                        
                    blend = feature_similarities
                
                # Apply temperature and select next song
                probs = apply_temperature(blend, temperature)
                if np.sum(probs) > 0:
                    next_index = np.random.choice(len(probs), p=probs/np.sum(probs))
                else:
                    # Fallback to random unselected song
                    available_indices = [i for i in range(len(self.song_features)) 
                                       if self.index_to_song_id[i] not in song_set]
                    next_index = random.choice(available_indices)
                    
                next_song_id = self.index_to_song_id[next_index]
                song_set.append(next_song_id)
                
                # Update source counts
                next_source = self.song_data[next_song_id]['source']
                source_counts[next_source] += 1
                
                # Update current index and key info for next iteration
                current_index = next_index
                current_key_info = self.parse_musical_key(self.song_data[next_song_id].get('key', ''))
                current_source = next_source
                
        logger.info(f"Generated set with {source_counts['New']} New songs and {source_counts['Old']} Old songs")
        return song_set
    
    def get_song_details(self, song_id):
        """Get detailed information about a song"""
        if song_id in self.song_data:
            return self.song_data[song_id]
        return None
    
    def explain_song_set(self, song_set):
        """Provide explanation for why songs were selected"""
        explanations = []
        for i in range(len(song_set) - 1):
            current_id = song_set[i]
            next_id = song_set[i+1]
            
            if current_id in self.song_data and next_id in self.song_data:
                current = self.song_data[current_id]
                next_song = self.song_data[next_id]
                
                # Get indices
                current_idx = self.song_id_to_index.get(current_id)
                next_idx = self.song_id_to_index.get(next_id)
                
                # Get key info
                current_key = self.parse_musical_key(current.get('key', ''))
                next_key = self.parse_musical_key(next_song.get('key', ''))
                
                # Construct explanation
                explanation = {
                    'transition': f"{current.get('Title', 'Unknown')} ({current_id}) → {next_song.get('Title', 'Unknown')} ({next_id})",
                    'sources': f"{current.get('source', 'Unknown')} to {next_song.get('source', 'Unknown')}",
                    'key_change': f"{current.get('key', 'Unknown')} to {next_song.get('key', 'Unknown')}",
                    'tempo_change': f"{current.get('speed', 'Unknown')} to {next_song.get('speed', 'Unknown')} BPM",
                }
                
                # Add relationship info if available
                if current_idx is not None and next_idx is not None:
                    if self.transitions[current_idx, next_idx] > 0:
                        explanation['relationship'] = f"These songs have appeared together in sequence {int(self.transitions[current_idx, next_idx])} times"
                    elif self.co_occurrence[current_idx, next_idx] > 0:
                        explanation['relationship'] = f"These songs have appeared in the same set {int(self.co_occurrence[current_idx, next_idx])} times"
                    else:
                        explanation['relationship'] = "These songs were selected based on musical similarity"
                
                explanations.append(explanation)
        
        return explanations
    
    def generate_multiple_sets(self, num_sets=5, songs_per_set=6, balance_sources=True, temperature=1.0):
        """Generate multiple song sets with varying temperatures"""
        sets = []
        
        # Gradually increase temperature for more variety
        for i in range(num_sets):
            # Adjust temperature to get more variety in later sets
            set_temp = temperature * (1 + 0.1 * i)
            
            song_set = self.generate_song_set(
                num_songs=songs_per_set, 
                balance_sources=balance_sources,
                temperature=set_temp
            )
            
            set_info = []
            source_counts = {'New': 0, 'Old': 0}
            
            for song_id in song_set:
                details = self.get_song_details(song_id)
                if details:
                    # Extract original ID without prefix
                    original_id = details.get('original_id', song_id.split('_')[-1])
                    source = details.get('source', 'Unknown')
                    source_counts[source] += 1
                    
                    set_info.append({
                        'id': original_id,  # Original ID without prefix
                        'source': source,
                        'title': details.get('Title', 'Unknown'),
                        'key': details.get('key', 'Unknown'),
                        'speed': details.get('speed', 'Unknown'),
                        'style': details.get('style', 'Unknown'),
                        'song_type': details.get('song_type', 'Unknown')
                    })
            
            # Add explanations
            explanations = self.explain_song_set(song_set)
            
            sets.append({
                'songs': set_info,
                'explanations': explanations,
                'temperature': set_temp,
                'source_counts': source_counts
            })
            
        return sets
    
    def format_for_export(self, song_set):
        """Format a generated song set for export in SongList format"""
        formatted_set = []
        
        for song_id in song_set:
            if song_id in self.song_data:
                # Extract source and original ID
                source = self.song_data[song_id]['source']
                original_id = self.song_data[song_id]['original_id']
                
                # Format as tuple string like in the original data
                formatted_set.append(f"('{source}', '{original_id}')")
        
        # Join with commas and wrap in square brackets
        return "[" + ", ".join(formatted_set) + "]"
    
    def export_sets_as_orders(self, sets, output_dir='generated_orders'):
        """Export generated sets in the same format as original order files"""
        os.makedirs(output_dir, exist_ok=True)
        
        exported_orders = {}
        for i, set_data in enumerate(sets):
            song_set = [f"{song['source']}_{song['id']}" for song in set_data['songs']]
            
            # Format song list in the original string representation format
            formatted_songs = self.format_for_export(song_set)
            
            # Create order entry
            order_id = f"generated_{i+1}.docx"
            order_entry = {
                "dateMod": pd.Timestamp.now().timestamp(),
                "path": f"C:\\generated\\{order_id}",
                "basePth": "generated",
                "songList": formatted_songs
            }
            
            exported_orders[order_id] = order_entry
        
        # Save to JSON
        output_path = os.path.join(output_dir, 'generated_orders.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(exported_orders, f, ensure_ascii=False, indent=2)
            
        logger.info(f"Exported {len(sets)} generated sets to {output_path}")
        return output_path
    
    def process_pipeline(self):
        """Run the complete processing pipeline with error handling"""
        try:
            if not self.load_data():
                logger.error("Failed to load data")
                return False
            
            if not self.extract_song_features():
                logger.error("Failed to extract song features")
                return False
            
            if not self.process_order_data():
                logger.error("Failed to process order data")
                return False
            
            self.analyze_song_keys()
            
            # Only proceed with ML if we have enough data
            if self.create_sequence_data():
                if self.build_pytorch_model():
                    self.train_model()
            
            logger.info("Pipeline completed successfully")
            return True
        except Exception as e:
            logger.error(f"Pipeline error: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False

    def save_model(self, path="song_model.pt"):
        """Save the trained model"""
        if self.model:
            try:
                torch.save({
                    'model_state_dict': self.model.state_dict(),
                    'feature_size': self.song_features.shape[1],
                    'output_size': len(self.song_id_to_index)
                }, path)
                logger.info(f"Model saved to {path}")
                return True
            except Exception as e:
                logger.error(f"Error saving model: {e}")
                return False
        return False
        
    def load_saved_model(self, path="song_model.pt"):
        """Load a saved model"""
        try:
            checkpoint = torch.load(path)
            feature_size = checkpoint.get('feature_size')
            output_size = checkpoint.get('output_size', len(self.song_id_to_index))
            
            self.model = SongLSTM(
                input_size=feature_size,
                hidden_size=128,
                output_size=output_size
            ).to(self.device)
            
            self.model.load_state_dict(checkpoint['model_state_dict'])
            self.model.eval()
            logger.info(f"Model loaded from {path}")
            return True
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False

# Example usage
def main():
    processor = MultiSongbookProcessor(
        'REDergaran.json',           # New songs
        'wordSongsIndex.json',       # Old songs
        'songs_cleaned.json'
    )
    processor.process_pipeline()
    
    # Save the model
    processor.save_model()
    
    # Generate balanced sets with mix of old and new songs
    new_sets = processor.generate_multiple_sets(num_sets=3, songs_per_set=6, balance_sources=True)
    
    # Print the generated sets
    for i, song_set in enumerate(new_sets, 1):
        source_counts = song_set['source_counts']
        print(f"\nSong Set {i} (Temperature: {song_set['temperature']:.2f}) - "
              f"New: {source_counts['New']}, Old: {source_counts['Old']}")
        
        for song in song_set['songs']:
            print(f"  {song['source']} {song['id']}: {song['title']}, Key: {song['key']}, Speed: {song['speed']}")
        
        print("\nTransition Explanations:")
        for expl in song_set['explanations']:
            print(f"  • {expl['transition']}")
            print(f"    - Sources: {expl['sources']}")
            print(f"    - Key change: {expl['key_change']}")
            print(f"    - Tempo change: {expl['tempo_change']}")
            if 'relationship' in expl:
                print(f"    - {expl['relationship']}")
            print()
            
    # Export the generated sets to JSON
    with open('generated_sets.json', 'w', encoding='utf-8') as f:
        json.dump(new_sets, f, ensure_ascii=False, indent=2)
    
    # Export in original order format
    processor.export_sets_as_orders(new_sets)
    
if __name__ == "__main__":
    main()