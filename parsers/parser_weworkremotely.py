from bs4 import BeautifulSoup
import os
import csv


def parse_jobs_from_html(filename=None):
    if filename is None:
        filename = os.path.join("..", "data", "raw", "jobs_weworkremotely.html")

    with open(filename, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    jobs = []

    for job_div in soup.find_all("div", class_="search-listings__container"):
        for job in job_div.find_all("li"):
            # Skip non-job list items
            if not job.find("a"):
                continue

            title_tag = job.find("div", class_="new-listing__header")
            company_tag = job.find("p", class_="new-listing__company-name")
            location_tag = job.find("p", class_="new-listing__company-headquarters")
            categories_tag = job.find("p", class_="new-listing__categories")
            link_tag = job.find("a", recursive=False)

            # Extract text safely
            title = title_tag.find("h3").text.strip() if title_tag else "N/A"
            company = company_tag.text.strip() if company_tag else "N/A"
            location = location_tag.text.strip() if location_tag else "N/A"
            categories = categories_tag.text.strip() if categories_tag else "N/A"
            apply_link = "https://weworkremotely.com" + link_tag["href"] if link_tag and link_tag.get("href") else "N/A"

            jobs.append({
                "title": title,
                "company": company,
                "location": location,
                "categories": categories,
                "apply_link": apply_link
            })

    return jobs

def save_jobs_to_csv(jobs, filename="../data/processed/jobs_weworkremotely.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "company", "location", "categories", "apply_link"])
        writer.writeheader()
        writer.writerows(jobs)


if __name__ == "__main__":
    jobs = parse_jobs_from_html()
    save_jobs_to_csv(jobs)
    print(f"Saved {len(jobs)} jobs to jobs_weworkremotely.csv")
