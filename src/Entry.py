# Entry class that has info about title, authors, published date, summary, link, and primary category, abstract etc.

import feedparser
from typing import List


class Entry:
    def __init__(
        self,
        feed: feedparser.FeedParserDict,
    ) -> None:
        self._id: str = feed.get("id", "")
        self._title: str = feed.get("title", "")
        self._authors: str = ", ".join(
            author["name"] for author in feed.get("authors", [])
        )
        self._published: str = feed.get("published", "")
        self._abstract: str = feed.get("summary", "")
        self._link: str = feed.get("link", "")

        self._categories: List[str] = [tag["term"] for tag in feed.get("tags", [])]
        self._primary_category: str = (
            feed.get("arxiv_primary_category", {}).get("term", "")
            if "arxiv_primary_category" in feed
            else "No Category"
        )

        self._doi: str = feed.get("arxiv_doi", "")

    def __repr__(self) -> str:
        return f"Entry(title={self.title}, authors={self.authors}, published={self.published}, link={self.link}, primary_category={self.primary_category})"

    # Getter only for all members as properties

    @property
    def id(self) -> str:
        return self._id

    @property
    def doi(self) -> str:
        return self._doi

    @property
    def categories(self) -> str:
        return self._categories

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
            "categories": self.categories,
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
            "tags": [{"term": c} for c in data.get("categories", [])],
            "primary_category": {"term": data.get("primary_category", "")},
            "doi": data.get("doi", ""),
        }
        return cls(feed)
