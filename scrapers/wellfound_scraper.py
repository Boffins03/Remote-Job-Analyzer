import requests
import os

def fetch_jobs() -> list[dict]:
    """Fetch remote job listings from Wellfound (AngelList)."""
    url = "https://wellfound.com/remote"
    headers = {
        "User-Agent": (
           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
           "AppleWebKit/537.36 (KHTML, like Gecko) "
           "Chrome/140.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Dnt": "1",
        
    }
    response = requests.get(url, headers=headers, timeout=10)
    return response.text

def save_html(content: str, filename="data/raw/jobs_wellfound.html"):
    """Save the HTML content to a local file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"HTML saved to {filename}")

if __name__ == "__main__":
    jobs = fetch_jobs()
    save_html(jobs)
    print("Fetched and saved jobs from Wellfound")