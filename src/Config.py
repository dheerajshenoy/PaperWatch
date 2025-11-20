# Use pydantic and toml to create a configuration class that loads settings from a TOML file.

from pydantic import BaseModel, Field, PositiveInt
import toml
from typing import Optional
from pathlib import Path

# Config for paperwatch application

# ------------------------------
# CARD APPEARANCE + CONTENT
# ------------------------------


class CardShowConfig(BaseModel):
    show_authors: bool = True
    show_date: bool = True
    show_categories: bool = True
    show_doi: bool = True
    show_abstract: bool = False
    show_comments: bool = False


class CardFontConfig(BaseModel):
    title: PositiveInt = 18
    authors: PositiveInt = 13
    meta: PositiveInt = 12


class CardLayoutConfig(BaseModel):
    max_width: PositiveInt = 600
    wrap_title: bool = True
    wrap_authors: bool = True


class CardButtonConfig(BaseModel):
    pdf: bool = True
    arxiv: bool = True
    doi: bool = True


class CardStyleConfig(BaseModel):
    shadow: bool = True
    border_radius: PositiveInt = 10

    background_light: str = "#ffffff"
    background_dark: str = "#222222"

    text_light: str = "#000000"
    text_dark: str = "#cccccc"


# ------------------------------
# TOP-LEVEL UI CARD MODEL
# ------------------------------


class CardUIConfig(BaseModel):
    show: CardShowConfig = CardShowConfig()
    font: CardFontConfig = CardFontConfig()
    layout: CardLayoutConfig = CardLayoutConfig()
    buttons: CardButtonConfig = CardButtonConfig()
    style: CardStyleConfig = CardStyleConfig()


# ------------------------------
# TOP-LEVEL APP CONFIG
# ------------------------------


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


class AppConfig(BaseModel):
    arxiv: ArxivConfig = ArxivConfig()
    ui_card: CardUIConfig = CardUIConfig()

def load_config(file_path: str) -> ArxivConfig:
    config_data = toml.load(Path(file_path))
    return AppConfig(**config_data)
