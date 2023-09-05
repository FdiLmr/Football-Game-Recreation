
# Use Python 3.11 as the parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY game_recreation_script.py ./
COPY combined_transition_matrix_updated.pkl ./
COPY action_norms_distribution.pkl ./
COPY match_1.json ./
COPY match_2.json ./

# Install necessary libraries
RUN pip install pandas numpy

# Run the game recreation script when the container launches
ENTRYPOINT ["python", "./game_recreation_script.py"]
