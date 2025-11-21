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
from PyQt6.QtGui import QFont, QDesktopServices, QPalette
from Entry import Entry
from LineEdit import LineEdit
from DOI2Bib import DOI2Bib
from Entry import Entry

class EntryInfoWidget(QWidget):
    backClicked = pyqtSignal()
    bookmarkClicked = pyqtSignal(Entry)

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
        self.doi_label.setFont(QFont("Arial", 10, QFont.Weight.Normal))
        self.doi_layout.addWidget(self.doi_label)
        self.doi_text_edit = LineEdit()
        self.doi2bib_btn = QPushButton("DOI to BibTeX")
        self.doi2bib_btn.clicked.connect(
            lambda: self.doi_fetcher.fetch(self.doi_text_edit.text())
        )

        self.doi_fetcher = DOI2Bib()

        self.doi_widget.hide()

        self.doi_text_edit.setReadOnly(True)
        self.doi_layout.addWidget(self.doi_text_edit)
        self.doi_layout.addWidget(self.doi2bib_btn)
        self.doi_layout.addStretch()

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.authors_label)
        self.layout.addWidget(self.abstract_text)
        self.layout.addWidget(self.doi_widget)

        self.layout.addStretch()

        self.btn_layout = QHBoxLayout()

        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.on_back_clicked)
        self.btn_layout.addWidget(self.back_btn)

        self.btn_layout.addStretch()
        # Add pdf button and website button

        self.bookmark_btn = QPushButton("Bookmark")
        self.bookmark_btn.clicked.connect(self.on_bookmark_clicked)
        self.btn_layout.addWidget(self.bookmark_btn)

        self.pdf_btn = QPushButton("PDF")
        self.pdf_btn.clicked.connect(self.on_pdf_open_clicked)
        self.btn_layout.addWidget(self.pdf_btn)

        self.website_btn = QPushButton("Webpage")
        self.website_btn.clicked.connect(self.on_website_open_clicked)
        self.btn_layout.addWidget(self.website_btn)

        self.layout.addLayout(self.btn_layout)

    def on_pdf_open_clicked(self):
        QDesktopServices.openUrl(QUrl(self.entry.link.replace("abs", "pdf")))

    def on_website_open_clicked(self):
        QDesktopServices.openUrl(QUrl(self.entry.link))

    def on_bookmark_clicked(self):
        self.setBookmarked(not self.bookmarked)
        self.bookmarkClicked.emit(self.entry)

    def on_back_clicked(self):
        self.backClicked.emit()

    def setEntryInfo(self, entry: Entry, bookmarked: bool = False):
        self.entry = entry
        self.title_label.setText(entry.title)
        self.authors_label.setText(entry.authors)
        self.abstract_text.setText(entry.abstract)
        self.setBookmarked(bookmarked)

    def setBookmarked(self, bookmarked: bool):
        self.bookmarked = bookmarked

        palette = self.bookmark_btn.palette()

        if bookmarked:
            self.bookmark_btn.setText("Bookmarked")

            # Use the system/theme highlight color
            bg = palette.color(QPalette.ColorRole.Highlight).name()
            text = palette.color(QPalette.ColorRole.HighlightedText).name()

            self.bookmark_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg};
                    color: {text};
                }}
            """)

        else:
            self.bookmark_btn.setText("Bookmark")
            # Default style palette

            bg = self.style().standardPalette().color(QPalette.ColorRole.Base).name()
            text = self.style().standardPalette().color(QPalette.ColorRole.Text).name()

            self.bookmark_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg};
                    color: {text};
                }}
                """)
