from bs4 import BeautifulSoup
import os
import csv

def parse_jobs_from_html(filename=None):
    if filename is None:
        filename = os.path.join("..", "data", "raw", "jobs.html")
    with open(filename, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    jobs = []
    for job_div in soup.find_all("div", class_="job"):
        title = job_div.find("h2").get_text(strip=True)
        company = job_div.find("p").get_text(strip=True).replace("Company:", "")
        # print(company.replace("Company:", ""))
        location = job_div.find_all("p")[1].get_text(strip=True).replace("Location:", "")
        salary = job_div.find_all("p")[2].get_text(strip=True).replace("Salary:", "")
        apply_link = job_div.find("a")["href"]

        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "salary": salary,
            "apply_link": apply_link
        })
    
    return jobs

def save_jobs_to_csv(jobs, filename="../data/processed/jobs.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "company", "location", "salary", "apply_link"])
        writer.writeheader()
        writer.writerows(jobs)


if __name__ == "__main__":
    jobs = parse_jobs_from_html()
    save_jobs_to_csv(jobs)
    print(f"Saved {len(jobs)} jobs to ../data/processed/jobs.csv")
