"""
Blog Data Source Models

Pydantic models for Notion data source query responses (blog pages).
"""

from __future__ import annotations
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from .pageblocks import RichText, EmojiIcon, FileIcon


# =============================================================================
# Property Types
# =============================================================================

class SelectOption(BaseModel):
    """A select option value."""
    id: str
    name: str
    color: str


class SelectProperty(BaseModel):
    """Select property type."""
    id: str
    type: Literal["select"] = "select"
    select: SelectOption | None = None


class MultiSelectProperty(BaseModel):
    """Multi-select property type."""
    id: str
    type: Literal["multi_select"] = "multi_select"
    multi_select: list[SelectOption] = Field(default_factory=list)


class RichTextProperty(BaseModel):
    """Rich text property type."""
    id: str
    type: Literal["rich_text"] = "rich_text"
    rich_text: list[RichText] = Field(default_factory=list)


class TitleProperty(BaseModel):
    """Title property type."""
    id: str
    type: Literal["title"] = "title"
    title: list[RichText] = Field(default_factory=list)


class LastEditedTimeProperty(BaseModel):
    """Last edited time property type."""
    id: str
    type: Literal["last_edited_time"] = "last_edited_time"
    last_edited_time: datetime


# =============================================================================
# Blog Page Properties
# =============================================================================

class BlogProperties(BaseModel):
    """Properties specific to a blog page."""
    Status: SelectProperty
    Tags: MultiSelectProperty
    Slug: RichTextProperty
    Description: RichTextProperty
    Type: SelectProperty
    Name: TitleProperty

    # Optional: Last Edited Time may have different casing
    class Config:
        populate_by_name = True


# =============================================================================
# Parent Types
# =============================================================================

class DataSourceParent(BaseModel):
    """Parent reference for data source pages."""
    type: Literal["data_source_id"] = "data_source_id"
    data_source_id: str
    database_id: str


# =============================================================================
# Blog Page
# =============================================================================

class PartialUser(BaseModel):
    """Partial user reference."""
    object: Literal["user"] = "user"
    id: str


Icon = EmojiIcon | FileIcon | None


class BlogPage(BaseModel):
    """A blog page from the data source query."""
    object: Literal["page"] = "page"
    id: str
    created_time: datetime
    last_edited_time: datetime
    created_by: PartialUser
    last_edited_by: PartialUser
    cover: dict | None = None
    icon: Icon = None
    parent: DataSourceParent
    archived: bool = False
    in_trash: bool = False
    is_locked: bool = False
    properties: BlogProperties
    url: str
    public_url: str | None = None

    # =========================================================================
    # Convenience Methods
    # =========================================================================

    def get_title(self) -> str:
        """Get the blog title as plain text."""
        return "".join(rt.plain_text for rt in self.properties.Name.title)

    def get_slug(self) -> str:
        """Get the blog slug as plain text."""
        return "".join(rt.plain_text for rt in self.properties.Slug.rich_text)

    def get_description(self) -> str:
        """Get the blog description as plain text."""
        return "".join(rt.plain_text for rt in self.properties.Description.rich_text)

    def get_status(self) -> str | None:
        """Get the blog status name."""
        return self.properties.Status.select.name if self.properties.Status.select else None

    def get_tags(self) -> list[str]:
        """Get the blog tags as a list of strings."""
        return [tag.name for tag in self.properties.Tags.multi_select]

    def get_type(self) -> str | None:
        """Get the blog type name."""
        return self.properties.Type.select.name if self.properties.Type.select else None

    def get_notion_page_id(self) -> str | None:
        """Get the notion page id."""
        return self.url.split("-")[-1]



# =============================================================================
# Query Response
# =============================================================================

class BlogDataSourceResponse(BaseModel):
    """Response from querying a blog data source."""
    object: Literal["list"] = "list"
    results: list[BlogPage]
    next_cursor: str | None = None
    has_more: bool = False
    type: Literal["page_or_data_source"] = "page_or_data_source"
    page_or_data_source: dict = Field(default_factory=dict)
    request_id: str | None = None

    def __iter__(self):
        """Iterate over blog pages."""
        return iter(self.results)

    def __len__(self):
        """Return number of blog pages."""
        return len(self.results)
