
import sys
from PyQt6.QtWidgets import QApplication
from PaperWatch import PaperWatchApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaperWatchApp()
    window.show()
    sys.exit(app.exec())
