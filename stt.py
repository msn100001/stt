#!/usr/bin/env python3
import pyaudio
import wave
import re
from vosk import Model, KaldiRecognizer
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QTextEdit, QWidget, QMessageBox, QComboBox
)
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class SpeechRecognitionThread(QThread):
    recognized_text = pyqtSignal(str)

    def __init__(self, language_model):
        super().__init__()
        self.language_model = language_model
        self.is_running = True

    def run(self):
        try:
            model = Model(self.language_model)  # Load the selected language model
            recognizer = KaldiRecognizer(model, 16000)
            audio = pyaudio.PyAudio()

            stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=2048)
            stream.start_stream()

            while self.is_running:
                data = stream.read(2048, exception_on_overflow=False)
                if recognizer.AcceptWaveform(data):
                    result = recognizer.Result()
                    self.recognized_text.emit(result)
                else:
                    partial_result = recognizer.PartialResult()
                    self.recognized_text.emit(partial_result)

            # Stop the stream when thread is stopped
            stream.stop_stream()
            stream.close()
            audio.terminate()
        except Exception as e:
            self.recognized_text.emit(f"Error: {e}")

    def stop(self):
        self.is_running = False

class RealTimeSpeechApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Real-Time Speech Recognition")
        self.setGeometry(100, 100, 600, 500)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # State variable for number format
        self.show_as_numerals = True

        # Status Label
        self.status_label = QLabel("Click 'Start' to begin speech recognition.", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Recognized Text Box
        self.textbox = QTextEdit(self)
        self.textbox.setPlaceholderText("Recognized speech will appear here...")
        self.textbox.setReadOnly(True)
        layout.addWidget(self.textbox)

        # Partial Result Box
        self.partial_textbox = QTextEdit(self)
        self.partial_textbox.setPlaceholderText("Partial recognition will appear here...")
        self.partial_textbox.setReadOnly(True)
        layout.addWidget(self.partial_textbox)

        # Language Selection Dropdown
        self.language_dropdown = QComboBox(self)
        self.language_dropdown.addItems([
            "English", "Spanish", "French"
        ])
        layout.addWidget(self.language_dropdown)

        # Buttons
        self.button_start = QPushButton("🎙 Start Listening", self)
        self.button_start.clicked.connect(self.start_recognition)
        layout.addWidget(self.button_start)

        self.button_stop = QPushButton("🛑 Stop Listening", self)
        self.button_stop.clicked.connect(self.stop_recognition)
        self.button_stop.setEnabled(False)
        layout.addWidget(self.button_stop)

        self.button_clear = QPushButton("🧹 Clear Text", self)
        self.button_clear.clicked.connect(self.clear_text)
        layout.addWidget(self.button_clear)

        # Indicator Label
        self.indicator_label = QLabel("", self)
        self.indicator_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.indicator_label.setStyleSheet("color: red; font-size: 16px;")
        layout.addWidget(self.indicator_label)

        # Speech Recognition Thread
        self.speech_thread = None

    def get_language_model_path(self):
        """Retrieve the path to the model based on selected language."""
        language = self.language_dropdown.currentText()
        language_model_paths = {
            "English": "model_en",
            "Spanish": "model_es",
            "French": "model_fr"
        }
        return language_model_paths.get(language, "model_en")

    def start_recognition(self):
        """Start speech recognition."""
        self.status_label.setText("Listening...")
        self.button_start.setEnabled(False)
        self.button_stop.setEnabled(True)

        language_model_path = self.get_language_model_path()
        if not self.speech_thread or not self.speech_thread.isRunning():
            self.speech_thread = SpeechRecognitionThread(language_model_path)
            self.speech_thread.recognized_text.connect(self.update_textbox)
            self.speech_thread.is_running = True  # Reset the running flag
            self.speech_thread.start()

    def stop_recognition(self):
        """Stop speech recognition."""
        if self.speech_thread:
            self.speech_thread.stop()
            self.speech_thread.wait()  # Ensure the thread has stopped before proceeding
        self.status_label.setText("Speech recognition stopped.")
        self.button_start.setEnabled(True)
        self.button_stop.setEnabled(False)

    def clear_text(self):
        """Clear the recognized text from the textbox."""
        self.textbox.clear()
        self.partial_textbox.clear()
        self.indicator_label.setText("")

    def update_textbox(self, text):
        """Update the textbox with normalized recognized text."""
        if "partial" in text:
            self.partial_textbox.setText(text)
        else:
            normalized_text = self.normalize_text(text)
            self.textbox.append(normalized_text)
            self.partial_textbox.clear()

    def normalize_text(self, text):
        """Normalize text by cleaning, formatting, and optionally converting numbers."""
        # Remove extra spaces and line breaks
        text = re.sub(r"\s+", " ", text.strip())
        # Replace non-alphanumeric characters except punctuation
        text = re.sub(r"[^\w\s.,!?'-]", "", text)

        # Remove the word 'text' at the beginning of each line
        lines = text.split("\n")
        normalized_lines = []
        for line in lines:
            line = re.sub(r"^text\s*", "", line.lstrip())
            if "taxed" in line:
                self.indicator_label.setText("Keyword 'taxed' recognized!")
            else:
                self.indicator_label.setText("")
            normalized_lines.append(line)
        return "\n".join(normalized_lines)

if __name__ == "__main__":
    app = QApplication([])
    window = RealTimeSpeechApp()
    window.show()
    app.exec()
