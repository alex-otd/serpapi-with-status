import os
import sys
import csv
import argparse
import requests
from serpapi import GoogleSearch
from dotenv import load_dotenv

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
        print(f"CSV writable: {filename}")
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

def fetch_google_results(query: str, location: str = "United States", pages: int = 10):
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise RuntimeError("SERPAPI_API_KEY environment variable not set")

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
            "filter": "0",
            "api_key": api_key,
        }

        print(f"Fetching Google page {page + 1}...")

        search = GoogleSearch(params)
        data = search.get_dict()

        organic = data.get("organic_results", [])
        if not organic:
            print("No additional results found.")
            break

        for item in organic:
            url = item.get("link")
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
        "position",
        "title",
        "link",
        "final_url",
        "http_code",
        "status",
        "displayed_link",
        "snippet",
    ]

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Saved {len(results)} URLs to {filename}")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Fetch Google results via SerpApi and audit URL status codes."
    )
    parser.add_argument(
        "--query",
        required=True,
        help='Google query, e.g. "site:example.com/old-section"',
    )
    parser.add_argument(
        "--location",
        default="United States",
        help="Search location (default: United States)",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=10,
        help="Number of Google result pages to fetch (10 results per page)",
    )
    parser.add_argument(
        "--output",
        default="serp_results.csv",
        help="Output CSV filename (default: serp_results.csv)",
    )
    return parser.parse_args()

def main():
    # Load .env if present
    load_dotenv()

    args = parse_args()
    output_file = args.output

    if not assert_csv_writable(output_file):
        sys.exit(1)

    results = fetch_google_results(
        query=args.query,
        location=args.location,
        pages=args.pages,
    )

    save_results_to_csv(results, output_file)

if __name__ == "__main__":
    main()
