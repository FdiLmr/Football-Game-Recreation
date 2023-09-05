import pandas as pd
import numpy as np
import random
import sys
import json

# Constants
MIN_GAIT_LENGTH = 5
MAX_GAIT_LENGTH = 150

# Transition matrix and action norms distribution (based on our previous analysis)
combined_transition_matrix_updated = pd.read_pickle('combined_transition_matrix_updated.pkl')
action_norms_distribution = pd.read_pickle('action_norms_distribution.pkl')

all_unique_labels = combined_transition_matrix_updated.columns.tolist()

def generate_action_sequence(transition_matrix, num_actions):
    # Start with a random action
    current_action = np.random.choice(all_unique_labels)
    sequence = [current_action]
    
    for _ in range(num_actions - 1):
        next_action = np.random.choice(all_unique_labels, p=transition_matrix.loc[current_action].values)
        sequence.append(next_action)
        current_action = next_action
        
    return sequence

def generate_acceleration_norms(action, distribution, min_length, max_length):
    gait_length = random.randint(min_length, max_length)
    generated_norms = np.random.choice(distribution[action], size=gait_length)
    return generated_norms.tolist()

def modify_transition_for_playstyle(transition_matrix, playstyle):
    adjusted_matrix = transition_matrix.copy()
    
    if playstyle == "attacking":
        adjusted_matrix["pass"] *= 1.5
        adjusted_matrix["shot"] *= 1.5
        adjusted_matrix["dribble"] *= 1.5

    elif playstyle == "defending":
        adjusted_matrix["tackle"] *= 1.5
    
    adjusted_matrix = adjusted_matrix.div(adjusted_matrix.sum(axis=1), axis=0)
    return adjusted_matrix

def generate_custom_game(data, transition_matrix, game_length_minutes=90, playstyle="normal", num_games=1):
    avg_duration = sum(len(entry['norm']) for entry in data) / len(data) / 50
    actions_per_minute = 60 / avg_duration
    total_actions = int(game_length_minutes * actions_per_minute)
    adjusted_matrix = modify_transition_for_playstyle(transition_matrix, playstyle)
    
    games = []
    for _ in range(num_games):
        game_actions = generate_action_sequence(adjusted_matrix, total_actions)
        game_norms = [generate_acceleration_norms(action, action_norms_distribution, MIN_GAIT_LENGTH, MAX_GAIT_LENGTH) 
                      for action in game_actions]
        game = [{'label': action, 'norm': norm} for action, norm in zip(game_actions, game_norms)]
        games.append(game)
    
    return games

if __name__ == "__main__":
    game_length_minutes = int(sys.argv[1]) if len(sys.argv) > 1 else 90
    playstyle = sys.argv[2] if len(sys.argv) > 2 else "normal"
    num_games = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    
    with open("match_1.json", 'r') as file:
        match_1_data = json.load(file)
        
    with open('match_2.json', 'r') as f:
        match_2_data = json.load(f)
        
    combined_data = match_1_data + match_2_data

    generated_games = generate_custom_game(combined_data, combined_transition_matrix_updated, game_length_minutes, playstyle, num_games)
    
    # Saving the output
    for idx, game in enumerate(generated_games, 1):
        with open(f'generated_game_{idx}.json', 'w') as f:
            json.dump(game, f, indent=4)

    print(f"Generated {num_games} games of length {game_length_minutes} minutes with {playstyle} style.")