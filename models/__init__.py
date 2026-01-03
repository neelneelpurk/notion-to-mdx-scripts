"""
NotionFlare Models

Pydantic models for Notion API responses.
"""

from .pageblocks import (
    PageBlocksResponse,
    Block,
    RichText,
    Annotations,
    NotionColor,
)

from .blogdatasource import (
    BlogDataSourceResponse,
    BlogPage,
    BlogProperties,
    SelectProperty,
    MultiSelectProperty,
    RichTextProperty,
    TitleProperty,
)

__all__ = [
    # Page Blocks
    "PageBlocksResponse",
    "Block",
    "RichText",
    "Annotations",
    "NotionColor",
    # Blog Data Source
    "BlogDataSourceResponse",
    "BlogPage",
    "BlogProperties",
    "SelectProperty",
    "MultiSelectProperty",
    "RichTextProperty",
    "TitleProperty",
]
