from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QStackedWidget,
    QLabel,
    QSpinBox,
    QMessageBox,
    QCheckBox,
    QComboBox,
    QListWidget,
    QPushButton,
    QListWidgetItem,
    QInputDialog,
)
from PyQt6.QtCore import Qt
from Config import AppConfig, CardConfig, StatusbarConfig
import tomli_w

class ConfigEditorWidget(QWidget):
    def __init__(self, config: AppConfig):
        super().__init__()
        self.config: AppConfig = config

        layout = QHBoxLayout(self)

        # Left side: tree
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        layout.addWidget(self.tree, 0)

        # Right side: stacked pages
        self.pages = QStackedWidget()
        layout.addWidget(self.pages, 1)

        # Create all pages
        self._make_arxiv_page()
        # self._make_bookmark_page()  # optional if you implement bookmarks
        self._make_side_panel_page()
        self._make_card_page()
        self._make_statusbar_page()

        # Tree mapping
        self._populate_tree()
        self.tree.currentItemChanged.connect(self._change_page)

        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setFixedSize(600, 800)
        self.show()

    # ---------------------------------------------
    def _populate_tree(self):
        mapping = {"arxiv": 0, "ui.side_panel": 1, "ui.card": 2, "ui.statusbar": 3}
        for key, idx in mapping.items():
            item = QTreeWidgetItem([key])
            item.setData(0, Qt.ItemDataRole.UserRole, idx)
            self.tree.addTopLevelItem(item)
        self.tree.setCurrentItem(self.tree.topLevelItem(0))

    def _change_page(self, item):
        idx = item.data(0, Qt.ItemDataRole.UserRole)
        self.pages.setCurrentIndex(idx)

    def _add_save_button(self, layout: QVBoxLayout):
        save_btn = QPushButton("Save configuration")
        save_btn.clicked.connect(self._save_config)
        layout.addWidget(save_btn)

    # =============================================
    # ARXIV PAGE
    # =============================================
    def _make_arxiv_page(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        self.max_results = QSpinBox()
        self.max_results.setRange(1, 10000)
        self.max_results.setValue(self.config.arxiv.max_results)
        layout.addWidget(QLabel("Max results"))
        layout.addWidget(self.max_results)

        layout.addWidget(QLabel("Subjects"))
        self.subjects = QListWidget()
        for s in self.config.arxiv.subjects or []:
            QListWidgetItem(s, self.subjects)
        layout.addWidget(self.subjects)

        add_btn = QPushButton("Add subject")
        add_btn.clicked.connect(self._add_subject)
        layout.addWidget(add_btn)

        self.doi_only = QCheckBox("Only papers with DOI")
        self.doi_only.setChecked(self.config.arxiv.doi_only)
        layout.addWidget(self.doi_only)

        layout.addWidget(QLabel("Sort by"))
        self.sort_by = QComboBox()
        self.sort_by.addItems(["submittedDate", "updatedDate", "relevance"])
        self.sort_by.setCurrentText(self.config.arxiv.sort_by)
        layout.addWidget(self.sort_by)

        layout.addWidget(QLabel("Sort order"))
        self.sort_order = QComboBox()
        self.sort_order.addItems(["ascending", "descending"])
        self.sort_order.setCurrentText(self.config.arxiv.sort_order)
        layout.addWidget(self.sort_order)

        layout.addStretch()
        self.pages.addWidget(w)

        self._add_save_button(layout)

    def _save_config(self):
        """Save current GUI config to TOML file."""
        if not self.config.file_path:
            return  # No path provided

        updated_config = self.get_config()  # Get updated AppConfig
        with open(self.config.file_path, "wb") as f:
            print(tomli_w.dumps(updated_config()).encode("utf-8"))
        QMessageBox.information(self, "Saved", "Configuration saved successfully.")

    def _add_subject(self):
        text, ok = QInputDialog.getText(self, "Add subject", "Enter subject:")
        if ok and text.strip():
            QListWidgetItem(text.strip(), self.subjects)

    # =============================================
    # SIDE PANEL
    # =============================================
    def _make_side_panel_page(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        self.side_visible = QCheckBox("Side panel visible")
        self.side_visible.setChecked(self.config.ui.side_panel.visible)
        layout.addWidget(self.side_visible)

        layout.addWidget(QLabel("Width"))
        self.side_width = QSpinBox()
        self.side_width.setRange(100, 1000)
        self.side_width.setValue(self.config.ui.side_panel.width)
        layout.addWidget(self.side_width)

        layout.addStretch()
        self.pages.addWidget(w)

        self._add_save_button(layout)

    # =============================================
    # CARD PAGE
    # =============================================
    def _make_card_page(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        c: CardConfig = self.config.ui.card

        def add_checkbox(label: str, value: bool):
            cb = QCheckBox(label)
            cb.setChecked(value)
            layout.addWidget(cb)
            return cb

        layout.addWidget(QLabel("Spacing"))
        self.card_spacing = QSpinBox()
        self.card_spacing.setRange(0, 50)
        self.card_spacing.setValue(c.spacing)
        layout.addWidget(self.card_spacing)

        self.card_show_title = add_checkbox("Show title", c.show_title)
        self.card_show_authors = add_checkbox("Show authors", c.show_authors)

        layout.addWidget(QLabel("Max authors"))
        self.card_authors_trunc = QSpinBox()
        self.card_authors_trunc.setRange(1, 20)
        self.card_authors_trunc.setValue(c.authors_truncate or 5)
        layout.addWidget(self.card_authors_trunc)

        self.card_show_date = add_checkbox("Show date", c.show_date)
        self.card_show_tags = add_checkbox("Show tags", c.show_tags)
        self.card_show_doi = add_checkbox("Show DOI", c.show_doi)
        self.card_show_abstract = add_checkbox("Show abstract", c.show_abstract)
        self.card_show_comments = add_checkbox("Show comments", c.show_comments)
        self.card_show_bookmark = add_checkbox(
            "Show bookmark button", c.show_bookmark_button
        )
        self.card_show_pdf = add_checkbox("Show PDF button", c.show_pdf_button)
        self.card_show_web = add_checkbox("Show webpage button", c.show_webpage_button)

        layout.addWidget(QLabel("Border radius"))
        self.card_radius = QSpinBox()
        self.card_radius.setRange(0, 40)
        self.card_radius.setValue(c.border_radius)
        layout.addWidget(self.card_radius)

        layout.addStretch()
        self.pages.addWidget(w)

        self._add_save_button(layout)

    # =============================================
    # STATUSBAR PAGE
    # =============================================
    def _make_statusbar_page(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        s: StatusbarConfig = self.config.ui.statusbar

        self.status_visible = QCheckBox("Show status bar")
        self.status_visible.setChecked(s.visible)
        layout.addWidget(self.status_visible)

        self.status_total = QCheckBox("Show total count")
        self.status_total.setChecked(s.show_total_count)
        layout.addWidget(self.status_total)

        layout.addStretch()
        self.pages.addWidget(w)

        self._add_save_button(layout)

    # =============================================
    # GET CONFIG BACK
    # =============================================
    def get_config(self) -> AppConfig:
        """Return updated AppConfig instance from GUI"""
        c = self.config
        # ARXIV
        c.arxiv.max_results = self.max_results.value()
        c.arxiv.subjects = [
            self.subjects.item(i).text() for i in range(self.subjects.count())
        ]
        c.arxiv.doi_only = self.doi_only.isChecked()
        c.arxiv.sort_by = self.sort_by.currentText()
        c.arxiv.sort_order = self.sort_order.currentText()

        # SIDE PANEL
        c.ui.side_panel.visible = self.side_visible.isChecked()
        c.ui.side_panel.width = self.side_width.value()

        # CARD
        card: CardConfig = c.ui.card
        card.spacing = self.card_spacing.value()
        card.show_title = self.card_show_title.isChecked()
        card.show_authors = self.card_show_authors.isChecked()
        card.authors_truncate = self.card_authors_trunc.value()
        card.show_date = self.card_show_date.isChecked()
        card.show_tags = self.card_show_tags.isChecked()
        card.show_doi = self.card_show_doi.isChecked()
        card.show_abstract = self.card_show_abstract.isChecked()
        card.show_comments = self.card_show_comments.isChecked()
        card.show_bookmark_button = self.card_show_bookmark.isChecked()
        card.show_pdf_button = self.card_show_pdf.isChecked()
        card.show_webpage_button = self.card_show_web.isChecked()
        card.border_radius = self.card_radius.value()

        # STATUSBAR
        s: StatusbarConfig = c.ui.statusbar
        s.visible = self.status_visible.isChecked()
        s.show_total_count = self.status_total.isChecked()

        return c
