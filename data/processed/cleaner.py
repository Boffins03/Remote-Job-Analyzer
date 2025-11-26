import pandas as pd
import numpy as np
import re

# =====================================================================
# Helper Functions
# =====================================================================

def clean_remoteok(df):
    # Clean encoding issues in "location"
    df["location"] = (
        df["location"]
        .astype(str)
        .str.encode("utf-8", "ignore")
        .str.decode("utf-8", "ignore")
    )

    df["location"] = df["location"].replace(
        {
            "Ã¢Â€Â": "",
            "Ã¢Â€Â“": ",",
            "Ã¢": ",",
            "Â": "",
            "/": ",",
            "-": ","
        },
        regex=True
    ).str.strip()

    df["location"] = df["location"].replace("nan", "Remote")

    # Extract salary min/max
    df["salary_min"] = df["salary"].str.extract(r"(\d[\d,]*)\s*[-–]").astype(float)
    df["salary_max"] = df["salary"].str.extract(r"[-–]\s*(\d[\d,]*)").astype(float)

    # Average
    df["salary_avg"] = df[["salary_min", "salary_max"]].mean(axis=1)

    mean_salary = int(df.loc[df["salary_avg"] > 0, "salary_avg"].mean())
    df["salary"] = df["salary_avg"].replace(0, mean_salary).astype(int)

    df = df.drop(columns=["salary_min", "salary_max", "salary_avg"])
    df.dropna(subset=["title"], inplace=True)

    df = df[["title", "company", "location", "salary", "apply_link"]]
    df["source"] = "remoteok"

    return df


# ---------------------------------------------------------------------

def extract_location_list_remotely(text):
    if not isinstance(text, str) or text.strip() == "":
        return []

    # extract text after USD
    match = re.search(r"USD\s*(.*)", text)
    if match:
        loc_text = match.group(1)
    else:
        match2 = re.search(r"(?:Full-Time|Contract)\s*(.*)", text)
        loc_text = match2.group(1) if match2 else ""

    loc_text = loc_text.strip()
    loc_text = re.sub(r"[^\w\s,]", "", loc_text)

    if loc_text == "":
        return []

    if "Anywhere in the World" in loc_text:
        return ["Anywhere in the World"]

    # split words
    return [x.strip() for x in loc_text.split() if x.strip()]


def clean_salary(value):
    if not isinstance(value, str):
        return None

    value = value.replace(",", "")
    nums = re.findall(r"\$(\d+)", value)

    if len(nums) == 2:
        low, high = map(int, nums)
        return int((low + high) / 2)

    if len(nums) == 1:
        return int(nums[0])

    return None


def clean_remotely(df):
    df.dropna(subset=["title"], inplace=True)

    # Extract salary (raw)
    df["salary"] = df["categories"].str.extract(
        r"(\$\d{1,3}(?:,\d{3})*(?:\s*-\s*\$\d{1,3}(?:,\d{3})*)?\s*(?:or more)?\s*USD)"
    )

    # Parse salary
    df["salary_cleaned"] = df["salary"].apply(clean_salary).astype("Int64")

    mean_salary = int(df["salary_cleaned"].mean())
    df["salary_cleaned"].fillna(mean_salary, inplace=True)

    # Parse location
    df["location"] = df["categories"].apply(extract_location_list_remotely)

    df["location_cleaned"] = df["location"].apply(
        lambda loc: "Remote" if "Anywhere in the World" in loc else ", ".join(loc)
    )

    df = df.drop(columns=["categories", "salary", "company_location"], errors="ignore")

    df["salary"] = df["salary_cleaned"]
    df["location"] = df["location_cleaned"]

    df = df.drop(columns=["salary_cleaned", "location_cleaned"])

    df = df[["title", "company", "location", "salary, apply_link"]]
    df["source"] = "remotely"

    return df

# =====================================================================
# Main Script
# =====================================================================

def main():
    print("Loading CSV files...")
    remoteok = pd.read_csv("jobs_remoteok.csv")
    remotely = pd.read_csv("jobs_weworkremotely.csv")

    print("Cleaning RemoteOK...")
    remoteok_clean = clean_remoteok(remoteok)

    print("Cleaning WeWorkRemotely...")
    remotely_clean = clean_remotely(remotely)

    print("Merging...")
    jobs = pd.concat([remoteok_clean, remotely_clean], ignore_index=True)

    print("Removing duplicates...")
    jobs = jobs.drop_duplicates(subset=["title", "company"], keep="first").reset_index(drop=True)

    print("Saving jobs_clean.csv...")
    jobs.to_csv("jobs_clean.csv", index=False)

    print("✔ Done! jobs_clean.csv generated.")


if __name__ == "__main__":
    main()
