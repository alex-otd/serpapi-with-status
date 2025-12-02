import os
import sys
import csv
from pathlib import Path

# ==============================================================================
#  👇 USER CONFIGURATION - EDIT YOUR SEARCH SETTINGS HERE 👇
# ==============================================================================

SEARCH_QUERY    = "site:onethingdigital.com"    # The query you want to search Google for, you can use commands like site: if you need
SEARCH_LOCATION = "United States"       # The region for the search results
NUMBER_OF_PAGES = 1                     # How many pages to fetch (10 results per page)
OUTPUT_FILENAME = "serp_results.csv"    # The file where results will be saved

# ==============================================================================
#  👆 END CONFIGURATION 👆
# ==============================================================================


# --- IMPROVED IMPORT SECTION ---
try:
    import requests
    from serpapi import GoogleSearch
    from dotenv import load_dotenv, find_dotenv
except ImportError as e:
    print("\n" + "=" * 60)
    print("❌ MISSING LIBRARIES DETECTED")
    print("=" * 60)
    print(f"Error detail: {e}")
    print("\nPlease run the following command to install the required libraries:")
    print("\n    pip install python-dotenv google-search-results requests")
    print("\n" + "=" * 60 + "\n")
    sys.exit(1)

# Check Python version
if sys.version_info < (3, 9):
    print("=" * 60)
    print("ERROR: Python 3.9 or newer is required")
    print("=" * 60)
    sys.exit(1)

# --- ROBUST .ENV LOADING ---
script_location = Path(__file__).resolve().parent
env_file_path = script_location / '.env'

print(f"DEBUG: Looking for .env at: {env_file_path}")

if env_file_path.exists():
    print("DEBUG: Found .env file. Loading...")
    load_dotenv(dotenv_path=env_file_path)
else:
    print("DEBUG: ❌ .env file NOT found at that path.")

# Check if key is loaded
if not os.getenv('SERPAPI_API_KEY'):
    print("\n" + "=" * 60)
    print("❌ ERROR: SERPAPI_API_KEY not loaded!")
    print("=" * 60)
    print(f"We found the file at: {env_file_path}")
    print("But we couldn't read 'SERPAPI_API_KEY' from it.")
    print("\nPlease check:")
    print("1. Did you save the file?")
    print("2. Does it contain: SERPAPI_API_KEY=your_key_here")
    print("\n" + "=" * 60 + "\n")
    sys.exit(1)

STATUS_MEANINGS = {
    200: "OK",
    201: "Created",
    202: "Accepted",
    204: "No Content",
    301: "Moved Permanently",
    302: "Temporary Redirect",
    303: "See Other",
    307: "Temporary Redirect (Preserve Method)",
    308: "Permanent Redirect (Preserve Method)",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    410: "Gone",
    429: "Too Many Requests",
    500: "Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
}

def assert_csv_writable(filename: str) -> bool:
    """Check that we can write to the CSV file BEFORE any API calls."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            f.write("")
        return True
    except Exception as e:
        print(f"Cannot write to {filename}")
        print(f"Reason: {e}")
        print("Close the file (Excel/other) and try again.")
        return False

def check_url_status(url: str, timeout: int = 10):
    """
    Check a URL via HEAD first, fall back to GET.
    Returns (status_code, meaning, final_url).
    """
    try:
        r = requests.head(url, allow_redirects=True, timeout=timeout)
        code = r.status_code
        return code, STATUS_MEANINGS.get(code, "Unknown"), r.url
    except Exception:
        pass

    try:
        r = requests.get(url, allow_redirects=True, timeout=timeout)
        code = r.status_code
        return code, STATUS_MEANINGS.get(code, "Unknown"), r.url
    except Exception as e:
        return None, f"Error: {e}", url

def fetch_google_results(query: str, location: str, pages: int):
    api_key = os.getenv("SERPAPI_API_KEY")
    all_results = []
    position = 1
    per_page = 10

    for page in range(pages):
        start = page * per_page

        params = {
            "engine": "google",
            "q": query,
            "location": location,
            "hl": "en",
            "gl": "us",
            "google_domain": "google.com",
            "num": per_page,
            "start": start,
            "api_key": api_key,
        }

        print(f"Fetching Google page {page + 1}...")

        try:
            search = GoogleSearch(params)
            data = search.get_dict()
        except Exception as e:
            print(f"Error connecting to SerpAPI: {e}")
            break

        if "error" in data:
            print(f"API Error: {data['error']}")
            break

        organic = data.get("organic_results", [])
        if not organic:
            print("No additional results found.")
            break

        for item in organic:
            url = item.get("link")
            if not url:
                continue
                
            code, meaning, resolved_url = check_url_status(url)

            all_results.append({
                "position": position,
                "title": item.get("title"),
                "link": url,
                "final_url": resolved_url,
                "http_code": code,
                "status": meaning,
                "displayed_link": item.get("displayed_link"),
                "snippet": item.get("snippet"),
            })
            position += 1

    return all_results

def save_results_to_csv(results, filename: str):
    fieldnames = [
        "position", "title", "link", "final_url", 
        "http_code", "status", "displayed_link", "snippet"
    ]

    try:
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        print(f"Saved {len(results)} URLs to {filename}")
    except Exception as e:
        print(f"Error saving CSV: {e}")

def main():
    # Verify we can write to the output file before starting
    if not assert_csv_writable(OUTPUT_FILENAME):
        sys.exit(1)

    print(f"\n--- Starting Search ---")
    print(f"Query:    {SEARCH_QUERY}")
    print(f"Location: {SEARCH_LOCATION}")
    print(f"Pages:    {NUMBER_OF_PAGES}")
    print(f"Output:   {OUTPUT_FILENAME}")
    print("-" * 23 + "\n")

    results = fetch_google_results(
        query=SEARCH_QUERY,
        location=SEARCH_LOCATION,
        pages=NUMBER_OF_PAGES,
    )

    save_results_to_csv(results, OUTPUT_FILENAME)

if __name__ == "__main__":
    main()