"""
Notion API Utilities

Shared functions for interacting with the Notion API.
"""

import os
from functools import lru_cache

import requests

from models.blogdatasource import BlogDataSourceResponse
from models.pageblocks import PageBlocksResponse


@lru_cache()
def get_notion_headers() -> tuple[tuple[str, str], ...]:
    """Get headers for Notion API requests (cached, returns tuple for hashability)."""
    api_key = os.environ.get("NOTION_API_KEY")
    if not api_key:
        raise ValueError("NOTION_API_KEY environment variable is required")
    
    return (
        ("Authorization", f"Bearer {api_key}"),
        ("Notion-Version", "2025-09-03"),
        ("Content-Type", "application/json"),
    )


def _headers_dict() -> dict[str, str]:
    """Convert cached headers to dict."""
    return dict(get_notion_headers())


# =============================================================================
# Data Source API
# =============================================================================

def query_data_source(data_source_id: str, cursor: str | None = None) -> BlogDataSourceResponse:
    """Query a Notion data source."""
    url = f"https://api.notion.com/v1/data_sources/{data_source_id}/query"
    
    payload = {}
    if cursor:
        payload["start_cursor"] = cursor
    
    response = requests.post(url, headers=_headers_dict(), json=payload)
    response.raise_for_status()
    
    return BlogDataSourceResponse.model_validate(response.json())


def fetch_all_pages(data_source_id: str) -> list:
    """Fetch all pages from a data source, handling pagination."""
    all_pages = []
    cursor = None
    
    while True:
        response = query_data_source(data_source_id, cursor)
        all_pages.extend(response.results)
        
        if not response.has_more:
            break
        cursor = response.next_cursor
    
    return all_pages


# =============================================================================
# Block API
# =============================================================================

def get_block_children(block_id: str, cursor: str | None = None) -> PageBlocksResponse:
    """Fetch block children from Notion API."""
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"
    
    params = {}
    if cursor:
        params["start_cursor"] = cursor
    
    response = requests.get(url, headers=_headers_dict(), params=params)
    response.raise_for_status()
    
    return PageBlocksResponse.model_validate(response.json())


def fetch_all_blocks(page_id: str) -> PageBlocksResponse:
    """Fetch all blocks from a page, handling pagination."""
    all_results = []
    cursor = None
    first_response = None
    
    while True:
        response = get_block_children(page_id, cursor)
        
        if first_response is None:
            first_response = response
        
        all_results.extend(response.results)
        
        if not response.has_more:
            break
        cursor = response.next_cursor
    
    if first_response:
        first_response.results = all_results
        first_response.has_more = False
        first_response.next_cursor = None
    
    return first_response


# =============================================================================
# Utilities
# =============================================================================

def sanitize_filename(name: str) -> str:
    """Convert a title to a safe filename."""
    safe = name.lower().replace(" ", "-")
    safe = "".join(c for c in safe if c.isalnum() or c in "-_")
    while "--" in safe:
        safe = safe.replace("--", "-")
    return safe.strip("-") or "untitled"


def set_github_output(name: str, value: str):
    """Set a GitHub Actions output variable."""
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"{name}={value}\n")
    else:
        print(f"::set-output name={name}::{value}")
