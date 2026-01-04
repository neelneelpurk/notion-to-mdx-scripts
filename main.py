#!/usr/bin/env python3
"""
Notion to MDX Scripts - Main Entrypoint

GitHub Action entrypoint that fetches all pages from a Notion blog datasource
and converts them to MDX files.

Environment Variables:
    NOTION_API_KEY: Notion API key (required)
    BLOG_DATASOURCE_ID: Notion data source ID (required)
    OUTPUT_DIR: Directory to write MDX files (default: ./content)
"""

import json
import os
import sys

from dotenv import load_dotenv

# Load .env file for local development
load_dotenv()

from tasks import fetch_datasource_pages, convert_pages_to_mdx
from utils.notion import set_github_output


def main():
    # Get configuration from environment
    data_source_id = os.environ.get("BLOG_DATASOURCE_ID")
    output_dir = os.environ.get("OUTPUT_DIR", "./content")
    
    if not data_source_id:
        print("Error: BLOG_DATASOURCE_ID environment variable is required")
        sys.exit(1)
    
    print("Notion to MDX Scripts - Blog to MDX Converter")
    print("====================================")
    print(f"Data Source: {data_source_id}")
    print(f"Output Dir:  {output_dir}")
    print()
    
    # Step 1: Fetch all pages from data source
    print("Fetching pages from data source...")
    try:
        all_pages = fetch_datasource_pages(data_source_id)
        # Filter to only published pages
        pages = [p for p in all_pages if p.get_status() == "Publish"]
        print(f"Found {len(all_pages)} pages, {len(pages)} published\n")
    except Exception as e:
        print(f"Error fetching data source: {e}")
        sys.exit(1)
    
    # Step 2: Convert each page to MDX
    generated_files = convert_pages_to_mdx(pages, output_dir)
    
    # Set GitHub Actions outputs
    set_github_output("files", json.dumps(generated_files))
    set_github_output("file_count", str(len(generated_files)))
    
    # Summary
    print("====================================")
    print(f"Generated {len(generated_files)} MDX files")
    for f in generated_files:
        print(f"  ✓ {f}")


if __name__ == "__main__":
    main()
