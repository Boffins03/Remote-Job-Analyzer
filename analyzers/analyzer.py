import pandas as pd
import os

def load_jobs():
    # Path to the processed CSV
    filename = os.path.join("data", "processed", "jobs.csv")

    if not os.path.exists(filename):
        raise FileNotFoundError("Run parser.py first to generate jobs.csv")

    df = pd.read_csv(filename)
    return df

def analyze_jobs(df):
    print("Basic Job Market Insights")
    print("-" * 40)

    # Total jobs
    print(f"Total Jobs Collected: {len(df)}")

    # Top companies hiring
    print("\nTop 5 Companies hiring:")
    print(df['company'].value_counts().head())

    # Locations
    print("\nTop 5 Locations:")
    print(df['location'].value_counts().head())

    # Salary stats (cleaning just in case)
    if 'salary' in df.columns:
        df['min_salary'] = df['salary'].str.extract(r'(\d+)').astype(float)
        df['max_salary'] = df['salary'].str.extract(r'(\d+)\s*-\s*(\d+)')[1].astype(float)

        print("\nSalary Range Overview:")
        print(f"Average Min Salary: {df['min_salary'].mean():.2f}")
        print(f"Average Max Salary: {df['max_salary'].mean():.2f}")

if __name__ == "__main__":
    df = load_jobs()
    analyze_jobs(df)
