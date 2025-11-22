# PyQt6 Code for side panel that lists the pages user has subscribed

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QFrame,
)
from PyQt6.QtCore import Qt


class SidePanel(QWidget):
    def __init__(self, parent=None):
        super(SidePanel, self).__init__(parent)

        # Set up the layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # List widget to display subscribed pages
        self.page_list = QListWidget()
        self.layout.addWidget(self.page_list)

        self.setContentsMargins(0, 0, 0, 0)

    def add_page(self, page_name):
        """Add a new page to the subscribed list."""
        item = QListWidgetItem(page_name)
        self.page_list.addItem(item)

    def remove_page(self, page_name):
        """Remove a page from the subscribed list."""
        items = self.page_list.findItems(page_name, Qt.MatchFlag.MatchExactly)
        for item in items:
            row = self.page_list.row(item)
            self.page_list.takeItem(row)

    def clear_pages(self):
        """Clear all subscribed pages."""
        self.page_list.clear()
