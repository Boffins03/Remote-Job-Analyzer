import os
import json
import time
import logging
import requests
from datetime import datetime

# Logging setup
logging.basicConfig(
    filename="logs/remoteok_scraper.log",
    level=logging.INFO,
    format="%(asctime)s- %(levelname)s - %(message)s",
)

def ensure_directories():
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("logs", exist_ok=True)


def fetch_jobs() -> list[dict]:
    """Fetch remote job listings from RemoteOK API."""
    url = "https://remoteok.com/api"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0 Safari/537.36"
        ),
        "Accept": "application/json",
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        time.sleep(1)
        response.raise_for_status()
        logging.info("Successfully fetched data from RemoteOK.")
        return response.json()
    
    except requests.RequestException as e:
        logging.error(f"Failed to fetch jobs: {e}")
        raise



def save_jobs_to_html(jobs,filename = "data/raw/jobs_remoteok.html"):
    with open(filename,"w",encoding="utf-8") as f:
        f.write("<html><head><title>Remote Jobs</title></head><body>")
        f.write("<h1>Remote Jobs(Raw Snapshot of RemoteOK)</h1>")
        
        for job in jobs:
            # Skip the 'legal' entry
            if "legal" in job:
                continue  

            f.write("<div class='job'>")
            f.write(f"<h2>{job.get('position', 'N/A')}</h2>")
            f.write(f"<p><b>Company: </b> {job.get('company', 'N/A')}</p>")
            f.write(f"<p><b>Location: </b> {job.get('location', 'N/A')}</p>")
            f.write(f"<p><b>Salary: </b> {job.get('salary_min', 'N/A')} - {job.get('salary_max', 'N/A')}</p>")
            f.write(f"<a href='{job.get('apply_url', job.get('url', '#'))}' target='_blank'>Apply Here</a>")
            f.write("<hr></div>")
        
        f.write("</body></html>")
    
    print(f"Jobs saved to {filename}")

if __name__ == "__main__":
    jobs = fetch_jobs()
    # print(jobs)
    save_jobs_to_html(jobs)
    print("Fetched and saved jobs from RemoteOK")
