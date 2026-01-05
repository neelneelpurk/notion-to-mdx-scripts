# 📝 Notion to MDX Scripts

[![GitHub license](https://img.shields.io/github/license/neelneelpurk/notion-to-mdx-scripts)](https://github.com/neelneelpurk/notion-to-mdx-scripts/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

**Notion to MDX Scripts** turns Notion into a high-performance headless content engine. It fetches pages from a Notion database and converts them into high-fidelity MDX files, perfect for modern static site generators like **Astro**, **Next.js**, or **Cloudflare Pages**.

You can read more about the motivation and setup in this blog post: [Host your Blog on Notion with Cloudflare Pages](https://soumyadeeppurkait.xyz/blog/host-blog-notion-cloudflare/).

---

## ✨ Features

- 🚀 **Built for CI/CD**: Seamlessly integrates with GitHub Actions for automated content syncing.
- 💎 **High-Fidelity Rendering**: Supports complex Notion blocks including nested lists, callouts, toggles, and code blocks.
- 🏷️ **YAML Frontmatter**: Automatically extracts page properties (Slug, Date, Tags, etc.) into clean MDX frontmatter.
- ⚡ **Optimized with uv**: Uses the fastest Python package manager for lightning-fast deployments.
- 🎨 **Rich Content Support**:
    - **Typography**: All heading levels (H1-H3), bold, italic, strikethrough, and inline code.
    - **Lists**: Ordered, unordered, and interactive To-Do lists.
    - **Media**: External images, videos, and file attachments.
    - **Advanced**: Math equations (LaTeX), Toggles (as `<details>`), Quotes, and Callouts.

## 🛠️ Configuration

Configure the script using environment variables:

| Variable | Description | Required | Default |
| :--- | :--- | :---: | :--- |
| `NOTION_API_KEY` | Your Notion Integration Secret | **Yes** | - |
| `BLOG_DATASOURCE_ID` | The ID of the Notion Database to fetch from | **Yes** | - |
| `OUTPUT_DIR` | Directory to save generated MDX files | No | `./content` |

## 🚀 Getting Started

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/neelneelpurk/notion-to-mdx-scripts.git
   cd notion-to-mdx-scripts
   ```

2. **Install dependencies**:
   We recommend using [uv](https://github.com/astral-sh/uv) for the best experience:
   ```bash
   uv sync
   # OR use standard pip
   pip install -e .
   ```

3. **Configure Environment**:
   Create a `.env` file in the root:
   ```env
   NOTION_API_KEY=secret_your_notion_key
   BLOG_DATASOURCE_ID=your_database_id
   OUTPUT_DIR=./content
   ```

4. **Run the sync**:
   ```bash
   uv run main.py
   ```

### 🤖 GitHub Actions Integration

Automate your content sync by adding this workflow to your site's repository:

```yaml
name: Sync Notion Content
on:
  schedule:
    - cron: '0 * * * *' # Every hour
  workflow_dispatch:      # Manual trigger

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Site Repo
        uses: actions/checkout@v4

      - name: Checkout Scripts
        uses: actions/checkout@v4
        with:
          repository: neelneelpurk/notion-to-mdx-scripts
          path: scripts

      - name: Install uv
        uses: astral-sh/setup-uv@v3

      - name: Set up Python
        run: uv python install 3.12

      - name: Run Sync
        run: |
          cd scripts
          uv run main.py
        env:
          NOTION_API_KEY: ${{ secrets.NOTION_API_KEY }}
          BLOG_DATASOURCE_ID: ${{ secrets.BLOG_DATASOURCE_ID }}
          OUTPUT_DIR: "../src/content/blog" # Adjust to your site's structure

      - name: Commit and Push Changes
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore: sync content from notion"
          file_pattern: "src/content/blog/*.mdx"
```


# Introduction

This post was synced automatically from Notion...

> 💡 **Tip**: Use Callouts in Notion for emphasized tips!
```

## 📝 License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details.

---

Built with ❤️ by [Soumyadeep Purkait](https://github.com/neelneelpurk)
