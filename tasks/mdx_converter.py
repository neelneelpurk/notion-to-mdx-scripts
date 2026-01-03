"""
MDX Converter Task

Convert Notion pages to MDX files.
"""

import json
from pathlib import Path

from models.blogdatasource import BlogPage
from utils.notion import fetch_all_blocks, sanitize_filename


def convert_page_to_mdx(page: BlogPage, output_dir: Path) -> str | None:
    """
    Convert a single Notion page to MDX.
    
    Args:
        page: The BlogPage to convert
        output_dir: Directory to write the MDX file
        
    Returns:
        Path to the generated file, or None on error
    """
    title = page.get_title()
    slug = page.get_slug()
    status = page.get_status()
    page_id = page.get_notion_page_id()
    
    try:
        # Fetch blocks
        blocks_response = fetch_all_blocks(page_id)
        
        # Convert to MDX
        content = blocks_response.to_mdx()
        
        # Generate filename from slug or title
        filename = (slug or sanitize_filename(title)) + ".mdx"
        file_path = output_dir / filename
        
        # Get tags, description, type
        tags = page.get_tags()
        tags_yaml = json.dumps(tags)  # Format as JSON array for YAML
        description = page.get_description()
        page_type = page.get_type() or ""
        
        # Build frontmatter
        frontmatter = f'''---
title: "{title}"
slug: "{slug}"
description: "{description}"
type: "{page_type}"
status: "{status}"
tags: {tags_yaml}
last_edited: "{page.last_edited_time.isoformat()}"
---

'''
        # Write file
        file_path.write_text(frontmatter + content, encoding="utf-8")
        
        return str(file_path)
        
    except Exception as e:
        print(f"  Error converting page {title}: {e}")
        return None


def convert_pages_to_mdx(pages: list[BlogPage], output_dir: str = "./content") -> list[str]:
    """
    Convert multiple Notion pages to MDX files.
    
    Args:
        pages: List of BlogPage objects to convert
        output_dir: Directory to write MDX files
        
    Returns:
        List of generated file paths
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    generated_files = []
    
    for page in pages:
        print(f"Processing: {page.get_title()}")
        print(f"  Status: {page.get_status()}, Slug: {page.get_slug()}")
        
        file_path = convert_page_to_mdx(page, output_path)
        
        if file_path:
            print(f"  Written: {file_path}")
            generated_files.append(file_path)
        
        print()
    
    return generated_files
