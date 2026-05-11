import requests
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import os
from supabase import create_client
from openai import OpenAI

load_dotenv() # load .env file, (contains API keys)

url = os.environ.get("SU_URL") # get url for my supabase project url
key = os.environ.get("SU_API_KEY") # get API KEY for supabase
API_KEY = os.environ.get("API_KEY") # get API KEY for apiverket (where I do data extraction)
OPEN_AI_KEY = os.environ.get("AI_KEY") # get openai key


URL = "https://apiverket.se/v1/police/events" # url for data extraction
HEADERS = {"Authorization": API_KEY} 

response2 = requests.get(URL, headers=HEADERS,params={"limit":25}) # get 30 of the most recent news

api_news = response2.json()["data"]["events"] # indexing through respone to get the data by rows

supabase = create_client(url, key) # connect to my supabase
client = OpenAI(api_key=OPEN_AI_KEY) # connect to openai api


def clean_data(df): # data cleaning function, that extracts relevant columns and removes irrelevant columns 

    exclude_types = [
    "Sammanfattning natt",
    "Övrigt",
    "Sammanfattning kväll och natt"
] 

    df = df[~df["type"].isin(exclude_types)] # remove rows where "type" isin exclude_types

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


df = pd.DataFrame(api_news) # convert to pandas Dataframe for data cleaning

df_cleaned = clean_data(df) # apply clean_data() to df

data_dict = df_cleaned.to_dict(orient="records") # convert df_cleaned to dict, row-wise and not column-wise

supabase.table("cleaned_news").upsert(data_dict).execute() # upsert new news to table "cleaned_news" where all news are stored


table = supabase.table("cleaned_news").select("*").is_("embedding",None).execute() # get rows where "embedding" is None, so I can embed it.
df_table = pd.DataFrame(table.data) # converting from json to pandas Dataframe

df_table["location_city"] = df_table["location_city"].replace(
    ["None", "none", "", "NULL", None],
    np.nan ) # some of the cells in location_city is EMPTY, so I replaced it with np.nan

def build_text(row): # this function will be used to create embedding_text for each row
    return f"""
    datum: {row ["event_date_str"]}
    stad: {row["location_city"] or 'okänd'}
    region: {row["location_name"]}
    typ: {row["type"]}
    
    sammanfattning: {row["summary"]}
    """

df_table["embedding_text"] = df_table.apply(build_text, axis=1) # applying build_text for each row and save it in new column "embedding_text"



def create_embedding (df_table,client,batch_size = 100): # creates embeddings from column "embedding_text" by model: text-embedding-3-small

    embeddings = []

    for i in range(0, len(df_table), batch_size):

        batch = df_table["embedding_text"].iloc[i:i + batch_size].tolist()

        response = client.embeddings.create(
            input=batch,
            model="text-embedding-3-small")

        batch_embedding = [item.embedding for item in response.data]
        embeddings.extend(batch_embedding) 

    return embeddings 


df_table["embedding"] = create_embedding(df_table= df_table, client= client) # call the function create_embedding() to create embedding and save it in column "embedding"


def upsert_embedding_to_supabase(df_table,supabase ,batch_size = 200): # upserts columns "embedding_text" and "embedding" to supabase table

    for i in range(0, len(df_table), batch_size):

        batch_df = df_table.iloc[i:i+batch_size]

        data = [
            {
                "id": row["id"],
                "embedding_text": row["embedding_text"],
                "embedding": row["embedding"],
                "location_city": None if pd.isna(row["location_city"]) else row["location_city"]
            }
            for _, row in batch_df.iterrows()
        ]

        supabase.table("cleaned_news").upsert(data).execute()


upsert_embedding_to_supabase(df_table=df_table, supabase=supabase)
