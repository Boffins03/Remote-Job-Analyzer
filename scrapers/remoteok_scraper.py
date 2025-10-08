import requests

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
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()

def save_jobs_to_html(jobs,filename = "data/raw/jobs_remoteok.html"):
    with open(filename,"w",encoding="utf-8") as f:
        f.write("<html><head><title>Jobs</title></head><body>")
        f.write("<h1>Remote Jobs</h1>")
        
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
    save_jobs_to_html(jobs)
    print("Fetched and saved jobs from RemoteOK")
