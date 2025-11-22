from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
    QFrame,
)
from PyQt6.QtGui import QDesktopServices, QPalette
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

        # Frame that will have the shadow
        shadow_frame = QFrame()
        shadow_frame.setStyleSheet(f"""
            .QFrame {{
                background-color: white;
                border: 1px solid #ddd;
                border-radius: {self.config.ui.card.border_radius}px;
                padding: 0;
            }}
            """)

        self.entry = entry
        shadow_layout = QVBoxLayout(shadow_frame)

        self.setContentsMargins(0, 0, 0, 0)
        layout = QVBoxLayout(self)

        title_label = ActionText(entry.title)
        title_label.setWordWrap(True)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.clicked.connect(lambda: self.entryClicked.emit(self.entry))

        # Ellipsize long author lists

        # authors_label = QLabel(entry.authors)
        authors = entry.authors.split(", ")
        truncate_at = self.config.ui.card.authors_truncate
        if len(authors) > truncate_at:
            authors = authors[:truncate_at]
            authors.append("et al.")
        authors = ", ".join(authors)
        authors_label = Label(authors)

        tag_layout = QHBoxLayout()

        for category in entry.categories:
            tag_label = Label(category)
            tag_label.setStyleSheet("""
                background-color: #eee;
                border-radius: 5px;
                padding: 2px 5px;
                font-size: 12px;
            """)
            tag_layout.addWidget(tag_label)

        tag_layout.addStretch()

        authors_label.setStyleSheet("font-size: 13px; font-style: oblique;")

        date_label = Label(f"Published: {entry.published}")
        date_label.setStyleSheet("font-size: 12px")

        doi_label = Label(f"DOI: {entry.doi}")
        doi_label.setStyleSheet("font-size: 12px")

        btn_row = QHBoxLayout()
        pdf_btn = QPushButton("PDF")
        web_btn = QPushButton("Arxiv Page")

        link = entry.link
        pdf_btn.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(link.replace("abs", "pdf")))
        )
        web_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(link)))

        self.bookmark_btn = QPushButton("Bookmark")
        self.bookmark_btn.clicked.connect(self._on_bookmark_clicked)

        if self.config.ui.card.show_date:
            btn_row.addWidget(date_label)

        btn_row.addStretch()

        if self.config.ui.card.show_bookmark_button:
            btn_row.addWidget(self.bookmark_btn)

        if self.config.ui.card.show_pdf_button:
            btn_row.addWidget(pdf_btn)

        if self.config.ui.card.show_webpage_button:
            btn_row.addWidget(web_btn)

        shadow_layout.addWidget(title_label)

        if self.config.ui.card.show_tags:
            shadow_layout.addLayout(tag_layout)
        shadow_layout.addWidget(authors_label)
        shadow_layout.addWidget(doi_label)
        shadow_layout.addLayout(btn_row)

        # self.setLayout(shadow_layout)

        layout.addWidget(shadow_frame)

        # Show/hide elements based on config
        title_label.setVisible(self.config.ui.card.show_title)
        date_label.setVisible(self.config.ui.card.show_date)
        authors_label.setVisible(self.config.ui.card.show_authors)
        doi_label.setVisible(self.config.ui.card.show_doi)

        # Apply shadow effect to frame only
        # shadow_effect = QGraphicsDropShadowEffect()
        # shadow_frame.setGraphicsEffect(shadow_effect)

    # Mouse hover show pointer cursor
    # def enterEvent(self, event):
    #     self.setCursor(Qt.CursorShape.PointingHandCursor)
    #
    # def leaveEvent(self, event):
    #     self.setCursor(Qt.CursorShape.ArrowCursor)

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
