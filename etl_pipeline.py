import requests
import pandas as pd
from datetime import datetime
from data.supabase_client import get_supabase

now = datetime.now()

date_str = now.strftime("%Y-%m-%d")

URL  = "https://polisen.se/api/events" 

response2 = requests.get(url=URL,params={"DateTime": date_str})

api_news = response2.json() 

df = pd.DataFrame(api_news)


def clean_data2(df):

    df["datetime_display_utc"] = pd.to_datetime(df["datetime"], utc=True)

    df["event_date_str"] = df["name"].str.split(",").str[0]

    df["location_name"] = df["location"].apply(lambda x: x["name"])

    df["location_city"] = df["name"].str.split(",").str[2]

    mask = df["location_city"].str.contains(" län")

    df.loc[mask, "location_city"] = ""

    mask = df["type"] == "Sammanfattning natt"

    df = df[~mask]

    df = df.sort_values(by="datetime_display_utc", ascending=False)

    df = df.drop(columns=["location","url","datetime","name"])

    df["datetime_display_utc"] = df["datetime_display_utc"].astype(str)

    df = df[["id","datetime_display_utc","event_date_str","location_city","summary","type","location_name"]]

    return df


supabase = get_supabase()

df_clean = clean_data2(df)

data_dict = df_clean.to_dict(orient="records")

supabase.table("cleaned_news").upsert(data_dict).execute()
