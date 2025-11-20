from PyQt6.QtCore import QUrl, QObject
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest


class DOI2Bib(QObject):
    def __init__(self):
        super().__init__()
        self.nam = QNetworkAccessManager()
        self.nam.finished.connect(self.handle_response)

    def fetch(self, doi: str):
        url = QUrl(f"https://doi.org/{doi}")
        request = QNetworkRequest(url)
        request.setRawHeader(b"Accept", b"application/x-bibtex")
        self.nam.get(request)

    def handle_response(self, reply):
        if reply.error():
            print("Error:", reply.errorString())
            return
        bibtex = reply.readAll().data().decode()
        print(bibtex)
