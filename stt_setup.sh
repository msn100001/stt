#!/bin/bash

# This script sets up a Python virtual environment and installs the required dependencies for the speech-to-text application with verbose output.

# Ensure the script exits on any error
set -e

# Define variables
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
MODEL_URL="https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
MODEL_DIR="model"

# Create and activate virtual environment
echo "Creating virtual environment..."
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

if [ $? -eq 0 ]; then
    echo "Virtual environment created and activated successfully."
else
    echo "Failed to create or activate virtual environment. Exiting."
    exit 1
fi

# Install required Python packages
echo "Installing required Python packages..."
pip install --upgrade pip --verbose
pip install vosk pyaudio PyQt6 --verbose

if [ $? -eq 0 ]; then
    echo "Required Python packages installed successfully."
else
    echo "Failed to install Python packages. Exiting."
    exit 1
fi

# Download and extract Vosk model
if [ ! -d "$MODEL_DIR" ]; then
    echo "Downloading Vosk model..."
    wget $MODEL_URL -O model.zip --verbose

    if [ $? -eq 0 ]; then
        echo "Vosk model downloaded successfully. Extracting..."
        unzip model.zip -d $MODEL_DIR
        rm model.zip
        echo "Vosk model extracted to $MODEL_DIR."
    else
        echo "Failed to download Vosk model. Exiting."
        exit 1
    fi
else
    echo "Vosk model already exists. Skipping download."
fi

# Create a requirements file for future use
echo "Generating requirements file..."
pip freeze > $REQUIREMENTS_FILE

if [ $? -eq 0 ]; then
    echo "Requirements file generated successfully."
else
    echo "Failed to generate requirements file. Exiting."
    exit 1
fi

echo "Setup completed successfully!"
echo "To activate the virtual environment, run: source $VENV_DIR/bin/activate"
echo "To start the application, use: python3 <your_script_name>.py"
