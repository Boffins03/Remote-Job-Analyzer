# analysis/queries.py
from sqlalchemy import text

# 1. Job count by company
QUERY_TOP_COMPANIES = text("""
SELECT c.name AS company, COUNT(j.id) AS total_jobs
FROM jobs j
JOIN companies c ON j.company_id = c.id
GROUP BY c.id
ORDER BY total_jobs DESC
LIMIT 10;
""")

# 2. Jobs per month (trend)
QUERY_JOBS_PER_MONTH = text("""
SELECT DATE_TRUNC('month', j.scraped_at) AS month, COUNT(j.id) AS total_jobs
FROM jobs j
GROUP BY month
ORDER BY month ASC;
""")

# 3. Top job titles
QUERY_TOP_TITLES = text("""
SELECT LOWER(title) AS title, COUNT(*) AS total
FROM jobs
GROUP BY LOWER(title)
ORDER BY total DESC
LIMIT 10;
""")

# 4. Salary distribution
QUERY_SALARY_STATS = text("""
SELECT salary FROM jobs WHERE salary IS NOT NULL;
""")
