import feedparser

from PyQt6.QtNetwork import QNetworkReply, QNetworkRequest
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QUrl, Qt
from PyQt6.QtGui import QDesktopServices, QAction, QActionGroup
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from EntryCard import EntryCard
from EntryInfoWidget import EntryInfoWidget
from Entry import Entry
import enum
from typing import List, overload, Union
from Config import AppConfig

from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QScrollArea,
    QWidget,
    QFrame,
    QStackedWidget,
)

from Statusbar import Statusbar


class PaperWatchApp(QMainWindow):
    # Sort entries general function that sorts according to enum SortBy
    class SortBy(enum.Enum):
        DATE = 1
        TITLE = 2
        AUTHOR = 3

    def __init__(self, config: AppConfig = None):
        super().__init__()

        self.config = config
        self.sort_by: self.SortBy = (
            self.config.arxiv.sort_by if self.config else self.SortBy.DATE
        )
        self.sort_order_ascending: bool = (
            self.config.arxiv.sort_order == "ascending" if self.config else False
        )
        self.entries: feedparser.FeedParserDict = None  # paper entries
        self.parameters: str = ""

        self.setWindowTitle("PaperWatch")
        self.setGeometry(100, 100, 800, 600)
        # Additional UI setup can be done here

        self.initUI()

        # Fetch papers based on keywords, it should be title=keyword+OR+title=keyword

        if self.config is not None:
            if self.config.arxiv.keywords:
                self.parameters = "+AND+".join(
                    f"ti:{keyword}" for keyword in self.config.arxiv.keywords
                )

            if self.config.arxiv.subjects:
                subject_filter = "+AND+".join(
                    f"all:{subject}" for subject in self.config.arxiv.subjects
                )

                if self.parameters != "":
                    self.parameters += f"+AND+({subject_filter})"

        self.method_name = "search_query"

        self._manager = QNetworkAccessManager()
        self._manager.finished.connect(self.on_page_response)

        if self.parameters != "":
            self.fetch_papers_async(
                self.method_name,
                self.parameters,
                max_results=self.config.arxiv.max_results,
            )

        self.sort_entries_by(self.SortBy.AUTHOR)

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

        # Add sorting options to view menu with exclusive selection with QActionGroup

        sort_group = QActionGroup(self)
        sort_by_date_action = QAction("Sort by Date", self, checkable=True)
        sort_by_title_action = QAction("Sort by Title", self, checkable=True)
        sort_by_author_action = QAction("Sort by Author", self, checkable=True)

        sort_group.addAction(sort_by_date_action)
        sort_group.addAction(sort_by_title_action)
        sort_group.addAction(sort_by_author_action)

        sort_by_date_action.triggered.connect(
            lambda: self.sort_entries_by(self.SortBy.DATE)
        )
        sort_by_title_action.triggered.connect(
            lambda: self.sort_entries_by(self.SortBy.TITLE)
        )
        sort_by_author_action.triggered.connect(
            lambda: self.sort_entries_by(self.SortBy.AUTHOR)
        )

        sort_by_author_action.setChecked(
            self.sort_by == self.SortBy.AUTHOR
        )
        sort_by_date_action.setChecked(
            self.sort_by == self.SortBy.DATE
        )
        sort_by_title_action.setChecked(
            self.sort_by == self.SortBy.TITLE
        )

        self.sort_by_menu = self.view_menu.addMenu("Sort By")

        self.sort_by_menu.addAction(sort_by_date_action)
        self.sort_by_menu.addAction(sort_by_title_action)
        self.sort_by_menu.addAction(sort_by_author_action)

        self.sort_order_menu = self.view_menu.addMenu("Sort Order")

        sort_order_group = QActionGroup(self)
        ascending_action = QAction("Ascending", self, checkable=True)
        descending_action = QAction("Descending", self, checkable=True)

        self.sort_order_menu.addAction(ascending_action)
        self.sort_order_menu.addAction(descending_action)

        ascending_action.setChecked(self.sort_order_ascending)
        descending_action.setChecked(not self.sort_order_ascending)

        sort_order_group.addAction(ascending_action)
        sort_order_group.addAction(descending_action)

        ascending_action.triggered.connect(
            lambda: self.sort_entries_by(self.sort_by)
        )

        descending_action.triggered.connect(
            lambda: self.sort_entries_by(self.sort_by)
        )

        # Main layout
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

    def showPapers(
        self,
        papers: Union[feedparser.FeedParserDict, List[Entry]],
        remove_existing_entries=False,
    ) -> None:
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

        subjects = self.config.arxiv.subjects if self.config else []

        for feed in self.entries:
            entry: Entry = Entry(feed)

            if subjects != [] and entry.primary_category not in subjects:
                continue  # Skip this entry

            card = EntryCard(entry)
            card.entryClicked.connect(self.on_entry_clicked)
            self.scroll_layout.addWidget(card)

    def fetch_papers_async(
        self, method_name: str, parameters: str, max_results: int = 10
    ):
        """
        Fetch papers asynchronously from arXiv API.
        """
        self.statusbar.set_message("Loading papers...", 0)
        url_template = "http://export.arxiv.org/api/query?{method_name}={parameters}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"

        url = f"{url_template.format(method_name=method_name, parameters=parameters, max_results=max_results)}"

        request = QNetworkRequest(QUrl(url))
        request.setAttribute(QNetworkRequest.Attribute.RedirectPolicyAttribute, True)
        self._manager.get(request)

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

    # Make this work with ascending/descending order
    def sort_entries_by(self, sort_by: SortBy):
        if self.entries is None:
            return

        self.sort_by = sort_by

        if self.sort_by == sort_by:
            self.sort_order_ascending = not self.sort_order_ascending
        else:
            self.sort_order_ascending = False  # Default to descending on new sort

        reverse = not self.sort_order_ascending

        if sort_by == self.SortBy.DATE:
            sorted_entries = sorted(self.entries, key=lambda e: e.published_parsed, reverse=reverse)

        elif sort_by == self.SortBy.TITLE:
            sorted_entries = sorted(self.entries, key=lambda e: e.title.lower(), reverse=reverse)

        elif sort_by == self.SortBy.AUTHOR:
            sorted_entries = sorted(self.entries, key=lambda e: e.authors[0]["name"].lower(), reverse=reverse)
        else:
            return

        self.statusbar.set_sort_indicator(
            sort_by.name, "Ascending" if self.sort_order_ascending else "Descending"
        )

        self.showPapers(sorted_entries, True)
