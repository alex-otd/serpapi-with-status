# serpapi-with-status

A small command-line tool that uses [SerpApi](https://serpapi.com/) to:

- Query Google (e.g. `site:example.com`)
- Collect organic search result URLs
- Resolve each URL and follow redirects
- Record HTTP status codes (200, 301, 404, etc.) and status descriptions
- Export everything to a CSV for audits, migrations, or redirect planning

Typical use cases:

- Website/platform migrations: find URLs that return 4xx or unexpected 3xx
- SEO cleanup: identify broken URLs Google still has indexed
- Redirect mapping: see where URLs actually resolve after multiple redirects

Repository: https://github.com/alex-otd/serpapi-with-status

---

## ⚠️ Before You Start

This tool requires:
- **Python 3.9+** installed on your system
- **A SerpAPI account** ([sign up free](https://serpapi.com/) - 100 searches/month on free tier)
- **5 minutes** to set up

**First time using this tool?** Follow all steps below in order - don't skip any!

---

## Features

- Uses SerpApi (Google Search JSON API) rather than scraping HTML
- Continuous position indexing across multiple result pages (1…N)
- Follows redirects and records the final resolved URL
- Captures HTTP status code and a human-readable status string
- Checks writability of the output CSV file before making any API calls
- Simple CLI interface with flags for query, pages, location, and output file

---

## Quick Start Guide

### Prerequisites

Before installing, make sure you have:
- [ ] Python 3.9 or newer (`python --version` or `python3 --version` to check)
- [ ] Git installed
- [ ] A SerpAPI account (get your free API key at https://serpapi.com/manage-api-key)

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/alex-otd/serpapi-with-status.git
cd serpapi-with-status
```

---

### Step 2: Create a Virtual Environment

**This step is required to avoid conflicts with other Python projects.**

```bash
python -m venv .venv
```

Then activate it:

**On macOS / Linux:**
```bash
source .venv/bin/activate
```

**On Windows (Command Prompt):**
```bash
.venv\Scripts\activate
```

**On Windows (PowerShell):**
```bash
.venv\Scripts\Activate.ps1
```

You should see `(.venv)` appear at the start of your command prompt.

---

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Python dependencies installed:
- `google-search-results` - SerpAPI client library
- `requests` - HTTP requests and redirect handling
- `python-dotenv` - Loads environment variables from .env file

---

### Step 4: Configure Your API Key (⚠️ REQUIRED)

**Without this step, the script will not work!**

1. **Copy the example environment file:**
   ```bash
   cp example.env .env
   ```

2. **Get your SerpAPI key:**
   - Sign up or log in at https://serpapi.com/
   - Go to https://serpapi.com/manage-api-key
   - Copy your API key

3. **Edit the `.env` file:**
   Open `.env` in any text editor and replace `your_serpapi_key_here` with your actual key:
   ```
   SERPAPI_API_KEY=your_actual_key_from_serpapi
   ```

4. **Save the file**

The script will automatically load this key when you run it.

**Alternative method (not recommended for beginners):**
You can also set the environment variable directly in your shell:

```bash
# macOS / Linux
export SERPAPI_API_KEY=your_real_serpapi_key_here

# Windows (PowerShell)
$env:SERPAPI_API_KEY="your_real_serpapi_key_here"
```

---

### Step 5: Run Your First Search

Test that everything works with a simple query:

```bash
python serp_scraper.py \
  --query "site:example.com" \
  --pages 2 \
  --output test_results.csv
```

If successful, you'll see:
- Progress messages as pages are fetched
- Status codes being checked
- A `test_results.csv` file created in your directory

---

## Usage

The main script is `serp_scraper.py`. It runs from the command line with various options.

### Basic Example

```bash
python serp_scraper.py \
  --query "site:example.com" \
  --pages 5 \
  --output serp_results.csv
```

### Common Migration Use Case

```bash
python serp_scraper.py \
  --query "site:example.com/old-section" \
  --pages 10 \
  --output old_section_status.csv
```

### Command-line Arguments

**`--query` (required)**  
The Google search query to send to SerpApi.

Examples:
- `site:example.com`
- `site:example.com/old-section`
- `site:example.com inurl:/blog/`

**`--location` (default: `United States`)**  
Location for the Google search.

**`--pages` (default: `10`)**  
Number of Google results pages to request.  
Each page returns up to 10 organic results.

**`--output` (default: `serp_results.csv`)**  
Output CSV filename.

### Full Example

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
| **http_code** | The HTTP status code of final_url:<br>• 200 — OK<br>• 301 — Permanent redirect<br>• 404 — Not Found<br>• 410 — Gone<br>• 500 — Server Error |
| **status** | Human-readable description:<br>• OK<br>• Moved Permanently<br>• Not Found<br>• Server Error<br>or an error message |
| **displayed_link** | The simplified URL displayed by Google. |
| **snippet** | Google's text snippet for the result. |

---

## Troubleshooting

### "SERPAPI_API_KEY environment variable not found"
**Problem:** Your `.env` file is missing or the API key isn't set.

**Solution:**
1. Make sure you ran `cp example.env .env`
2. Open `.env` and verify your API key is there
3. Make sure there are no spaces around the `=` sign
4. Restart your terminal or reactivate your virtual environment

---

### "Permission denied" or "File in use" error
**Problem:** The output CSV file is open in another program (like Excel).

**Solution:** Close the CSV file in any programs that have it open, then run the script again.

This pre-flight check prevents wasting API credits on failed writes.

---

### "Module not found" or "No module named 'serpapi'"
**Problem:** Dependencies aren't installed or virtual environment isn't activated.

**Solution:**
1. Make sure you see `(.venv)` at the start of your command prompt
2. If not, activate it: `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\activate` (Windows)
3. Run `pip install -r requirements.txt` again

---

### "Python version not supported" or script won't run
**Problem:** You're using Python 3.8 or older.

**Solution:** Upgrade to Python 3.9 or newer. Check your version with:
```bash
python --version
```

---

### No results returned or fewer pages than expected
**Problem:** Google may not have indexed as many pages as you requested.

**Solution:** 
- Try a broader search query
- Check that your `site:` query is spelled correctly
- Note that Google's reported result count is often approximate

---

### "Invalid API key" or "401 Unauthorized"
**Problem:** Your SerpAPI key is incorrect or you've run out of credits.

**Solution:**
1. Double-check your API key at https://serpapi.com/manage-api-key
2. Check your account credit balance at https://serpapi.com/dashboard
3. Free accounts get 100 searches per month

---

## Pre-flight CSV Check

Before any SerpApi API calls, the script attempts to open the output CSV file for writing.

If it cannot (e.g. Excel has it open), the script will:
- Print an error message
- Exit immediately
- Prevent API credits from being spent

This is intentional to reduce accidental API usage and wasted credits.

---

## Typical Workflow for Site Migrations

**1. Run a `site:` query for the old domain or directory:**

```bash
python serp_scraper.py \
  --query "site:oldsite.com" \
  --pages 10 \
  --output old_status.csv
```

**2. Open the CSV and inspect:**
- `http_code` in `404`, `410` → broken URLs still indexed
- `http_code` in `301`, `302`, `307`, `308` where `final_url != link` → redirect chains or legacy paths

**3. Build redirect mappings:**
Add a `new_url` column mapping `link` → new location.

**4. Implement redirects using:**
- Apache `.htaccess`
- Nginx
- Shopify CSV redirects
- WordPress Redirection plugin
- Cloudflare rules

---

## Notes and Limitations

- This tool uses SerpApi's JSON API. You are responsible for your own key and credit usage.
- Google often reports an approximate number of indexed URLs. Actual available pages may be fewer.
- The script stops automatically when SerpApi no longer returns organic results.
- This is **not a crawler**. It only audits URLs returned by the search query you specify.

---

## Project Structure

```
serpapi-with-status/
├── serp_scraper.py       # Main script
├── requirements.txt      # Python dependencies
├── .gitignore           # Git ignore rules
├── example.env          # Example environment file
└── README.md            # This file
```

You can customize:
- `STATUS_MEANINGS` in the code
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
