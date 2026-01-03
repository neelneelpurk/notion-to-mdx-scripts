"""
Datasource Task

Fetch pages from a Notion data source.
"""

from models.blogdatasource import BlogPage
from utils.notion import fetch_all_pages


def fetch_datasource_pages(data_source_id: str) -> list[BlogPage]:
    """
    Fetch all pages from a Notion data source.
    
    Args:
        data_source_id: The Notion data source ID
        
    Returns:
        List of BlogPage objects
    """
    return fetch_all_pages(data_source_id)
