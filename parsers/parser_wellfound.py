from bs4 import BeautifulSoup
import os
import csv

def parse_jobs_from_html(filename=None):
    if filename is None:
        filename = os.path.join("..", "data", "raw", "jobs_wellfound.html")

    with open(filename, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    job_fetched = []

    for job_div in soup.find_all("div", class_="my-4 w-full"):
        for jobs in job_div.find_all("div", class_="mb-6 w-full rounded border border-gray-400 bg-white"):
            company_tag = jobs.find("div", class_="flex space-x-2")
            for job in jobs.find_all("div", class_="w-full pb-1 sm:pb-0"):
                title_tag = job.find("div", class_="mb-1 flex items-start")
                details_tag = job.find("div", class_="sm:flex sm:space-x-2")
                link_tag = title_tag.find("a", recursive=False)
                # Extract text safely
                title = title_tag.find("a").text.strip() if title_tag else "N/A"
                company = company_tag.find("h2").text.strip() if company_tag else "N/A"
                details = details_tag.text.strip() if details_tag else "N/A"
                apply_link = "https://wellfound.com/" + link_tag["href"] if link_tag and link_tag.get("href") else "N/A"

                job_fetched.append({
                    "title": title,
                    "company": company,
                    "details": details,
                    "apply_link": apply_link
                })

    return job_fetched

def save_jobs_to_csv(jobs, filename="../data/processed/jobs_wellfound.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "company", "details", "apply_link"])
        writer.writeheader()
        writer.writerows(jobs)


if __name__ == "__main__":
    jobs = parse_jobs_from_html()
    save_jobs_to_csv(jobs)
    print(f"Saved {len(jobs)} jobs to ../data/processed/jobs_wellfound.csv")
