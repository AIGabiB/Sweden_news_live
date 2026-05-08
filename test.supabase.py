import requests
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

url = os.environ.get("SU_URL")
key = os.environ.get("SU_API_KEY")
API_KEY = os.environ.get("API_KEY")


URL = "https://apiverket.se/v1/police/events"
HEADERS = {"Authorization": API_KEY} 


response2 = requests.get(URL, headers=HEADERS,params={"limit":30})


api_news = response2.json()["data"]["events"]

supabase = create_client(url, key)

df = pd.DataFrame(api_news)

exclude_types = [
    "Sammanfattning natt",
    "Övrigt",
    "Sammanfattning kväll och natt"
]

df = df[~df["type"].isin(exclude_types)]

def clean_data(df):
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True)

    df["datetime_display_utc"] = df["datetime"].dt.strftime("%Y-%m-%d %H:%M:%S")

    df["event_date_str"] = df["name"].str.split(",").str[0].str.strip()


    split_col = df["name"].str.split(",")
    
    df["location_city"] = np.where(
    ~split_col.str[-1].str.contains("län", na=False, case=False),
    split_col.str[-1].str.strip(),
    "")

    df = df.drop(columns=["name","datetime","latitude","longitude","url"])

    return df

df_cleaned = clean_data(df)

data_dict = df_cleaned.to_dict(orient="records")

supabase.table("cleaned_news").upsert(data_dict).execute()