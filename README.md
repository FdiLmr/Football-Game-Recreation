
# Football Game Recreation

This repository provides tools to recreate football games based on player movements and actions. Using transition matrices and acceleration data, the tools generate simulated games that mimic real football match dynamics.

## Contents

1. **game_recreation_script_modified.py** - The main Python script to generate recreated games.
2. **Dockerfile** - Instructions for Docker to build an image for game recreation.
3. Other necessary files like `combined_transition_matrix_updated.pkl` and `action_norms_distribution.pkl` that the script depends on.
4. **genfoot.ipynb** - Jupyter Notebook containing the data analysis and details on the conception of the algorithm.

## Requirements

- Docker: Ensure you have [Docker](https://docs.docker.com/get-docker/) installed.

## Building the Docker Image

1. Clone this repository to your local machine.
2. Navigate to the directory containing the Dockerfile.
3. Build the Docker image using the command:
   ```
   docker build -t game_recreation:latest .
   ```

## Running the Docker Container

To generate a simulated game, run:

```
docker run game_recreation [game_duration] [game_type] [number_of_games]
```

- `game_duration`: Duration of the game in minutes (e.g., 15, 20, 60, etc.)
- `game_type`: Type of gameplay desired. Options include "attacking", "defending", or "normal".
- `number_of_games`: Number of games desired.

Example:

```
docker run game_recreation 15 attacking 3
```

This will generate 3 15-minute attacking-style game.

## Output

Each generated game will be saved in a separate JSON file in the format `generated_game_1.json`, `generated_game_2.json`, etc.
