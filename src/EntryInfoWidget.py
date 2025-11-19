# Entry info widget which shows detailed information like title, abstract about a selected entry.

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont
from Entry import Entry

class EntryInfoWidget(QWidget):
    backClicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel("Title")
        self.title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.layout.addWidget(self.title_label)

        self.authors_label = QLabel("Authors")
        self.authors_label.setFont(QFont("Arial", 12, QFont.Weight.Normal))
        self.layout.addWidget(self.authors_label)

        self.abstract_text = QTextEdit()
        self.abstract_text.setReadOnly(True)
        self.layout.addWidget(self.abstract_text)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.on_back_clicked)
        self.layout.addWidget(self.back_button)

    def on_back_clicked(self):
        self.backClicked.emit()

    def setEntryInfo(self, entry: Entry):
        self.title_label.setText(entry.title)
        self.authors_label.setText(entry.authors)
        self.abstract_text.setPlainText(entry.abstract)

