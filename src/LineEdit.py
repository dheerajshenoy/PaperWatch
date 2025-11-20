# Custom QLineEdit implementation with resize_to_contents method

from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt

class LineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def resize_to_contents(self):
        """Resize the QLineEdit to fit its contents."""
        fm = self.fontMetrics()
        text_width = fm.horizontalAdvance(self.text()) + 10  # Add some padding
        self.setFixedWidth(text_width)
