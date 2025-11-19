# Code for custom status bar in a GUI application using PyQt6
# Should have methods to set and clear messages with different levels of importance and timeouts
# Should also support a progress bar for long-running tasks
# Should also support showing current keywords activated and subjects being monitored
# Should show number of papers fetched or being processed

from PyQt6.QtWidgets import QStatusBar, QLabel, QProgressBar
from PyQt6.QtCore import Qt
from typing import List

class Statusbar(QStatusBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.message_label = QLabel("")
        self.addWidget(self.message_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.addPermanentWidget(self.progress_bar)

        self.keywords_label = QLabel("")
        self.addPermanentWidget(self.keywords_label)

        self.subjects_label = QLabel("")
        self.addPermanentWidget(self.subjects_label)

        self.num_papers_label = QLabel("")
        self.addPermanentWidget(self.num_papers_label)

        self.sort_label = QLabel("")
        self.addPermanentWidget(self.sort_label)

    def set_message(self, message: str, timeout: int = 5000):
        """Set a message in the status bar with an optional timeout."""
        self.showMessage(message, timeout)

    def clear_message(self):
        """Clear the current message in the status bar."""
        self.clearMessage()

    def start_progress(self, maximum: int):
        """Start a progress bar with a given maximum value."""
        self.progress_bar.setMaximum(maximum)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

    def update_progress(self, value: int):
        """Update the progress bar to a new value."""
        self.progress_bar.setValue(value)

    def stop_progress(self):
        """Stop and hide the progress bar."""
        self.progress_bar.setVisible(False)

    def set_keywords(self, keywords: List[str]):
        """Display the current keywords being monitored."""
        self.keywords_label.setText("Keywords: " + ", ".join(keywords))

    def set_subjects(self, subjects: List[str]):
        """Display the current subjects being monitored."""
        self.subjects_label.setText("Subjects: " + ", ".join(subjects))

    def set_papers_count(self, count: int):
        """Display the number of papers fetched or being processed."""
        self.num_papers_label.setText(f"Papers fetched: {count}")

    # Add sort indicator with a dedicated label
    def set_sort_indicator(self, sort_by: str, sort_order: str):
        """Display the current sorting method and order."""
        self.sort_label.setText(f"Sorted by: {sort_by} ({sort_order})")
