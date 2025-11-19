# Entry info widget which shows detailed information like title, abstract about a selected entry.

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout)
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

        self.abstract_text = QLabel()
        self.abstract_text.setWordWrap(True)
        self.abstract_text.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        # self.abstract_text.setReadOnly(True)
        self.layout.addWidget(self.abstract_text)
        self.layout.addStretch()

        self.btn_layout = QHBoxLayout()

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.on_back_clicked)
        self.btn_layout.addWidget(self.back_button)

        self.btn_layout.addStretch()
        # Add pdf button and website button

        self.pdf_button = QPushButton("Open PDF")
        self.btn_layout.addWidget(self.pdf_button)

        self.website_button = QPushButton("Open Website")
        self.btn_layout.addWidget(self.website_button)


        self.layout.addLayout(self.btn_layout)


    def on_back_clicked(self):
        self.backClicked.emit()

    def setEntryInfo(self, entry: Entry):
        self.title_label.setText(entry.title)
        self.authors_label.setText(entry.authors)
        self.abstract_text.setText(entry.abstract)

