#!/usr/bin/env python3
import pyaudio
import wave
import re
from vosk import Model, KaldiRecognizer
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QTextEdit, QWidget, QMessageBox
from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class SpeechRecognitionThread(QThread):
    recognized_text = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.is_running = True

    def run(self):
        try:
            model = Model("model")  # Ensure the "model" directory exists with a valid Vosk model
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

        self.button_toggle = QPushButton("🔄 Toggle Numbers Format", self)
        self.button_toggle.clicked.connect(self.toggle_numbers_format)
        layout.addWidget(self.button_toggle)

        # Indicator Label
        self.indicator_label = QLabel("", self)
        self.indicator_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.indicator_label.setStyleSheet("color: red; font-size: 16px;")
        layout.addWidget(self.indicator_label)

        # Speech Recognition Thread
        self.speech_thread = SpeechRecognitionThread()
        self.speech_thread.recognized_text.connect(self.update_textbox)

    def toggle_numbers_format(self):
        """Toggle the format of numbers between numerals and words."""
        self.show_as_numerals = not self.show_as_numerals
        format_type = "Numerals" if self.show_as_numerals else "Words"
        self.status_label.setText(f"Numbers will be displayed as {format_type}.")

    def words_to_numbers(self, text):
        """Convert spelled-out numbers to numerals, ensuring proper concatenation for large numbers."""
        number_words = {
            "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
            "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
            "ten": "10", "eleven": "11", "twelve": "12", "thirteen": "13",
            "fourteen": "14", "fifteen": "15", "sixteen": "16", "seventeen": "17",
            "eighteen": "18", "nineteen": "19", "twenty": "20", "thirty": "30",
            "forty": "40", "fifty": "50", "sixty": "60", "seventy": "70",
            "eighty": "80", "ninety": "90", "hundred": "100", "thousand": "1000",
            "million": "1000000", "billion": "1000000000", "trillion": "1000000000000",
            "point": ".", "plus": "+", "minus": "-", "times": "*", "divided": "/",
            "equals": "="
        }

        def replace_large_numbers(words):
            result = []
            i = 0
            while i < len(words):
                word = words[i].lower()
                if word in number_words:
                    num = number_words[word]
                    if i + 1 < len(words):
                        next_word = words[i + 1].lower()
                        if next_word in ["hundred", "thousand", "million", "billion", "trillion"]:
                            multiplier = int(number_words[next_word])
                            num = int(num) * multiplier
                            i += 1
                    result.append(str(num))
                else:
                    result.append(words[i])
                i += 1
            return result

        def format_numbers(text):
            words = text.split()
            converted_words = replace_large_numbers(words)
            formatted_text = " ".join(converted_words)
            return re.sub(r"(?<=\d)(?=(\d{3})+$)", ",", formatted_text)

        return format_numbers(text)

    def predictive_text_normalization(self, text):
        """Add predictive text normalization for context-aware replacements."""
        corrections = {
            "ther": "there",
            "recieve": "receive",
            "adress": "address",
            "seperate": "separate",
            "occurence": "occurrence"
        }

        def replace(match):
            return corrections[match.group(0).lower()]

        pattern = re.compile(r"\b(" + "|".join(re.escape(word) for word in corrections) + r")\b", re.IGNORECASE)
        return pattern.sub(replace, text)

    def normalize_text(self, text):
        """Normalize text by cleaning, formatting, and optionally converting numbers."""
        # Remove extra spaces and line breaks
        text = re.sub(r"\s+", " ", text.strip())
        # Replace non-alphanumeric characters except punctuation
        text = re.sub(r"[^\w\s.,!?'-]", "", text)

        if self.show_as_numerals:
            text = self.words_to_numbers(text)

        # Apply predictive text normalization
        text = self.predictive_text_normalization(text)

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

    def start_recognition(self):
        """Start speech recognition."""
        self.status_label.setText("Listening...")
        self.button_start.setEnabled(False)
        self.button_stop.setEnabled(True)

        if not self.speech_thread.isRunning():
            self.speech_thread.is_running = True  # Reset the running flag
            self.speech_thread.start()

    def stop_recognition(self):
        """Stop speech recognition."""
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

if __name__ == "__main__":
    app = QApplication([])
    window = RealTimeSpeechApp()
    window.show()
    app.exec()
