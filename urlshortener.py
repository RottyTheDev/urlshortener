import sys
import pyshorteners
import pyperclip
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt6.QtCore import QTimer
import requests

class URLShortener(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('URL Shortener')
        self.setFixedSize(400, 200)
        self.setStyleSheet("""
            QWidget {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QLineEdit {
                background-color: #34495e;
                border: 2px solid #3498db;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        layout = QVBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter URL to shorten")
        layout.addWidget(self.url_input)

        button_layout = QHBoxLayout()
        self.shorten_btn = QPushButton("Shorten")
        self.shorten_btn.clicked.connect(self.shorten_url)
        button_layout.addWidget(self.shorten_btn)

        self.copy_btn = QPushButton("Copy")
        self.copy_btn.clicked.connect(self.copy_to_clipboard)
        self.copy_btn.setEnabled(False)
        button_layout.addWidget(self.copy_btn)

        layout.addLayout(button_layout)

        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def shorten_url(self):
        long_url = self.url_input.text()
        if long_url:
            try:
                s = pyshorteners.Shortener()
                short_url = s.tinyurl.short(long_url)
                self.result_label.setText(short_url)
                self.copy_btn.setEnabled(True)
                self.animate_label()
            except requests.exceptions.RequestException as e:
                self.result_label.setText(f"Error: {str(e)}")
            except Exception as e:
                self.result_label.setText(f"Unexpected error: {str(e)}")
        else:
            self.result_label.setText("Please enter a URL")

    def copy_to_clipboard(self):
        pyperclip.copy(self.result_label.text())
        self.result_label.setText("Copied to clipboard!")
        self.animate_label()

    def animate_label(self):
        original_pos = self.result_label.pos()
        
        def move_up():
            self.result_label.move(original_pos.x(), original_pos.y() - 20)
        
        def move_down():
            self.result_label.move(original_pos.x(), original_pos.y())
        
        # Move up
        QTimer.singleShot(0, move_up)
        
        # Move down after 500ms
        QTimer.singleShot(500, move_down)

# ... (keep the rest of the code)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = URLShortener()
    ex.show()
    sys.exit(app.exec())