#!/usr/bin/env python3
"""
Data Pipeline: Scrape → Parse → Clean → Load → Analyze
Run this script periodically to update job data
"""

import logging
import sys
import os
from datetime import datetime

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scrapers.remoteok_scraper import fetch_jobs, save_jobs_to_html
from scrapers.weworkremotely_scraper import fetch_jobs as fetch_wwr_jobs, save_jobs_to_html as save_wwr_jobs_to_html
from parsers.parser_remoteok import parse_jobs_from_html, save_jobs_to_csv
from parsers.parser_weworkremotely import parse_jobs_from_html as parse_wwr_jobs_from_html, save_jobs_to_csv as save_wwr_jobs_to_csv
from data.processed.cleaner import main as clean_data
from scripts.load_csv import load_csv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/pipeline.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def run_pipeline():
    """Execute the complete data pipeline"""
    start_time = datetime.now()
    logging.info("🚀 Starting data pipeline...")
    
    try:
        # Step 1: Scrape
        logging.info("📥 Step 1: Scraping jobs from remoteok...")
        jobs = fetch_jobs()
        save_jobs_to_html(jobs)
        
        logging.info("📥 Step 2: Scraping jobs from weworkremotely...")
        wwr_jobs = fetch_wwr_jobs()
        save_wwr_jobs_to_html(wwr_jobs)
        
        # Step 2: Parse
        logging.info("🔍 Step 3: Parsing HTML from remoteok...")
        parsed_jobs = parse_jobs_from_html()
        save_jobs_to_csv(parsed_jobs)
        
        logging.info("🔍 Step 4: Parsing HTML from weworkremotely...")
        parsed_wwr_jobs = parse_wwr_jobs_from_html()
        save_wwr_jobs_to_csv(parsed_wwr_jobs)
        
        # Step 3: Clean
        logging.info("🧹 Step 5: Cleaning data...")
        clean_data()
        
        # Step 4: Load to database
        logging.info("💾 Step 6: Loading to database...")
        load_csv()
        
        # Step 5: Update analytics
        logging.info("📊 Step 7: Updating analytics...")
        # Analytics are automatically updated via the stats endpoints
        
        duration = (datetime.now() - start_time).total_seconds()
        logging.info(f"✅ Pipeline completed successfully in {duration:.2f} seconds")
        
    except Exception as e:
        logging.error(f"❌ Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()