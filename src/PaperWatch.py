import feedparser

from PyQt6.QtNetwork import QNetworkReply, QNetworkRequest
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QUrl, Qt
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from EntryCard import EntryCard

from PyQt6.QtWidgets import (
    QMainWindow,
    QScrollBar,
    QVBoxLayout,
    QScrollArea,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QHBoxLayout,
    QHeaderView,
    QSizePolicy,
)

MAX_RESULTS_EACH = 10
SUBJECTS = ["astro-ph.CO", "cs.CV", "cs.LG", "cs.ML"]
KEYWORDS = ["CNN", "Machine Learning"]


class PaperWatchApp(QMainWindow):
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

        # self.button.clicked.connect(self.fetch_papers_async)

        # If you want to filter by subjects as well, uncomment the following lines
        subject_filter = "+OR+".join(f"cat:{subject}" for subject in SUBJECTS)
        parameters = f"({parameters})+AND+({subject_filter})"
        self.fetch_papers_async(method_name="search_query", parameters=parameters)

    def initUI(self):
        """Initialize the user interface."""
        self.menubar = self.menuBar()

        self.file_menu = self.menubar.addMenu("File")
        self.edit_menu = self.menubar.addMenu("Edit")
        self.view_menu = self.menubar.addMenu("View")
        self.help_menu = self.menubar.addMenu("Help")

        self.layout = QHBoxLayout()
        self.statusbar = self.statusBar()
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_widget.setLayout(self.layout)
        self.leftPanel = QWidget()
        self.rightPanel = QWidget()
        # self.layout.addWidget(self.leftPanel)
        # self.layout.addWidget(self.rightPanel)
        self.menubar.show()
        # self.tableCols = 4  # Number of columns in the table
        # self.table: QTableWidget = QTableWidget(
        #     0, self.tableCols
        # )  # Placeholder for future table widget
        # self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        # self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        # self.table.setSortingEnabled(True)
        # # Set table headers label
        # self.table.setHorizontalHeaderLabels(
        #     ["Title", "Subject", "Authors", "Published"]
        # )
        #
        # # Expand first column section of the table to fill available space, also make it resizable
        #
        # self.table.horizontalHeader().setSectionResizeMode(
        #     0, QHeaderView.ResizeMode.Stretch
        # )
        #
        # for i in range(1, self.tableCols):
        #     self.table.horizontalHeader().setSectionResizeMode(
        #         i, QHeaderView.ResizeMode.Interactive
        #     )
        #
        # self.layout.addWidget(self.table)

        self.scroll_area = QScrollArea()
        # self.scroll_area.setVerticalScrollBarPolicy(
        #     Qt.ScrollBarPolicy.ScrollBarAlwaysOn
        # )
        self.scroll_area.setWidgetResizable(True)

        self.scroll_layout = QVBoxLayout()
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.layout.addWidget(self.scroll_area)

    def on_item_double_clicked(self, item: QTableWidgetItem):
        """
        Handle double-click event on table items.
        """
        row = item.row()
        title_item = self.table.item(row, 0)
        if title_item:
            # Handle the double-click event, e.g., open the paper link in a web browser, but even if entries are sorted
            # you can still access the original entry using self.entries[row]
            if self.entries and row < len(self.entries):
                entry = self.entries[row]
                # QDesktopServices.openUrl(QUrl(entry.link))

                # TODO: This is just a hack to open the PDF directly, improve it later
                QDesktopServices.openUrl(QUrl(entry.link.replace("abs", "pdf")))

    def showPapers(self, papers: feedparser.FeedParserDict) -> None:
        """
        Display fetched papers in the UI.
        """
        self.entries = papers.entries
        for entry in papers.entries:
            # title = QTableWidgetItem(entry.title)
            # authors = QTableWidgetItem(
            #     ", ".join(author.name for author in entry.authors)
            # )
            # published = QTableWidgetItem(entry.published_parsed)
            # published = QTableWidgetItem(entry.published)

            primary_category = (
                entry.arxiv_primary_category["term"]
                if "arxiv_primary_category" in entry
                else None
            )

            if primary_category not in SUBJECTS:
                continue  # Skip this entry

            card = EntryCard(
                entry.title,
                [author.name for author in entry.authors],
                entry.published,
                entry.link.replace("abs", "pdf"),
                entry.link,
            )

            self.scroll_layout.addWidget(card)

            # subject = QTableWidgetItem(entry.tags[0]["term"] if entry.tags else "DD")
            # self.table.insertRow(self.table.rowCount())
            #
            # self.table.setItem(self.table.rowCount() - 1, 0, title)
            # self.table.setItem(self.table.rowCount() - 1, 1, subject)
            # self.table.setItem(self.table.rowCount() - 1, 2, authors)
            # self.table.setItem(self.table.rowCount() - 1, 3, published)
            # Additional columns can be added for authors, published date, link, etc.

    def fetch_papers_async(self, method_name: str, parameters: str):
        """
        Fetch papers asynchronously from arXiv API.
        """
        self.statusbar.showMessage("Loading papers...", 0)
        url_template = "http://export.arxiv.org/api/query?{method_name}={parameters}&start=0&sortBy=submittedDate&sortOrder=descending"

        url = f"{url_template.format(method_name=method_name, parameters=parameters)}"

        request = QNetworkRequest(QUrl(url))
        request.setAttribute(QNetworkRequest.Attribute.RedirectPolicyAttribute, True)
        self.manager.get(request)

    @pyqtSlot(QNetworkReply)
    def on_page_response(self, reply: QNetworkReply):
        if reply.error() != QNetworkReply.NetworkError.NoError:
            raise ValueError("Error:", reply.errorString())
            return

        data = reply.readAll().data()
        feed = feedparser.parse(data)

        # Clear table
        # self.table.setRowCount(0)

        self.showPapers(feed)
        self.statusbar.showMessage("Papers loaded.", 2500)
        self.scroll_area.setContentsMargins(10, 10, 10, 10)
