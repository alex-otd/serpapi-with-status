# serpapi-with-status

A small command-line tool that uses [SerpApi](https://serpapi.com/) to:

- Query Google (e.g. `site:example.com`)
- Collect organic search result URLs
- Resolve each URL and follow redirects
- Record HTTP status codes (200, 301, 404, etc.) and status descriptions
- Export everything to a CSV for audits, migrations, or redirect planning

**Typical use cases:**

- **Website/platform migrations**: find URLs that return 4xx or unexpected 3xx
- **SEO cleanup**: identify broken URLs Google still has indexed
- **Redirect mapping**: see where URLs actually resolve after multiple redirects

**Repository**: https://github.com/alex-otd/serpapi-with-status

---

## Features

- Uses SerpApi (Google Search JSON API) rather than scraping HTML
- Continuous position indexing across multiple result pages (1…N)
- Follows redirects and records the final resolved URL
- Captures HTTP status code and a human-readable status string
- Checks writability of the output CSV file before making any API calls
- Simple CLI interface with flags for query, pages, location, and output file

---

## Requirements

- Python 3.9+ (3.10 or newer recommended)
- A SerpApi account and API key
- Internet access from the machine running the script

**Python dependencies** (also listed in `requirements.txt`):

- `google-search-results`
- `requests`
- `python-dotenv`

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/alex-otd/serpapi-with-status.git
cd serpapi-with-status
```

2. **Create and activate a virtual environment (recommended):**

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## Configuration

The script expects your SerpApi key in an environment variable named `SERPAPI_API_KEY`.

You can provide it using a `.env` file:

1. **Copy the example file:**

```bash
cp example.env .env
```

2. **Edit `.env` and set your key:**

```env
SERPAPI_API_KEY=your_real_serpapi_key_here
```

`python-dotenv` will load this automatically when you run the script.

**Alternatively**, export the variable directly in your shell:

```bash
# macOS / Linux
export SERPAPI_API_KEY=your_real_serpapi_key_here

# Windows (PowerShell)
$env:SERPAPI_API_KEY="your_real_serpapi_key_here"
```

---

## Usage

The main script is `serp_scraper.py`. It is designed to run from the command line.

**Basic example:**

```bash
python serp_scraper.py \
  --query "site:example.com" \
  --pages 5 \
  --output serp_results.csv
```

**Common migration use case:**

```bash
python serp_scraper.py \
  --query "site:example.com/old-section" \
  --pages 10 \
  --output old_section_status.csv
```

### Command-line arguments

**`--query`** (required)  
The Google search query to send to SerpApi.

Examples:
- `site:example.com`
- `site:example.com/old-section`
- `site:example.com inurl:/blog/`

**`--location`** (default: `United States`)  
Location for the Google search.

**`--pages`** (default: `10`)  
Number of Google results pages to request.  
Each page returns up to 10 organic results.

**`--output`** (default: `serp_results.csv`)  
Output CSV filename.

**Example:**

```bash
python serp_scraper.py \
  --query "site:westcoastdownsizingsolution.com" \
  --pages 10 \
  --output westcoastdownsize_status.csv
```

---

## Output: CSV Columns

The script writes a CSV with the following columns:

| Column | Description |
|--------|-------------|
| **position** | Continuous position across all pages (1, 2, 3, …). Not reset per page, unlike Google. |
| **title** | Search result title. |
| **link** | The original URL Google returned via SerpApi. This represents what is indexed. |
| **final_url** | The fully resolved URL after following redirects (if any).<br>Example:<br>`link: https://domain.com/old`<br>`final_url: https://domain.com/new` |
| **http_code** | The HTTP status code of `final_url`:<br>• `200` — OK<br>• `301` — Permanent redirect<br>• `404` — Not Found<br>• `410` — Gone<br>• `500` — Server Error |
| **status** | Human-readable description:<br>• `OK`<br>• `Moved Permanently`<br>• `Not Found`<br>• `Server Error`<br>or an error message |
| **displayed_link** | The simplified URL displayed by Google. |
| **snippet** | Google's text snippet for the result. |

---

## Pre-flight CSV Check

Before any SerpApi API calls, the script attempts to open the output CSV.

If it cannot (e.g. Excel has it open), the script will:
- Print an error
- Exit
- Prevent API credits from being spent

This is intentional to reduce accidental API usage.

---

## Notes and Limitations

- This tool uses SerpApi's JSON API. You are responsible for your own key and credit usage.
- Google often reports an approximate number of indexed URLs. Actual available pages may be fewer.
- The script stops automatically when SerpApi no longer returns organic results.
- **This is not a crawler.** It only audits URLs returned by the search query you specify.

---

## Typical Workflow for Site Migrations

1. **Run a `site:` query for the old domain or directory:**

```bash
python serp_scraper.py \
  --query "site:oldsite.com" \
  --pages 10 \
  --output old_status.csv
```

2. **Open the CSV and inspect:**
   - `http_code` in `404`, `410` → broken URLs still indexed
   - `http_code` in `301`, `302`, `307`, `308` where `final_url != link` → redirect chains or legacy paths

3. **Build redirect mappings:**  
   Add a `new_url` column mapping `link` → new location.

4. **Implement redirects:**
   - Apache `.htaccess`
   - Nginx
   - Shopify CSV redirects
   - WordPress Redirection plugin
   - Cloudflare rules

---

## Project Structure

```
serpapi-with-status/
├── serp_scraper.py
├── requirements.txt
├── .gitignore
├── example.env
└── README.md
```

You can customize:
- `STATUS_MEANINGS`
- Timeout logic
- CSV columns
- Output formatting

---

## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

---

## Disclaimer

This project is not affiliated with Google or SerpApi.  
Use responsibly and in compliance with their terms of service.