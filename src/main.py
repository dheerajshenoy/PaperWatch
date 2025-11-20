import sys
from PyQt6.QtWidgets import QApplication
from PaperWatch import PaperWatchApp
from Config import load_config

if __name__ == "__main__":
    config = load_config("config.toml")
    app = QApplication(sys.argv)
    window = PaperWatchApp(config)
    window.show()
    sys.exit(app.exec())
