import requests
import pandas as pd
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")


# SETTINGS
URL = "https://apiverket.se/v1/police/events"
HEADERS = {"Authorization": API_KEY} 

DB_PATH = r"C:\Users\gabib\test_apiverket\events.db"


# 1. Get API-data
response = requests.get(URL, headers=HEADERS,params={"limit":30})

if response.status_code != 200:
    print("API error:", response.status_code)
    with open("log.txt", "a") as f:
        f.write(f"ERROR {datetime.now()} | status: {response.status_code}\n")
    exit()

api_news = response.json()["data"]["events"]


# 2. Connect to DB
conn = sqlite3.connect(DB_PATH)

# Create table "events_table" if not excited 
conn.execute("""
CREATE TABLE IF NOT EXISTS events_table (
    id INTEGER PRIMARY KEY,
    datetime TEXT,
    name TEXT,
    summary TEXT,
    type TEXT,
    location_name TEXT,
    latitude REAL,
    longitude REAL
)
""")


# 3. Get exicting IDs from table
existing = set(pd.read_sql("SELECT id FROM events_table", conn)["id"])


# 4. Filter new data, by compering "id" in api_news with existing "id" in events_table
new_data = [e for e in api_news if e["id"] not in existing]


# 5. Save new data from API to "events_table"
if new_data:
    df_new = pd.DataFrame(new_data)

    # Keeps only these columns:
    df_new = df_new[
        ["id", "datetime", "name", "summary", "type", "location_name", "latitude", "longitude"]
    ]

    df_new["datetime"] = df_new["datetime"].str.split(" ").str[:2].str.join(" ")
    df_new["datetime"] = pd.to_datetime(df_new["datetime"])

    df_new.to_sql("events_table", conn, if_exists="append", index=False)

    
    print(f"{len(new_data)} new rows saved")

else:
    print("NO new data")



# 6. Create log file: "log.txt"
with open("log.txt", "a") as f:
    f.write(f"{datetime.now()} | new: {len(new_data)}\n")

conn.close()