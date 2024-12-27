#!/bin/bash

# This script sets up a Python virtual environment and installs the required dependencies for the speech-to-text application.
# It ensures that Vosk models are downloaded and placed in correct directories.

set -e  # Exit on error

# Define variables
REPO_URL="https://github.com/msn100001/stt.git"
CLONE_DIR="stt"
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
SCRIPT_NAME="stt.py"

# Language model URLs
declare -A MODEL_URLS
MODEL_URLS=(
    ["English"]="https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip"
    ["French"]="https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip"
    ["Spanish"]="https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip"
)

# Target directories for models
declare -A MODEL_DIRS
MODEL_DIRS=(
    ["English"]="model_en"
    ["French"]="model_fr"
    ["Spanish"]="model_es"
)

# Ask user for language selection
echo "Select language models to download:"
echo "1) English"
echo "2) French"
echo "3) Spanish"
echo "4) All"
read -rp "Enter your choice (1-4): " choice

case $choice in
    1)
        LANGUAGES=("English")
        ;;
    2)
        LANGUAGES=("French")
        ;;
    3)
        LANGUAGES=("Spanish")
        ;;
    4)
        LANGUAGES=("English" "French" "Spanish")
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac

# Clone the repository if not already cloned
if [ ! -d "$CLONE_DIR" ]; then
    echo "Cloning repository from $REPO_URL..."
    git clone $REPO_URL
else
    echo "Repository already cloned. Pulling latest changes..."
    cd $CLONE_DIR
    git pull
    cd ..
fi

# Navigate into the project directory
cd $CLONE_DIR

# Create and activate virtual environment
echo "Creating virtual environment..."
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

echo "Installing required Python packages..."
pip install --upgrade pip --verbose
pip install vosk pyaudio PyQt6 --verbose

# Download and extract selected language models
for lang in "${LANGUAGES[@]}"; do
    MODEL_DIR="${MODEL_DIRS[$lang]}"
    if [ ! -d "$MODEL_DIR" ]; then
        echo "Downloading $lang model..."
        wget "${MODEL_URLS[$lang]}" -O model.zip --verbose
        echo "Extracting $lang model..."
        mkdir -p "$MODEL_DIR"
        unzip -q model.zip
        mv vosk-model-small-*/* "$MODEL_DIR/" 2>/dev/null || mv vosk-model-small-*/*.* "$MODEL_DIR/"  # Handle variations in extraction structure
        rm -r vosk-model-small-* model.zip
        echo "$lang model extracted to $MODEL_DIR."
    else
        echo "$lang model already exists. Skipping download."
    fi
done

# Create a requirements file for future use
echo "Generating requirements file..."
pip freeze > $REQUIREMENTS_FILE

# Ensure the main script is executable
chmod +x $SCRIPT_NAME

echo "Setup completed successfully!"
echo "To activate the virtual environment, run: source $VENV_DIR/bin/activate"
echo "To start the application, use: python3 $SCRIPT_NAME"
