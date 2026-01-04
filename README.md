# Notion to MDX Scripts

Notion to MDX Scripts turns Notion into a headless content engine for your static site (Cloudflare Pages, Next.js, Astro, etc.). It fetches pages from a Notion database and converts them into MDX files with full frontmatter and high-fidelity block rendering.

## Features

- **Automated Content Sync**: Fetches all pages from a specified Notion database.
- **Rich Markdown (MDX)**: Converts Notion blocks (headings, lists, code, images, etc.) into clean MDX.
- **Frontmatter Support**: Automatically extracts page properties as YAML frontmatter.
- **GitHub Actions Integration**: Built to run as part of your CI/CD pipeline.

## Configuration

The script is configured via environment variables.

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `NOTION_API_KEY` | Your Notion Integration Secret | Yes | - |
| `BLOG_DATASOURCE_ID` | The ID of the Notion Database to fetch from | Yes | - |
| `OUTPUT_DIR` | Directory to save generated MDX files | No | `./content` |

## Usage

### Local Development

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/notion-to-mdx-scripts.git
    cd notion-to-mdx-scripts
    ```

2.  **Install dependencies**:
    ```bash
    pip install -e .
    # OR if using uv
    uv sync
    ```

3.  **Setup Environment**:
    Create a `.env` file in the root directory:
    ```env
    NOTION_API_KEY=secret_...
    BLOG_DATASOURCE_ID=your_database_id
    OUTPUT_DIR=./content
    ```

4.  **Run the script**:
    ```bash
    python main.py
    ```

### GitHub Actions

To use this in your workflow, you can run the python script directly.

```yaml
name: Sync Content
on:
  schedule:
    - cron: '0 0 * * *' # Run daily

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repo
        uses: actions/checkout@v4

      - name: Checkout notion-to-mdx-scripts
        uses: actions/checkout@v4
        with:
          repository: neelneelpurk/notion-to-mdx-scripts
          ref: main
          path: notion-to-mdx-scripts

      - name: Install uv
        uses: astral-sh/setup-uv@v3

      - name: Set up Python
        run: uv python install 3.12

      - name: Run notion-to-mdx-scripts
        run: |
          cd notion-to-mdx-scripts
          uv run main.py
        env:
          OUTPUT_DIR: "./output"
          NOTION_API_KEY: ${{ secrets.NOTION_API_KEY }}
          BLOG_DATASOURCE_ID: ${{ secrets.BLOG_DATASOURCE_ID }}
...

```

## License

[Apache 2.0](LICENSE)
