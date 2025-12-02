# serpapi-with-status

A small Python tool that uses SerpApi to:

- Query Google (e.g. `site:example.com`)
- Collect organic search result URLs
- Resolve each URL and follow redirects
- Record HTTP status codes (200, 301, 404, etc.) and status descriptions
- Export everything to a CSV for audits, migrations, or redirect planning

## Typical use cases

- **Website/platform migrations**: find URLs that return 4xx or unexpected 3xx
- **SEO cleanup**: identify broken URLs Google still has indexed
- **Redirect mapping**: see where URLs actually resolve after multiple redirects

**Repository**: https://github.com/alex-otd/serpapi-with-status

---

## ⚠️ Before You Start

This tool requires:

- Python 3.9+ installed on your system
- A SerpAPI account (sign up free - 100 searches/month on free tier)
- 5 minutes to set up

---

## Features

- Uses SerpApi (Google Search JSON API) rather than scraping HTML
- Continuous position indexing across multiple result pages (1…N)
- Follows redirects and records the final resolved URL
- Captures HTTP status code and a human-readable status string
- Checks writability of the output CSV file before making any API calls
- Easy Configuration: Edit settings directly at the top of the script

---

## Quick Start Guide

### Prerequisites

Before installing, make sure you have:

- [ ] Python 3.9 or newer (`python --version` to check)
- [ ] Git installed
- [ ] A SerpAPI account (get your free API key at https://serpapi.com/manage-api-key)

### Step 1: Clone the Repository

```bash
git clone https://github.com/alex-otd/serpapi-with-status.git
cd serpapi-with-status
```

### Step 2: Create a Virtual Environment

This step is required to avoid conflicts with other Python projects.

```bash
python -m venv .venv
```

Then activate it:

**On macOS / Linux:**
```bash
source .venv/bin/activate
```

**On Windows (Command Prompt):**
```cmd
.venv\Scripts\activate
```

**On Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

You should see `(.venv)` appear at the start of your command prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Your API Key (⚠️ REQUIRED)

**Without this step, the script will not work!**

1. Copy the example environment file:
   ```bash
   cp example.env .env
   ```
   (On Windows, you can just manually create a file named `.env`)

2. Get your SerpAPI key:
   - Sign up or log in at https://serpapi.com/
   - Go to https://serpapi.com/manage-api-key
   - Copy your API key

3. Edit the `.env` file:
   - Open `.env` in any text editor and replace `your_serpapi_key_here` with your actual key:
   ```
   SERPAPI_API_KEY=your_actual_key_from_serpapi
   ```
   - Save the file

### Step 5: Configure Your Search

Open `serpAPI_withStatus.py` in your code editor (VS Code, Notepad++, etc.).

Look for the **USER CONFIGURATION** section at the top:

```python
# ==============================================================================
#  👇 USER CONFIGURATION - EDIT YOUR SEARCH SETTINGS HERE 👇
# ==============================================================================

SEARCH_QUERY    = "site:example.com"    # The query you want to search Google for
SEARCH_LOCATION = "United States"       # The region for the search results
NUMBER_OF_PAGES = 1                     # How many pages to fetch (10 results per page)
OUTPUT_FILENAME = "serp_results.csv"    # The file where results will be saved

# ==============================================================================
#  👆 END CONFIGURATION 👆
# ==============================================================================
```

Edit these variables to match what you want to search for.

### Step 6: Run the Script

Run the script from your terminal:

```bash
python serpAPI_withStatus.py
```

If successful, you'll see:
- Progress messages as pages are fetched
- Status codes being checked
- A CSV file (e.g., `serp_results.csv`) created in your directory

---

## Output: CSV Columns

The script writes a CSV with the following columns:

| Column | Description |
|--------|-------------|
| **position** | Continuous position across all pages (1, 2, 3, …). Not reset per page, unlike Google. |
| **title** | Search result title. |
| **link** | The original URL Google returned via SerpApi. This represents what is indexed. |
| **final_url** | The fully resolved URL after following redirects (if any).<br><br>Example:<br>`link: https://domain.com/old`<br>`final_url: https://domain.com/new` |
| **http_code** | The HTTP status code of `final_url`:<br>• 200 — OK<br>• 301 — Permanent redirect<br>• 404 — Not Found<br>• 410 — Gone<br>• 500 — Server Error |
| **status** | Human-readable description:<br>• OK<br>• Moved Permanently<br>• Not Found<br>• Server Error<br>or an error message |
| **displayed_link** | The simplified URL displayed by Google. |
| **snippet** | Google's text snippet for the result. |

---

## Troubleshooting

### "SERPAPI_API_KEY not loaded!"

**Problem**: Your `.env` file is missing or the API key isn't set.

**Solution**:
- Ensure the file is named exactly `.env` (not `.env.txt`)
- Ensure it is in the same folder as the script
- Make sure there are no spaces around the `=` sign inside the file

### "Permission denied" or "File in use" error

**Problem**: The output CSV file is open in another program (like Excel).

**Solution**: Close the CSV file in any programs that have it open, then run the script again.

### "Module not found" or "No module named 'serpapi'"

**Problem**: Dependencies aren't installed or virtual environment isn't activated.

**Solution**:
- Make sure you see `(.venv)` at the start of your command prompt
- If not, activate it: `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\activate` (Windows)
- Run `pip install -r requirements.txt` again

---

## Typical Workflow for Site Migrations

1. **Configure the script:**
   - Set `SEARCH_QUERY = "site:oldsite.com"`
   - Set `NUMBER_OF_PAGES = 10`
   - Set `OUTPUT_FILENAME = "old_status.csv"`

2. **Run the script:**
   ```bash
   python serpAPI_withStatus.py
   ```

3. **Open the CSV and inspect:**
   - `http_code` in 404, 410 → broken URLs still indexed
   - `http_code` in 301, 302 where `final_url != link` → redirect chains or legacy paths

---

## Project Structure

```
serpapi-with-status/
├── serpAPI_withStatus.py  # Main script
├── requirements.txt       # Python dependencies
├── .gitignore             # Git ignore rules
├── example.env            # Example environment file
└── README.md              # This file
```

---

## License

This project is licensed under the MIT License.

See the LICENSE file for details.