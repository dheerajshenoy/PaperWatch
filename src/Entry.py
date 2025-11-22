# Entry class that has info about title, authors, published date, summary, link, and primary category, abstract etc.

import feedparser
from typing import List
import re
from datetime import datetime

def arxiv_to_doi(url: str) -> str:
    """Convert an arXiv abstract URL to a DOI link."""
    # match the identifier including version
    m = re.search(r'arxiv\.org/abs/([0-9]{4}\.[0-9]+)(v[0-9]+)?', url)
    if not m:
        raise ValueError(f"URL does not look like an arXiv abs link: {url}")
    arxiv_id = m.group(1)  # e.g., "2510.07692"
    doi = f"https://doi.org/10.48550/arXiv.{arxiv_id}"
    return doi


class Entry:
    def __init__(
        self,
        feed: feedparser.FeedParserDict,
    ):
        self._id: str = feed.get("id", "")
        self._title: str = feed.get("title", "")
        self._authors: str = ", ".join(
            author["name"] for author in feed.get("authors", [])
        )
        self._published: str = str(datetime.strptime(feed.get("published", ""), "%Y-%m-%dT%H:%M:%SZ"))
        self._abstract: str = feed.get("summary", "")
        self._link: str = feed.get("link", "")

        self._tags: List[str] = [tag["term"] for tag in feed.get("tags", [])]
        self._primary_category: str = (
            feed.get("arxiv_primary_category", {}).get("term", "")
            if "arxiv_primary_category" in feed
            else ""
        )

        # Handle DOI
        self._doi: str = feed.get("arxiv_doi", arxiv_to_doi(self._link))

    def __repr__(self) -> str:
        return f"Entry(title={self._title}, authors={self._authors}, published={self._published}, link={self._link}, primary_category={self._primary_category}, tags={self._tags})"

    # Getter only for all members as properties

    @property
    def id(self) -> str:
        return self._id

    @property
    def doi(self) -> str:
        return self._doi

    @property
    def tags(self) -> str:
        return self._tags

    @property
    def title(self) -> str:
        return self._title

    @property
    def authors(self) -> str:
        return self._authors

    @property
    def published(self) -> str:
        return self._published

    @property
    def abstract(self) -> str:
        return self._abstract

    @property
    def link(self) -> str:
        return self._link

    @property
    def primary_category(self) -> str:
        return self._primary_category

    # ------------------------
    # JSON SERIALIZATION
    # ------------------------
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors,
            "published": self.published,
            "abstract": self.abstract,
            "link": self.link,
            "tags": self.tags,
            "primary_category": self.primary_category,
            "doi": self.doi,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Entry":
        """
        Rebuild Entry object from stored dict.
        FeedParserDict isn't needed for deserialization.
        """
        if type(data) is not dict:
            return None

        feed = {
            "id": data.get("id", ""),
            "title": data.get("title", ""),
            "authors": [
                {"name": name.strip()}
                for name in data.get("authors", "").split(",")
                if name.strip()
            ],
            "published": data.get("published", ""),
            "summary": data.get("abstract", ""),
            "link": data.get("link", ""),
            "tags": [{"term": c} for c in data.get("tags", [])],
            "primary_category": {"term": data.get("primary_category", "")},
            "doi": data.get("doi", ""),
        }
        return cls(feed)
