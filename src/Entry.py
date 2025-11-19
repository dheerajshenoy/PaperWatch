# Entry class that has info about title, authors, published date, summary, link, and primary category, abstract etc.

import feedparser


class Entry:
    def __init__(
        self,
        feed: feedparser.FeedParserDict,
    ) -> None:
        self._title = feed.get("title", "No Title")
        self._authors = ", ".join(author["name"] for author in feed.get("authors", []))
        self._published = feed.get("published", "No Published Date")
        self._abstract = feed.get("summary", "No Abstract")
        self._link = feed.get("link", "No Link")
        self._primary_category = (
            feed.get("arxiv_primary_category", {}).get("term", "No Category")
            if "arxiv_primary_category" in feed
            else "No Category"
        )

    def __repr__(self) -> str:
        return f"Entry(title={self.title}, authors={self.authors}, published={self.published}, link={self.link}, primary_category={self.primary_category})"

# Getter only for all members as properties

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

