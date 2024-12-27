
# Speech-to-Text Application (stt)

A real-time speech-to-text application that uses the Vosk speech recognition library and PyQt6 for an interactive graphical user interface. This project supports multiple languages, including English, French, and Spanish, and allows real-time transcription with customizable options.

---

## Features

- **Real-Time Speech Recognition**:
  - Transcribes audio input into text with minimal delay.
- **Multi-Language Support**:
  - Recognizes speech in English, French, and Spanish.
- **Intuitive GUI**:
  - User-friendly interface built with PyQt6.
- **Partial and Full Transcription**:
  - Displays partial transcription results in real-time.
- **Keyword Highlighting**:
  - Detects specific keywords (e.g., "taxed") and highlights them.
- **Language Selection**:
  - Easily switch between supported languages.
- **Text Management**:
  - Clear transcriptions with a single button.

---

## Prerequisites

- **Python**:
  - Python 3.8 or later is required.
- **Dependencies**:
  - `vosk`, `pyaudio`, and `PyQt6`.
- **Vosk Language Models**:
  - Pre-trained models for English, French, and Spanish.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone git@github.com:msn100001/stt.git
   cd stt
   ```

2. **Run the Setup Script**:
   ```bash
   ./stt_setup.sh
   ```

3. **Choose Language Models**:
   - During the setup, select the desired languages (English, French, Spanish, or all).
   - Models are downloaded and placed in their respective directories (`model_en`, `model_fr`, `model_es`).

4. **Activate the Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

---

## Usage

### Starting the Application
1. Ensure the virtual environment is activated:
   ```bash
   source venv/bin/activate
   ```

2. Run the application:
   ```bash
   python3 stt.py
   ```

### Features in the GUI
- **Start Listening**:
  - Begin transcription by clicking "🎙 Start Listening."
- **Stop Listening**:
  - Stop the transcription process with "🛑 Stop Listening."
- **Clear Text**:
  - Use "🧹 Clear Text" to clear the transcriptions.
- **Language Selection**:
  - Choose the desired language from the dropdown menu before starting.

---

## Directory Structure

```
stt/
├── model_en/           # English Vosk model
├── model_fr/           # French Vosk model
├── model_es/           # Spanish Vosk model
├── stt.py              # Main application script
├── stt_setup.sh        # Setup script
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

---

## Troubleshooting

### Common Issues
- **Audio Input Errors**:
  - Ensure your microphone is not in use by another application.
  - Check audio device permissions.

- **Model Not Found**:
  - Ensure that the language models are correctly placed in `model_en`, `model_fr`, and `model_es`.

- **ALSA or Jack Errors**:
  - Install `pulseaudio` to resolve sound system conflicts:
    ```bash
    sudo apt install pulseaudio
    ```

### Debugging
- Activate the virtual environment and re-run the setup script if issues persist:
  ```bash
  source venv/bin/activate
  ./stt_setup.sh
  ```

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributions

Contributions are welcome! Feel free to fork the repository and submit a pull request.

---

## Acknowledgments

- **Vosk**:
  - [Vosk Speech Recognition Toolkit](https://alphacephei.com/vosk/)
- **PyQt6**:
  - [PyQt6 Documentation](https://www.riverbankcomputing.com/software/pyqt/intro)
