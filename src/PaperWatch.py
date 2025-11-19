import feedparser
import urllib3
import certifi

from PyQt6.QtWidgets import (
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHBoxLayout,
    QHeaderView,
)


class PaperWatchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PaperWatch")
        self.setGeometry(100, 100, 800, 600)
        # Additional UI setup can be done here

        self.initUI()
        papers = self.fetch_papers(method_name="query", parameters="search_query=CNN")
        self.showPapers(papers)

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
        self.layout.addWidget(self.leftPanel)
        self.menubar.show()
        self.table: QTableWidget = QTableWidget(0, 3)  # Placeholder for future table widget
        self.layout.addWidget(self.table)

        # Set table headers label
        self.table.setHorizontalHeaderLabels(["Title", "Authors", "Published"])

        # Expand first column section of the table to fill available space
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)

    def showPapers(self, papers):
        """
        Display fetched papers in the UI.
        """
        # for entry in papers.entries:
        #     print(f"Title: {entry.title}")
        #     print(f"Authors: {', '.join(author.name for author in entry.authors)}")
        #     print(f"Published: {entry.published}")
        #     print(f"Link: {entry.link}")
        #     print("-" * 40)
        # Add entries to the table self.table
        self.table.setColumnCount(3)
        for entry in papers.entries:
            self.table.insertRow(self.table.rowCount())
            title = QTableWidgetItem(entry.title)
            authors = QTableWidgetItem(
                ", ".join(author.name for author in entry.authors)
            )
            published = QTableWidgetItem(entry.published)
            self.table.setItem(self.table.rowCount() - 1, 0, title)
            self.table.setItem(self.table.rowCount() - 1, 1, authors)
            self.table.setItem(self.table.rowCount() - 1, 2, published)
            # Additional columns can be added for authors, published date, link, etc.

    def fetch_papers(
        self, method_name: str, parameters: str
    ) -> feedparser.FeedParserDict:
        """
        Fetch papers from arXiv API.
        """
        # Create a PoolManager (handles connections)
        http = urllib3.PoolManager(
            cert_reqs="CERT_REQUIRED",  # enforce SSL certificate verification
            ca_certs=certifi.where(),  # use certifi CA bundle
        )

        url_template = "http://export.arxiv.org/api/{method_name}?{parameters}"
        # url = 'http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=1'

        # Google Chrome User-Agent string (example from latest Chrome)
        chrome_ua = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/118.0.5993.90 Safari/537.36"
        )

        url = f"{url_template.format(method_name=method_name, parameters=parameters)}"
        # Make GET request with Chrome User-Agent
        response = http.request("GET", url, headers={"User-Agent": chrome_ua})

        return feedparser.parse(response.data)
