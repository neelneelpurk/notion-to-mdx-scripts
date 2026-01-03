"""
Notion Block Data Models

Comprehensive Pydantic models for all supported Notion block types.
Based on: https://developers.notion.com/reference/block
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Literal, Union

from pydantic import BaseModel, Field


# =============================================================================
# Enums
# =============================================================================

class NotionColor(str, Enum):
    """Notion text and background colors."""
    DEFAULT = "default"
    GRAY = "gray"
    BROWN = "brown"
    ORANGE = "orange"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    PURPLE = "purple"
    PINK = "pink"
    RED = "red"
    GRAY_BACKGROUND = "gray_background"
    BROWN_BACKGROUND = "brown_background"
    ORANGE_BACKGROUND = "orange_background"
    YELLOW_BACKGROUND = "yellow_background"
    GREEN_BACKGROUND = "green_background"
    BLUE_BACKGROUND = "blue_background"
    PURPLE_BACKGROUND = "purple_background"
    PINK_BACKGROUND = "pink_background"
    RED_BACKGROUND = "red_background"


# =============================================================================
# Shared / Base Models
# =============================================================================

class Annotations(BaseModel):
    """Text annotations for rich text."""
    bold: bool = False
    italic: bool = False
    strikethrough: bool = False
    underline: bool = False
    code: bool = False
    color: NotionColor = NotionColor.DEFAULT


class TextContent(BaseModel):
    """Text content with optional link."""
    content: str
    link: dict[str, str] | None = None


class MentionDate(BaseModel):
    """Date mention content."""
    start: str
    end: str | None = None
    time_zone: str | None = None



class Mention(BaseModel):
    """Mention object within rich text."""
    type: Literal["date", "link_preview"]
    date: MentionDate | None = None
    link_preview: dict[str, str] | None = None


class Equation(BaseModel):
    """Equation content (LaTeX expression)."""
    expression: str


class RichText(BaseModel):
    """Rich text object - the fundamental text unit in Notion."""
    type: Literal["text", "mention", "equation"]
    text: TextContent | None = None
    mention: Mention | None = None
    equation: Equation | None = None
    annotations: Annotations = Field(default_factory=Annotations)
    plain_text: str
    href: str | None = None


class PartialUser(BaseModel):
    """Partial user object."""
    object: Literal["user"] = "user"
    id: str


class Parent(BaseModel):
    """Parent object for blocks."""
    type: Literal["page_id", "block_id", "workspace", "database_id"]
    page_id: str | None = None
    block_id: str | None = None
    database_id: str | None = None
    workspace: bool | None = None


# =============================================================================
# File Objects
# =============================================================================

class ExternalFile(BaseModel):
    """External file reference."""
    url: str


class FileObject(BaseModel):
    """Generic file object (external, file, or file_upload)."""
    type: Literal["external", "file", "file_upload"]
    external: ExternalFile | None = None
    caption: list[RichText] = Field(default_factory=list)
    name: str | None = None


# =============================================================================
# Icon Objects
# =============================================================================

class EmojiIcon(BaseModel):
    """Emoji icon."""
    type: Literal["emoji"] = "emoji"
    emoji: str


class FileIcon(BaseModel):
    """File-based icon."""
    type: Literal["external", "file"]
    external: ExternalFile | None = None


Icon = EmojiIcon | FileIcon


# =============================================================================
# Block Content Types
# =============================================================================

class RichTextBlockContent(BaseModel):
    """Base content for blocks with rich text, color, and optional children."""
    rich_text: list[RichText] = Field(default_factory=list)
    color: NotionColor = NotionColor.DEFAULT
    children: list[Any] | None = None  # Forward ref handled by update_forward_refs


class ParagraphContent(RichTextBlockContent):
    """Paragraph block content."""
    pass


class HeadingContent(BaseModel):
    """Heading block content (h1, h2, h3)."""
    rich_text: list[RichText] = Field(default_factory=list)
    color: NotionColor = NotionColor.DEFAULT
    is_toggleable: bool = False


class BulletedListItemContent(RichTextBlockContent):
    """Bulleted list item content."""
    pass


class NumberedListItemContent(RichTextBlockContent):
    """Numbered list item content."""
    pass


class ToDoContent(RichTextBlockContent):
    """To-do block content."""
    checked: bool = False


class ToggleContent(RichTextBlockContent):
    """Toggle block content."""
    pass


class QuoteContent(RichTextBlockContent):
    """Quote block content."""
    pass


class CalloutContent(BaseModel):
    """Callout block content."""
    rich_text: list[RichText] = Field(default_factory=list)
    icon: Icon | None = None
    color: NotionColor = NotionColor.DEFAULT


class CodeContent(BaseModel):
    """Code block content."""
    rich_text: list[RichText] = Field(default_factory=list)
    caption: list[RichText] = Field(default_factory=list)
    language: str = "plain text"


class ChildPageContent(BaseModel):
    """Child page block content."""
    title: str


class ChildDatabaseContent(BaseModel):
    """Child database block content."""
    title: str


class EmbedContent(BaseModel):
    """Embed block content."""
    url: str


class BookmarkContent(BaseModel):
    """Bookmark block content."""
    url: str
    caption: list[RichText] = Field(default_factory=list)


class EquationContent(BaseModel):
    """Equation block content."""
    expression: str


class DividerContent(BaseModel):
    """Divider block content (empty)."""
    pass


class BreadcrumbContent(BaseModel):
    """Breadcrumb block content (empty)."""
    pass


class TableOfContentsContent(BaseModel):
    """Table of contents block content."""
    color: NotionColor = NotionColor.DEFAULT


class LinkPreviewContent(BaseModel):
    """Link preview block content."""
    url: str


class TableContent(BaseModel):
    """Table block content."""
    table_width: int
    has_column_header: bool = False
    has_row_header: bool = False


class TableRowContent(BaseModel):
    """Table row block content."""
    cells: list[list[RichText]] = Field(default_factory=list)


class ColumnListContent(BaseModel):
    """Column list block content (empty, children are columns)."""
    pass


class ColumnContent(BaseModel):
    """Column block content (empty, children are blocks)."""
    pass


# =============================================================================
# Block Base
# =============================================================================

class BlockBase(BaseModel):
    """Base class for all Notion blocks."""
    object: Literal["block"] = "block"
    id: str
    parent: Parent
    created_time: datetime
    last_edited_time: datetime
    created_by: PartialUser
    last_edited_by: PartialUser
    has_children: bool = False
    archived: bool = False
    in_trash: bool = False


# =============================================================================
# Concrete Block Types
# =============================================================================

class ParagraphBlock(BlockBase):
    type: Literal["paragraph"] = "paragraph"
    paragraph: ParagraphContent


class Heading1Block(BlockBase):
    type: Literal["heading_1"] = "heading_1"
    heading_1: HeadingContent


class Heading2Block(BlockBase):
    type: Literal["heading_2"] = "heading_2"
    heading_2: HeadingContent


class Heading3Block(BlockBase):
    type: Literal["heading_3"] = "heading_3"
    heading_3: HeadingContent


class BulletedListItemBlock(BlockBase):
    type: Literal["bulleted_list_item"] = "bulleted_list_item"
    bulleted_list_item: BulletedListItemContent


class NumberedListItemBlock(BlockBase):
    type: Literal["numbered_list_item"] = "numbered_list_item"
    numbered_list_item: NumberedListItemContent


class ToDoBlock(BlockBase):
    type: Literal["to_do"] = "to_do"
    to_do: ToDoContent


class ToggleBlock(BlockBase):
    type: Literal["toggle"] = "toggle"
    toggle: ToggleContent


class CodeBlock(BlockBase):
    type: Literal["code"] = "code"
    code: CodeContent


class ChildPageBlock(BlockBase):
    type: Literal["child_page"] = "child_page"
    child_page: ChildPageContent


class ChildDatabaseBlock(BlockBase):
    type: Literal["child_database"] = "child_database"
    child_database: ChildDatabaseContent


class EmbedBlock(BlockBase):
    type: Literal["embed"] = "embed"
    embed: EmbedContent


class ImageBlock(BlockBase):
    type: Literal["image"] = "image"
    image: FileObject


class VideoBlock(BlockBase):
    type: Literal["video"] = "video"
    video: FileObject


class FileBlock(BlockBase):
    type: Literal["file"] = "file"
    file: FileObject


class PdfBlock(BlockBase):
    type: Literal["pdf"] = "pdf"
    pdf: FileObject


class AudioBlock(BlockBase):
    type: Literal["audio"] = "audio"
    audio: FileObject


class BookmarkBlock(BlockBase):
    type: Literal["bookmark"] = "bookmark"
    bookmark: BookmarkContent


class CalloutBlock(BlockBase):
    type: Literal["callout"] = "callout"
    callout: CalloutContent


class QuoteBlock(BlockBase):
    type: Literal["quote"] = "quote"
    quote: QuoteContent


class EquationBlock(BlockBase):
    type: Literal["equation"] = "equation"
    equation: EquationContent


class DividerBlock(BlockBase):
    type: Literal["divider"] = "divider"
    divider: DividerContent = Field(default_factory=DividerContent)


class TableOfContentsBlock(BlockBase):
    type: Literal["table_of_contents"] = "table_of_contents"
    table_of_contents: TableOfContentsContent


class BreadcrumbBlock(BlockBase):
    type: Literal["breadcrumb"] = "breadcrumb"
    breadcrumb: BreadcrumbContent = Field(default_factory=BreadcrumbContent)


class ColumnListBlock(BlockBase):
    type: Literal["column_list"] = "column_list"
    column_list: ColumnListContent = Field(default_factory=ColumnListContent)


class ColumnBlock(BlockBase):
    type: Literal["column"] = "column"
    column: ColumnContent = Field(default_factory=ColumnContent)


class LinkPreviewBlock(BlockBase):
    type: Literal["link_preview"] = "link_preview"
    link_preview: LinkPreviewContent


class TableBlock(BlockBase):
    type: Literal["table"] = "table"
    table: TableContent


class TableRowBlock(BlockBase):
    type: Literal["table_row"] = "table_row"
    table_row: TableRowContent


class UnsupportedBlock(BlockBase):
    type: Literal["unsupported"] = "unsupported"


# =============================================================================
# Discriminated Union of All Blocks
# =============================================================================

Block = Annotated[
    Union[
        ParagraphBlock,
        Heading1Block,
        Heading2Block,
        Heading3Block,
        BulletedListItemBlock,
        NumberedListItemBlock,
        ToDoBlock,
        ToggleBlock,
        CodeBlock,
        ChildPageBlock,
        ChildDatabaseBlock,
        EmbedBlock,
        ImageBlock,
        VideoBlock,
        FileBlock,
        PdfBlock,
        AudioBlock,
        BookmarkBlock,
        CalloutBlock,
        QuoteBlock,
        EquationBlock,
        DividerBlock,
        TableOfContentsBlock,
        BreadcrumbBlock,
        ColumnListBlock,
        ColumnBlock,
        LinkPreviewBlock,
        TableBlock,
        TableRowBlock,
        UnsupportedBlock,
    ],
    Field(discriminator="type")
]


# =============================================================================
# API Response Models
# =============================================================================

class PageBlocksResponse(BaseModel):
    """Response from the Retrieve Block Children endpoint."""
    object: Literal["list"] = "list"
    results: list[Block]
    next_cursor: str | None = None
    has_more: bool = False
    type: Literal["block"] = "block"
    block: dict = Field(default_factory=dict)
    request_id: str | None = None

    # =========================================================================
    # Utility Methods
    # =========================================================================

    @staticmethod
    def _extract_plain_text(rich_text_list: list[RichText]) -> str:
        """Extract plain text from a list of rich text objects."""
        return "".join(rt.plain_text for rt in rich_text_list)

    @staticmethod
    def _get_block_text(block: Block) -> str:
        """Extract the main text content from a block."""
        block_type = block.type
        
        content_map = {
            "paragraph": lambda b: PageBlocksResponse._extract_plain_text(b.paragraph.rich_text),
            "heading_1": lambda b: PageBlocksResponse._extract_plain_text(b.heading_1.rich_text),
            "heading_2": lambda b: PageBlocksResponse._extract_plain_text(b.heading_2.rich_text),
            "heading_3": lambda b: PageBlocksResponse._extract_plain_text(b.heading_3.rich_text),
            "bulleted_list_item": lambda b: PageBlocksResponse._extract_plain_text(b.bulleted_list_item.rich_text),
            "numbered_list_item": lambda b: PageBlocksResponse._extract_plain_text(b.numbered_list_item.rich_text),
            "to_do": lambda b: PageBlocksResponse._extract_plain_text(b.to_do.rich_text),
            "toggle": lambda b: PageBlocksResponse._extract_plain_text(b.toggle.rich_text),
            "quote": lambda b: PageBlocksResponse._extract_plain_text(b.quote.rich_text),
            "callout": lambda b: PageBlocksResponse._extract_plain_text(b.callout.rich_text),
            "code": lambda b: PageBlocksResponse._extract_plain_text(b.code.rich_text),
            "child_page": lambda b: b.child_page.title,
            "child_database": lambda b: b.child_database.title,
            "equation": lambda b: b.equation.expression,
            "bookmark": lambda b: b.bookmark.url,
            "embed": lambda b: b.embed.url,
            "link_preview": lambda b: b.link_preview.url,
        }
        
        extractor = content_map.get(block_type)
        return extractor(block) if extractor else ""

    # =========================================================================
    # Markdown Conversion Methods
    # =========================================================================

    @staticmethod
    def _rich_text_to_markdown(rich_text_list: list[RichText]) -> str:
        """Convert a list of rich text objects to markdown string with formatting."""
        result = []
        
        for rt in rich_text_list:
            text = rt.plain_text
            annotations = rt.annotations
            
            # Apply formatting in order: code, bold, italic, strikethrough, underline
            if annotations.code:
                text = f"`{text}`"
            if annotations.bold:
                text = f"**{text}**"
            if annotations.italic:
                text = f"*{text}*"
            if annotations.strikethrough:
                text = f"~~{text}~~"
            # Underline has no standard markdown, skip or use HTML
            
            # Add link if present
            if rt.href:
                text = f"[{text}]({rt.href})"
            
            result.append(text)
        
        return "".join(result)

    @staticmethod
    def _block_to_markdown(block: Block, indent: int = 0, number: int | None = None) -> str:
        """Convert a single block to markdown string."""
        indent_str = "  " * indent
        block_type = block.type
        
        match block_type:
            case "paragraph":
                text = PageBlocksResponse._rich_text_to_markdown(block.paragraph.rich_text)
                return f"{indent_str}{text}\n" if text else "\n"
            
            case "heading_1":
                text = PageBlocksResponse._rich_text_to_markdown(block.heading_1.rich_text)
                return f"# {text}\n"
            
            case "heading_2":
                text = PageBlocksResponse._rich_text_to_markdown(block.heading_2.rich_text)
                return f"## {text}\n"
            
            case "heading_3":
                text = PageBlocksResponse._rich_text_to_markdown(block.heading_3.rich_text)
                return f"### {text}\n"
            
            case "bulleted_list_item":
                text = PageBlocksResponse._rich_text_to_markdown(block.bulleted_list_item.rich_text)
                return f"{indent_str}- {text}\n"
            
            case "numbered_list_item":
                text = PageBlocksResponse._rich_text_to_markdown(block.numbered_list_item.rich_text)
                num = number if number is not None else 1
                return f"{indent_str}{num}. {text}\n"
            
            case "to_do":
                text = PageBlocksResponse._rich_text_to_markdown(block.to_do.rich_text)
                checkbox = "[x]" if block.to_do.checked else "[ ]"
                return f"{indent_str}- {checkbox} {text}\n"
            
            case "toggle":
                text = PageBlocksResponse._rich_text_to_markdown(block.toggle.rich_text)
                return f"{indent_str}<details>\n{indent_str}<summary>{text}</summary>\n{indent_str}</details>\n"
            
            case "code":
                text = PageBlocksResponse._extract_plain_text(block.code.rich_text)
                lang = block.code.language.value if hasattr(block.code.language, 'value') else block.code.language
                return f"```{lang}\n{text}\n```\n"
            
            case "quote":
                text = PageBlocksResponse._rich_text_to_markdown(block.quote.rich_text)
                lines = text.split("\n")
                quoted = "\n".join(f"> {line}" for line in lines)
                return f"{quoted}\n"
            
            case "callout":
                text = PageBlocksResponse._rich_text_to_markdown(block.callout.rich_text)
                icon = ""
                if block.callout.icon:
                    if hasattr(block.callout.icon, 'emoji'):
                        icon = f"{block.callout.icon.emoji} "
                return f"> {icon}{text}\n"
            
            case "divider":
                return "---\n"
            
            case "equation":
                expr = block.equation.expression
                return f"$$\n{expr}\n$$\n"
            
            case "image":
                url = ""
                if block.image.external:
                    url = block.image.external.url
                caption = PageBlocksResponse._rich_text_to_markdown(block.image.caption) if block.image.caption else "image"
                return f"![{caption}]({url})\n"
            
            case "video":
                url = ""
                if block.video.external:
                    url = block.video.external.url
                return f"[Video]({url})\n"
            
            case "audio":
                url = ""
                if block.audio.external:
                    url = block.audio.external.url
                return f"[Audio]({url})\n"
            
            case "file":
                url = ""
                if block.file.external:
                    url = block.file.external.url
                name = block.file.name or "file"
                return f"[{name}]({url})\n"
            
            case "pdf":
                url = ""
                if block.pdf.external:
                    url = block.pdf.external.url
                return f"[PDF]({url})\n"
            
            case "bookmark":
                url = block.bookmark.url
                caption = PageBlocksResponse._rich_text_to_markdown(block.bookmark.caption) if block.bookmark.caption else url
                return f"[{caption}]({url})\n"
            
            case "embed":
                return f"[Embed]({block.embed.url})\n"
            
            case "link_preview":
                return f"[Link]({block.link_preview.url})\n"
            
            case "child_page":
                return f"📄 [{block.child_page.title}]()\n"
            
            case "child_database":
                return f"🗄️ [{block.child_database.title}]()\n"
            
            case "table_of_contents":
                return "[TOC]\n"
            
            case "breadcrumb":
                return ""  # Breadcrumbs don't render to markdown
            
            case "column_list" | "column":
                return ""  # Handled by children
            
            case "table":
                return ""  # Table header, rows handled separately
            
            case "table_row":
                cells = [PageBlocksResponse._rich_text_to_markdown(cell) for cell in block.table_row.cells]
                return "| " + " | ".join(cells) + " |\n"
            
            case _:
                return ""

    def to_markdown(self) -> str:
        """
        Convert the page blocks to a markdown string.
        
        Returns:
            A markdown string representation of all blocks
        """
        lines: list[str] = []
        numbered_list_counter = 0
        prev_type: str | None = None
        
        for block in self.results:
            block_type = block.type
            
            # Reset numbered list counter when leaving numbered list
            if block_type != "numbered_list_item" and prev_type == "numbered_list_item":
                numbered_list_counter = 0
            
            # Increment numbered list counter
            if block_type == "numbered_list_item":
                numbered_list_counter += 1
                md = self._block_to_markdown(block, number=numbered_list_counter)
            else:
                md = self._block_to_markdown(block)
            
            if md:
                lines.append(md)
            
            # Add blank line after certain block types for readability
            if block_type in ("heading_1", "heading_2", "heading_3", "paragraph", "quote", "callout", "code"):
                if block_type == "paragraph" and not self._get_block_text(block):
                    pass  # Don't add extra line after empty paragraph
                elif prev_type not in ("bulleted_list_item", "numbered_list_item", "to_do"):
                    pass  # Spacing already handled
            
            prev_type = block_type
        
        return "".join(lines)

    def get_plain_text(self) -> str:
        """
        Extract all plain text from the page blocks.
        
        Returns:
            A string containing all plain text content
        """
        texts = []
        for block in self.results:
            text = self._get_block_text(block)
            if text:
                texts.append(text)
        return "\n".join(texts)

    # =========================================================================
    # MDX Conversion Methods
    # =========================================================================

    @staticmethod
    def _wrap_with_color(text: str, color: str) -> str:
        """Wrap text with a color Span component if not default."""
        if color == "default" or not color:
            return text
        return f'<Span color="{color}">{text}</Span>'

    @staticmethod
    def _block_to_mdx(block: Block, indent: int = 0, number: int | None = None) -> str:
        """Convert a single block to MDX string with JSX components."""
        indent_str = "  " * indent
        block_type = block.type
        
        match block_type:
            case "paragraph":
                text = PageBlocksResponse._rich_text_to_markdown(block.paragraph.rich_text)
                color = block.paragraph.color.value if hasattr(block.paragraph.color, 'value') else block.paragraph.color
                if not text:
                    return "\n"
                text = PageBlocksResponse._wrap_with_color(text, color)
                return f"{indent_str}{text}\n"
            
            case "heading_1":
                text = PageBlocksResponse._rich_text_to_markdown(block.heading_1.rich_text)
                color = block.heading_1.color.value if hasattr(block.heading_1.color, 'value') else block.heading_1.color
                text = PageBlocksResponse._wrap_with_color(text, color)
                return f"# {text}\n"
            
            case "heading_2":
                text = PageBlocksResponse._rich_text_to_markdown(block.heading_2.rich_text)
                color = block.heading_2.color.value if hasattr(block.heading_2.color, 'value') else block.heading_2.color
                text = PageBlocksResponse._wrap_with_color(text, color)
                return f"## {text}\n"
            
            case "heading_3":
                text = PageBlocksResponse._rich_text_to_markdown(block.heading_3.rich_text)
                color = block.heading_3.color.value if hasattr(block.heading_3.color, 'value') else block.heading_3.color
                text = PageBlocksResponse._wrap_with_color(text, color)
                return f"### {text}\n"
            
            case "bulleted_list_item":
                text = PageBlocksResponse._rich_text_to_markdown(block.bulleted_list_item.rich_text)
                color = block.bulleted_list_item.color.value if hasattr(block.bulleted_list_item.color, 'value') else block.bulleted_list_item.color
                text = PageBlocksResponse._wrap_with_color(text, color)
                return f"{indent_str}- {text}\n"
            
            case "numbered_list_item":
                text = PageBlocksResponse._rich_text_to_markdown(block.numbered_list_item.rich_text)
                color = block.numbered_list_item.color.value if hasattr(block.numbered_list_item.color, 'value') else block.numbered_list_item.color
                text = PageBlocksResponse._wrap_with_color(text, color)
                num = number if number is not None else 1
                return f"{indent_str}{num}. {text}\n"
            
            case "to_do":
                text = PageBlocksResponse._rich_text_to_markdown(block.to_do.rich_text)
                color = block.to_do.color.value if hasattr(block.to_do.color, 'value') else block.to_do.color
                text = PageBlocksResponse._wrap_with_color(text, color)
                checkbox = "[x]" if block.to_do.checked else "[ ]"
                return f"{indent_str}- {checkbox} {text}\n"
            
            case "toggle":
                text = PageBlocksResponse._rich_text_to_markdown(block.toggle.rich_text)
                color = block.toggle.color.value if hasattr(block.toggle.color, 'value') else block.toggle.color
                return f'<Accordion title="{text}" color="{color}">\n</Accordion>\n'
            
            case "code":
                text = PageBlocksResponse._extract_plain_text(block.code.rich_text)
                lang = block.code.language
                return f"```{lang}\n{text}\n```\n"
            
            case "quote":
                text = PageBlocksResponse._rich_text_to_markdown(block.quote.rich_text)
                color = block.quote.color.value if hasattr(block.quote.color, 'value') else block.quote.color
                if color != "default":
                    return f'<Quote color="{color}">{text}</Quote>\n'
                lines = text.split("\n")
                quoted = "\n".join(f"> {line}" for line in lines)
                return f"{quoted}\n"
            
            case "callout":
                text = PageBlocksResponse._rich_text_to_markdown(block.callout.rich_text)
                color = block.callout.color.value if hasattr(block.callout.color, 'value') else block.callout.color
                icon = ""
                if block.callout.icon:
                    if hasattr(block.callout.icon, 'emoji'):
                        icon = block.callout.icon.emoji
                return f'<Callout icon="{icon}" color="{color}">\n  {text}\n</Callout>\n'
            
            case "divider":
                return "---\n"
            
            case "equation":
                expr = block.equation.expression
                return f"<Math>{expr}</Math>\n"
            
            case "image":
                url = ""
                if block.image.external:
                    url = block.image.external.url
                caption = PageBlocksResponse._rich_text_to_markdown(block.image.caption) if block.image.caption else ""
                if caption:
                    return f'<Image src="{url}" alt="{caption}" />\n'
                return f'<Image src="{url}" />\n'
            
            case "video":
                url = ""
                if block.video.external:
                    url = block.video.external.url
                return f'<Video src="{url}" />\n'
            
            case "audio":
                url = ""
                if block.audio.external:
                    url = block.audio.external.url
                return f'<Audio src="{url}" />\n'
            
            case "file":
                url = ""
                if block.file.external:
                    url = block.file.external.url
                name = block.file.name or "file"
                return f'<FileDownload href="{url}" name="{name}" />\n'
            
            case "pdf":
                url = ""
                if block.pdf.external:
                    url = block.pdf.external.url
                return f'<PDF src="{url}" />\n'
            
            case "bookmark":
                url = block.bookmark.url
                caption = PageBlocksResponse._rich_text_to_markdown(block.bookmark.caption) if block.bookmark.caption else url
                return f'<Bookmark url="{url}" title="{caption}" />\n'
            
            case "embed":
                return f'<Embed url="{block.embed.url}" />\n'
            
            case "link_preview":
                return f'<LinkPreview url="{block.link_preview.url}" />\n'
            
            case "child_page":
                return f'<ChildPage title="{block.child_page.title}" />\n'
            
            case "child_database":
                return f'<ChildDatabase title="{block.child_database.title}" />\n'
            
            case "table_of_contents":
                color = block.table_of_contents.color.value if hasattr(block.table_of_contents.color, 'value') else block.table_of_contents.color
                if color != "default":
                    return f'<TableOfContents color="{color}" />\n'
                return "<TableOfContents />\n"
            
            case "breadcrumb":
                return ""
            
            case "column_list" | "column":
                return ""
            
            case "table":
                return ""
            
            case "table_row":
                cells = [PageBlocksResponse._rich_text_to_markdown(cell) for cell in block.table_row.cells]
                return "| " + " | ".join(cells) + " |\n"
            
            case _:
                return ""

    def to_mdx(self) -> str:
        """
        Convert the page blocks to an MDX string with JSX components.
        
        MDX components used:
        - <Callout icon="...">content</Callout>
        - <Image src="..." alt="..." />
        - <Video src="..." />
        - <Audio src="..." />
        - <PDF src="..." />
        - <Embed url="..." />
        - <Bookmark url="..." title="..." />
        - <Accordion title="...">content</Accordion>
        - <Math>expression</Math>
        - <FileDownload href="..." name="..." />
        - <TableOfContents />
        - <ChildPage title="..." />
        - <ChildDatabase title="..." />
        - <LinkPreview url="..." />
        
        Returns:
            An MDX string representation of all blocks
        """
        lines: list[str] = []
        numbered_list_counter = 0
        prev_type: str | None = None
        
        for block in self.results:
            block_type = block.type
            
            # Reset numbered list counter when leaving numbered list
            if block_type != "numbered_list_item" and prev_type == "numbered_list_item":
                numbered_list_counter = 0
            
            # Increment numbered list counter
            if block_type == "numbered_list_item":
                numbered_list_counter += 1
                mdx = self._block_to_mdx(block, number=numbered_list_counter)
            else:
                mdx = self._block_to_mdx(block)
            
            if mdx:
                lines.append(mdx)
            
            prev_type = block_type
        
        return "".join(lines)
