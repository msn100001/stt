# Speech-to-Text Application

## Overview
This is a real-time speech-to-text application that uses Python to transcribe spoken words into text. The application leverages the Vosk library for speech recognition and PyQt6 for its graphical user interface (GUI). This project is designed to support live transcription with features like number formatting and predictive text normalization.

## Features
- **Real-Time Speech Recognition:** Converts speech into text instantly.
- **Predictive Text Normalization:** Corrects common misspellings and enhances transcription quality.
- **Customizable Number Output:** Toggle between displaying numbers as words or numerals.
- **Keyword Recognition:** Highlights specific words like "taxed" in the output.
- **Interactive GUI:** Simple and intuitive interface built with PyQt6.

## Requirements
### System Requirements
- Python 3.6+
- Internet connection (for initial setup)
- Microphone

### Python Dependencies
- `vosk`
- `pyaudio`
- `PyQt6`

## Installation

### Clone the Repository
```bash
git clone git@github.com:msn100001/stt.git
cd stt
```

### Run the Setup Script
Use the provided setup script to automate the environment setup:
```bash
chmod +x stt_setup.sh
./stt_setup.sh
```
The script will:
1. Create a Python virtual environment.
2. Install the required Python dependencies.
3. Download and extract the Vosk model for speech recognition.
4. Generate a `requirements.txt` file for tracking dependencies.

### Activate the Virtual Environment
```bash
source venv/bin/activate
```

## Usage
### Run the Application
1. Ensure the virtual environment is active:
   ```bash
   source venv/bin/activate
   ```
2. Start the application:
   ```bash
   python3 stt.py
   ```

### Application Features
- **Start Listening:** Begin live transcription.
- **Stop Listening:** Halt the transcription process.
- **Clear Text:** Clear all transcribed text from the interface.
- **Toggle Numbers Format:** Switch between displaying numbers as numerals or words.

## Troubleshooting
- **PyAudio Installation Issues:**
   If you encounter errors with `pyaudio`, ensure you have the required development libraries:
   ```bash
   sudo apt-get install portaudio19-dev
   ```
- **Microphone Access Issues:**
   - Ensure the microphone is enabled and accessible by Python.
   - Test microphone functionality with other programs.
- **Vosk Model Download Failed:**
   Ensure you have an active internet connection when running the setup script.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [Vosk](https://alphacephei.com/vosk/) for the speech recognition library.
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/intro) for the GUI framework.

## Contact
For questions or support, open an issue on the [GitHub repository](https://github.com/msn100001/stt/issues).
