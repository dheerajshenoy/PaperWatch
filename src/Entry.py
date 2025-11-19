# Entry class that has info about title, authors, published date, summary, link, and primary category, abstract etc.

import feedparser


class Entry:
    def __init__(
        self,
        feed: feedparser.FeedParserDict,
    ) -> None:
        self._title = feed.get("title", "")
        self._authors = ", ".join(author["name"] for author in feed.get("authors", []))
        self._published = feed.get("published", "")
        self._abstract = feed.get("summary", "")
        self._link = feed.get("link", "")

        self._categories = [tag["term"] for tag in feed.get("tags", [])]
        self._primary_category = (
            feed.get("arxiv_primary_category", {}).get("term", "")
            if "arxiv_primary_category" in feed
            else "No Category"
        )

        self._doi = feed.get("arxiv_doi", "")

    def __repr__(self) -> str:
        return f"Entry(title={self.title}, authors={self.authors}, published={self.published}, link={self.link}, primary_category={self.primary_category})"

# Getter only for all members as properties

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

