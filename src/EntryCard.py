from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
    QFrame,
)
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl, pyqtSignal, Qt
from typing import Optional, List
from Entry import Entry


class ActionText(QLabel):
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

    def __init__(self, entry: Entry):
        super().__init__()

        # Frame that will have the shadow
        shadow_frame = QFrame()
        shadow_frame.setStyleSheet("""
            .QFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #ddd;
            }
        """)
        self.entry = entry
        shadow_layout = QVBoxLayout(shadow_frame)

        layout = QVBoxLayout(self)

        title_label = ActionText(entry.title)
        title_label.setWordWrap(True)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.clicked.connect(lambda: self.entryClicked.emit(self.entry))

        # Ellipsize long author lists

        # authors_label = QLabel(entry.authors)
        authors = entry.authors
        if len(authors) > 100:
            authors = authors[:100] + "..."
        authors_label = QLabel(authors)

        tag_layout = QHBoxLayout()

        for category in entry.categories:
            tag_label = QLabel(category)
            tag_label.setStyleSheet("""
                background-color: #eee;
                border-radius: 5px;
                padding: 2px 5px;
                font-size: 12px;
            """)
            tag_layout.addWidget(tag_label)

        tag_layout.addStretch()

        authors_label.setStyleSheet("font-size: 13px; font-style: oblique;")

        date_label = QLabel(f"Published: {entry.published}")
        date_label.setStyleSheet("font-size: 12px")

        btn_row = QHBoxLayout()
        pdf_btn = QPushButton("PDF")
        web_btn = QPushButton("Arxiv Page")

        link = entry.link
        pdf_btn.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(link.replace("abs", "pdf")))
        )
        web_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(link)))

        btn_row.addWidget(date_label)
        btn_row.addStretch()
        btn_row.addWidget(pdf_btn)
        btn_row.addWidget(web_btn)

        shadow_layout.addWidget(title_label)
        shadow_layout.addLayout(tag_layout)
        shadow_layout.addWidget(authors_label)
        shadow_layout.addLayout(btn_row)

        # self.setLayout(shadow_layout)

        layout.addWidget(shadow_frame)

        # Apply shadow effect to frame only
        # shadow_effect = QGraphicsDropShadowEffect()
        # shadow_frame.setGraphicsEffect(shadow_effect)

    # Mouse hover show pointer cursor
    # def enterEvent(self, event):
    #     self.setCursor(Qt.CursorShape.PointingHandCursor)
    #
    # def leaveEvent(self, event):
    #     self.setCursor(Qt.CursorShape.ArrowCursor)

    def entry(self) -> Entry:
        return self.entry

    # Handle click event and send signal called entryClicked
    # def mousePressEvent(self, event):
    #     self.entryClicked.emit(self.entry)
