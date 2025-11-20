import json
from pathlib import Path
from typing import List, overload
from Entry import Entry


class BookmarkManager:
    def __init__(self, json_path: str):
        self._path = Path(json_path)
        self._id_index: set[str] = set()
        self._bookmarks: List[Entry] = []
        self._load()

    # -----------------------------
    # Persistence
    # -----------------------------
    def _load(self):
        if not self._path.exists():
            self._bookmarks = []
            return

        try:
            raw = json.loads(self._path.read_text())
            self._bookmarks = [Entry.from_dict(item) for item in raw]
        except Exception:
            # Don’t silently corrupt data; just reset and move on.
            self._bookmarks = []
        self._build_index()

    def _build_index(self):
        """Builds indices for fast lookup."""
        self._id_index = {e.id for e in self._bookmarks}

    def _save(self):
        raw = [entry.to_dict() for entry in self._bookmarks]
        self._path.write_text(json.dumps(raw, indent=2))

    # -----------------------------
    # Operations
    # -----------------------------
    def add(self, entry: Entry):
        # Avoid duplicates by id (best unique IDs for arXiv items)
        if any(e.id == entry.id for e in self._bookmarks):
            return

        self._bookmarks.append(entry)
        self._build_index()
        self._save()

    def remove(self, id: str):
        before = len(self._bookmarks)
        self._bookmarks = [e for e in self._bookmarks if e.id != id]

        if len(self._bookmarks) != before:
            self._save()
        self._build_index()

    def list_all(self) -> List[Entry]:
        return list(self._bookmarks)

    def clear(self):
        self._bookmarks = []
        self._save()
        self._id_index.clear()

    def is_bookmarked(self, entry: Entry) -> bool:
        """Check if an entry is already bookmarked by ID."""
        return entry.id in self._id_index
