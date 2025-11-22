from PyQt6.QtCore import QUrl, QObject, pyqtSignal
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


class DOI2Bib(QObject):
    bibtex_fetched = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.nam = QNetworkAccessManager()
        self.nam.finished.connect(self.handle_response)

    def fetch(self, doi: str):
        url = QUrl(f"https://doi.org/{doi}")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Accept", b"application/x-bibtex")
        self.nam.get(request)

    def handle_response(self, reply) -> str:
        """Handle the network reply and return the BibTeX string."""
        if reply.error() != QNetworkReply.NetworkError.NoError:
            print("Error:", reply.errorString())
            return ""
        self.bibtex_fetched.emit(reply.readAll().data().decode())
