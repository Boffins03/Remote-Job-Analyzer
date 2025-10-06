import scrapers.remoteok_scraper as remoteok_scraper
import schedule
import time

def run_pipeline():
    print("Starting job scraping pipeline...")
    jobs = remoteok_scraper.fetch_jobs()
    remoteok_scraper.save_jobs_to_html(jobs)
    print("Job scraping pipeline completed.")   

# Schedule the pipeline to run every day at 9 AM
schedule.every().day.at("09:00").do(run_pipeline)   
print("-" * 40)

print("Job Scraping Pipeline Scheduler")
