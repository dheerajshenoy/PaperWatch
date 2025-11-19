import feedparser

from PyQt6.QtNetwork import QNetworkReply, QNetworkRequest
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QUrl, Qt
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from EntryCard import EntryCard
from EntryInfoWidget import EntryInfoWidget
from Entry import Entry
import enum
from typing import List, overload, Union

from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QScrollArea,
    QWidget,
    QFrame,
    QStackedWidget,
)

from Statusbar import Statusbar

MAX_RESULTS_EACH = 30
SUBJECTS = ["astro-ph.CO", "cs.CV", "cs.LG", "cs.ML"]
KEYWORDS = ["CNN", "Machine Learning"]


class PaperWatchApp(QMainWindow):
    # Sort entries general function that sorts according to enum SortBy
    class SortBy(enum.Enum):
        DATE = 1
        TITLE = 2
        AUTHOR = 3

    def __init__(self):
        super().__init__()

        self.entries: feedparser.FeedParserDict = None  # Placeholder for paper entries

        self.setWindowTitle("PaperWatch")
        self.setGeometry(100, 100, 800, 600)
        # Additional UI setup can be done here

        self.initUI()

        # Fetch papers based on keywords, it should be title=keyword+OR+title=keyword
        parameters = "+AND+".join(f"ti:{keyword}" for keyword in KEYWORDS)

        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.on_page_response)

        # If you want to filter by subjects as well, uncomment the following lines
        # subject_filter = "+OR+".join(f"cat:{subject}" for subject in SUBJECTS)
        for subject in SUBJECTS:
            subject_filter = f"cat:{subject}"
            self.parameters = f"({parameters})+AND+({subject_filter})"
            self.method_name = "search_query"
            self.fetch_papers_async(
                self.method_name, self.parameters, max_results=MAX_RESULTS_EACH
            )

    def initUI(self):
        """Initialize the user interface."""
        self.menubar = self.menuBar()

        self.file_menu = self.menubar.addMenu("File")
        self.edit_menu = self.menubar.addMenu("Edit")
        self.view_menu = self.menubar.addMenu("View")
        self.help_menu = self.menubar.addMenu("Help")

        self.file_menu.addAction(
            "Refresh",
            lambda: self.fetch_papers_async(self.method_name, self.parameters),
        )
        self.file_menu.addAction("Exit", self.close)

        self.view_menu.addAction(
            "Sort by Date",
            lambda: self.sort_entries(self.SortBy.DATE),
            )

        self.view_menu.addAction(
            "Sort by Title",
            lambda: self.sort_entries(self.SortBy.TITLE),
            )

        self.view_menu.addAction(
            "Sort by Author",
            lambda: self.sort_entries(self.SortBy.AUTHOR),
            )

        self.layout = QVBoxLayout()
        self.statusbar = Statusbar(self)
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_widget.setLayout(self.layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll_area.setFrameStyle(QFrame.Shape.NoFrame)
        self.scroll_area.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_layout = QVBoxLayout()
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_area_widget)

        self.stacked_widget = QStackedWidget()
        self.entry_info_widget = EntryInfoWidget()

        self.entry_info_widget.backClicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.scroll_area)
        )

        self.layout.addWidget(self.stacked_widget)
        self.stacked_widget.addWidget(self.scroll_area)
        self.stacked_widget.addWidget(self.entry_info_widget)
        self.layout.addWidget(self.statusbar)

    def showPapers(self, papers: Union[feedparser.FeedParserDict, List[Entry]], remove_existing_entries = False) -> None:
        """
        Display fetched papers in the UI.
        """

        if remove_existing_entries:
            # Clear the children of scroll_layout
            for i in reversed(range(self.scroll_layout.count())):
                widget_to_remove = self.scroll_layout.itemAt(i).widget()
                self.scroll_layout.removeWidget(widget_to_remove)
                widget_to_remove.setParent(None)

        if isinstance(papers, list):
            self.entries = papers
        elif isinstance(papers, feedparser.FeedParserDict):
            self.entries = papers.entries

        for feed in self.entries:
            entry: Entry = Entry(feed)

            if entry.primary_category not in SUBJECTS:
                continue  # Skip this entry

            card = EntryCard(entry)
            card.entryClicked.connect(self.on_entry_clicked)
            self.scroll_layout.addWidget(card)

    def fetch_papers_async(
        self, method_name: str, parameters: str, max_results: int = MAX_RESULTS_EACH
    ):
        """
        Fetch papers asynchronously from arXiv API.
        """
        self.statusbar.set_message("Loading papers...", 0)
        url_template = "http://export.arxiv.org/api/query?{method_name}={parameters}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"

        url = f"{url_template.format(method_name=method_name, parameters=parameters, max_results=max_results)}"

        request = QNetworkRequest(QUrl(url))
        request.setAttribute(QNetworkRequest.Attribute.RedirectPolicyAttribute, True)
        self.manager.get(request)

    def on_page_response(self, reply: QNetworkReply):
        if reply.error() != QNetworkReply.NetworkError.NoError:
            raise ValueError("Error:", reply.errorString())
            return

        data = reply.readAll().data()
        feed = feedparser.parse(data)

        self.numPapers = len(feed.entries)
        self.statusbar.set_papers_count(self.numPapers)
        self.showPapers(feed, remove_existing_entries=True)
        self.statusbar.set_message("Papers loaded successfully.", 3000)

    def on_entry_clicked(self, entry: Entry):
        self.stacked_widget.setCurrentWidget(self.entry_info_widget)
        self.entry_info_widget.setEntryInfo(entry)

    # self.entries is an instance of Entry list
    def sort_entries(self, sort_by: SortBy):
        if self.entries is None:
            return

        if sort_by == self.SortBy.DATE:
            sorted_entries = sorted(
                self.entries, key=lambda e: e.published_parsed, reverse=True
            )
        elif sort_by == self.SortBy.TITLE:
            sorted_entries = sorted(self.entries, key=lambda e: e.title.lower())
        elif sort_by == self.SortBy.AUTHOR:
            sorted_entries = sorted(self.entries, key=lambda e: e.authors[0]["name"].lower())
        else:
            return

        self.showPapers(sorted_entries, True)
