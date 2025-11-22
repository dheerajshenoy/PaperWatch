# Use pydantic and toml to create a configuration class that loads settings from a TOML file.

from pydantic import BaseModel, Field, PositiveInt
import tomllib
from typing import Optional


class CardConfig(BaseModel):
    show_title: bool = True
    show_authors: bool = True
    authors_truncate: Optional[PositiveInt] = 5
    show_date: bool = True
    show_tags: bool = True
    show_doi: bool = True
    show_abstract: bool = False
    show_comments: bool = False
    show_bookmark_button: bool = True
    show_pdf_button: bool = True
    show_webpage_button: bool = True

    font_title: PositiveInt = 18
    font_authors: PositiveInt = 13
    font_meta: PositiveInt = 12

    max_width: PositiveInt = 600
    wrap_title: bool = True
    wrap_authors: bool = True

    shadow: bool = True
    border_radius: int = 0


# SIDE PANEL CONFIG


class SidePanelConfig(BaseModel):
    visible: bool = True
    width: PositiveInt = 300


# STATUSBAR CONFIG


class StatusbarConfig(BaseModel):
    visible: bool = True
    show_total_count: bool = True


# UI CONFIG


class UIConfig(BaseModel):
    side_panel: SidePanelConfig = SidePanelConfig()
    card: CardConfig = CardConfig()
    statusbar: StatusbarConfig = StatusbarConfig()


# TOP-LEVEL APP CONFIG


class ArxivConfig(BaseModel):
    # Give me sensible options for arXiv API
    max_results: PositiveInt = Field(
        50, description="Maximum number of results to fetch from arXiv API per query."
    )
    subjects: Optional[list[str]] = Field(
        None, description="List of arXiv subject categories to filter papers."
    )

    # Sorting by submittedDate, lastUpdatedDate, relevance, etc.
    sort_by: str = Field(
        "submittedDate", description="Sorting criteria for arXiv API results."
    )

    # Sorting order: ascending or descending
    sort_order: str = Field(
        "descending", description="Sorting order for arXiv API results."
    )

    keywords: Optional[list[str]] = Field(
        None, description="List of keywords to search for in paper titles."
    )

    doi_only: bool = Field(
        False, description="If true, only fetch papers that have a DOI."
    )


class AppConfig(BaseModel):
    arxiv: ArxivConfig = ArxivConfig()
    ui: UIConfig = UIConfig()


def load_config(file_path: str) -> ArxivConfig:
    return AppConfig(**tomllib.load(open(file_path, "rb")))
