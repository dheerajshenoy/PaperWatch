# Entry info widget which shows detailed information like title, abstract about a selected entry.

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
)
from PyQt6.QtCore import pyqtSignal, Qt, QUrl
from PyQt6.QtGui import QFont, QDesktopServices
from Entry import Entry


class EntryInfoWidget(QWidget):
    backClicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.title_label = QLabel("Title")
        self.title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.title_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.authors_label = QLabel("Authors")
        self.authors_label.setWordWrap(True)
        self.authors_label.setFont(QFont("Arial", 12, QFont.Weight.Normal))
        self.authors_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.abstract_text = QLabel()
        self.abstract_text.setWordWrap(True)
        self.abstract_text.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.abstract_text.setFont(QFont("Arial", 11, QFont.Weight.Normal))

        self.doi_widget = QWidget()
        self.doi_layout = QHBoxLayout()
        self.doi_widget.setLayout(self.doi_layout)

        self.doi_label = QLabel("DOI:")
        self.doi_label.setFont(QFont("Arial", 10, QFont.Weight.Normal
                                     ))
        self.doi_layout.addWidget(self.doi_label)
        self.doi_text_edit = QLineEdit()
        # Make it so that the QLineEdit expands to size of the content
        self.doi_text_edit.setMinimumWidth(400)

        self.doi_widget.hide()

        self.doi_text_edit.setReadOnly(True)
        self.doi_layout.addWidget(self.doi_text_edit)
        self.doi_layout.addStretch()

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.authors_label)
        self.layout.addWidget(self.abstract_text)
        self.layout.addWidget(self.doi_widget)

        self.layout.addStretch()

        self.btn_layout = QHBoxLayout()

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.on_back_clicked)
        self.btn_layout.addWidget(self.back_button)

        self.btn_layout.addStretch()
        # Add pdf button and website button

        self.pdf_button = QPushButton("PDF")
        self.pdf_button.clicked.connect(self.on_pdf_open_clicked)
        self.btn_layout.addWidget(self.pdf_button)

        self.website_button = QPushButton("Webpage")
        self.website_button.clicked.connect(self.on_website_open_clicked)
        self.btn_layout.addWidget(self.website_button)

        self.layout.addLayout(self.btn_layout)

    def on_pdf_open_clicked(self):
        QDesktopServices.openUrl(QUrl(self.link.replace("abs", "pdf")))

    def on_website_open_clicked(self):
        QDesktopServices.openUrl(QUrl(self.link))

    def on_back_clicked(self):
        self.backClicked.emit()

    def setEntryInfo(self, entry: Entry):
        self.link = entry.link
        self.title_label.setText(entry.title)
        self.authors_label.setText(entry.authors)
        self.abstract_text.setText(entry.abstract)
        if entry.doi != "":
            self.doi_widget.show()
            self.doi_text_edit.setText(entry.doi)
