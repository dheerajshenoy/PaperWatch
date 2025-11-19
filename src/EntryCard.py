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
from PyQt6.QtCore import QUrl
from typing import Optional, List


class EntryCard(QWidget):
    def __init__(
        self,
        title: str,
        authors: List[str],
        date: str,
        pdf_url: Optional[str] = None,
        web_url: Optional[str] = None,
    ):
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
        # shadow_frame.setStyleSheet("background-color: white; border-radius: 10px;")
        shadow_layout = QVBoxLayout(shadow_frame)

        layout = QVBoxLayout(self)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")

        authors_label = QLabel(f"Authors: {', '.join(authors)}")
        authors_label.setStyleSheet("font-size: 13px;")

        date_label = QLabel(f"Published: {date}")
        date_label.setStyleSheet("font-size: 12px; color: #bbb;")

        btn_row = QHBoxLayout()
        pdf_btn = QPushButton("PDF")
        web_btn = QPushButton("Arxiv Page")

        pdf_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(pdf_url)))
        web_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(web_url)))

        btn_row.addWidget(pdf_btn)
        btn_row.addWidget(web_btn)
        btn_row.addStretch()

        shadow_layout.addWidget(title_label)
        shadow_layout.addWidget(authors_label)
        shadow_layout.addWidget(date_label)
        shadow_layout.addLayout(btn_row)

        # self.setLayout(shadow_layout)

        layout.addWidget(shadow_frame)

        # Apply shadow effect to frame only
        # shadow_effect = QGraphicsDropShadowEffect()
        # shadow_frame.setGraphicsEffect(shadow_effect)
