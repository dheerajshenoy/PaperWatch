from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
    QFrame,
)
from PyQt6.QtGui import QDesktopServices, QPalette, QColor
from PyQt6.QtCore import QUrl, pyqtSignal, Qt
from typing import Optional, List
from Entry import Entry


class Label(QLabel):
    """QLabel with text mouse copy support"""

    def __init__(self, text: str, parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)


class ActionText(Label):
    """
    A QLabel that looks like a hyperlink and can be clicked to perform an action. User can define the action by connecting to the clicked signal.
    """

    clicked = pyqtSignal()

    def __init__(self, text: str, parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def enterEvent(self, event):
        font = self.font()
        font.setUnderline(True)
        self.setFont(font)

    def leaveEvent(self, event):
        font = self.font()
        font.setUnderline(False)
        self.setFont(font)

    def mousePressEvent(self, event):
        self.clicked.emit()


class EntryCard(QWidget):
    entryClicked = pyqtSignal(object)  # Signal emitted when the card is clicked
    bookmarkEntryClicked = pyqtSignal(
        object
    )  # Signal emitted when bookmark button is clicked
    config = None  # Placeholder for config usage

    @classmethod
    def set_config(cls, config):
        cls.config = config

    def __init__(self, entry: Entry):
        super().__init__()

        self.entry = entry

        card_frame = QFrame(self)
        palette = card_frame.palette()
        border_color = palette.color(QPalette.ColorRole.Accent).name()

        # padding: 10px;  /* space inside the border */
        # border: 1px solid {border_color};
        card_frame.setStyleSheet(f"""
            QFrame {{
                border-radius: {self.config.ui.card.border_radius}px;
                background: palette(base); /* keeps theme correct */
            }}
        """)

        #
        # Outer layout (for this widget)
        #
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(card_frame)

        #
        # Layout inside the card border
        #
        layout = QVBoxLayout(card_frame)
        layout.setSpacing(6)

        #
        # Title
        #
        title_label = ActionText(entry.title)
        title_label.setWordWrap(True)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.clicked.connect(lambda: self.entryClicked.emit(entry))
        title_label.setVisible(self.config.ui.card.show_title)
        layout.addWidget(title_label)

        #
        # Tags
        #
        if self.config.ui.card.show_tags:
            tag_layout = QHBoxLayout()
            tag_background = palette.color(QPalette.ColorRole.Mid).name()
            for tag in entry.tags:
                tag_lbl = Label(tag)
                tag_lbl.setStyleSheet(f"""
                    background-color: {tag_background};
                    border-radius: 5px;
                    padding: 2px 5px;
                    font-size: 12px;
                """)
                tag_layout.addWidget(tag_lbl)
            tag_layout.addStretch()
            layout.addLayout(tag_layout)

        #
        # Authors
        #
        authors = entry.authors.split(", ")
        if len(authors) > self.config.ui.card.authors_truncate:
            authors = authors[: self.config.ui.card.authors_truncate] + ["et al."]
        authors_label = Label(", ".join(authors))
        authors_label.setStyleSheet("font-size: 13px; font-style: oblique;")
        authors_label.setVisible(self.config.ui.card.show_authors)
        layout.addWidget(authors_label)

        #
        # DOI
        #
        doi_label = Label(f"DOI: {entry.doi}")
        doi_label.setStyleSheet("font-size: 12px")
        doi_label.setVisible(self.config.ui.card.show_doi)
        layout.addWidget(doi_label)

        #
        # Bottom row
        #
        row = QHBoxLayout()

        date_label = Label(f"Published: {entry.published}")
        date_label.setStyleSheet("font-size: 12px")
        date_label.setVisible(self.config.ui.card.show_date)
        row.addWidget(date_label)

        row.addStretch()

        if self.config.ui.card.show_bookmark_button:
            self.bookmark_btn = QPushButton("Bookmark")
            self.bookmark_btn.clicked.connect(self._on_bookmark_clicked)
            row.addWidget(self.bookmark_btn)

        if self.config.ui.card.show_pdf_button:
            pdf_btn = QPushButton("PDF")
            pdf_btn.clicked.connect(
                lambda: QDesktopServices.openUrl(QUrl(entry.link.replace("abs", "pdf")))
            )
            row.addWidget(pdf_btn)

        if self.config.ui.card.show_webpage_button:
            web_btn = QPushButton("Arxiv Page")
            web_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(entry.link)))
            row.addWidget(web_btn)

        layout.setContentsMargins(10, 10, 10, 10)
        layout.addLayout(row)

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

    def entry(self) -> Entry:
        return self.entry

    def _on_bookmark_clicked(self):
        # Refresh the bookmark state
        self.setBookmarked(not self.bookmarked)
        self.bookmarkEntryClicked.emit(self.entry)
