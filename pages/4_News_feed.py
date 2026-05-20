import streamlit as st
import pandas as pd
from data.supabase_client2 import get_supabase # self created function to connect to my supabase project

st.set_page_config(layout="wide") # set page to wide

st.markdown("""
<style>
html, body, [class*="css"]  {
    font-size: 14px;
}
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True) # used to reduce font size and padding on top and bottom

@st.cache_data(ttl=300)
def load_news(): # select all data in table "cleaned_news"
    return supabase.table("cleaned_news").select("*").order("datetime_display_utc",desc=True).execute().data 

with st.sidebar:
    st.info("Historical data from April 19, 2024 to today. Updated continuously.")

supabase = get_supabase() # connects to my supabase project

data = load_news() 

df = pd.DataFrame(data) # convert table data to pandas DataFrame

df["location_city"] = df["location_city"].replace("","Unknown City") 

df["datetime_display_utc"] = pd.to_datetime(df["datetime_display_utc"])

# create new column "datetime_swe" by converting time in UTC to time in SWEDEN
df["datetime_swe"] = (
    df["datetime_display_utc"]
    .dt.tz_localize('UTC') 
    .dt.tz_convert('Europe/Stockholm')) 


col1, col2, col3, col4 = st.columns(4)

with col1:
    selected_type = st.selectbox("Type", ["All"] + sorted(df["type"].dropna().unique())) # show type choices  

with col2:
    selected_lan = st.selectbox("Län", ["All"] + sorted(df["location_name"].dropna().unique())) # show county choices 

with col3:
    selected_city = st.selectbox("City", ["All"] + sorted(df["location_city"].dropna().unique())) # show city choices 

with col4:
    search = st.text_input("Search") # text cell for searching news


filtered_df = df.copy()

if selected_type != "All":
    filtered_df = filtered_df[filtered_df["type"] == selected_type] # filter by type

if selected_lan != "All":
    filtered_df = filtered_df[filtered_df["location_name"] == selected_lan] # filter by county

if selected_city != "All":
    filtered_df = filtered_df[filtered_df["location_city"] == selected_city] # filter by city

if search:
    filtered_df = filtered_df[
        filtered_df["summary"].str.contains(search, case=False, na=False)
    ] # filter by user text 

col1,col2 = st.columns([1,0.17])

with col2:
    page_size = 10
    page = st.number_input("Page", min_value=1, step=1) # get page number

    start = (page - 1) * page_size
    end = start + page_size

    page_df = filtered_df.iloc[start:end] # cut data, depending on selected page


for _, row in page_df.iterrows(): # show news row-wise 

    st.markdown(f"""
    ##### {row['summary'][:100]}  
    📍 {row["location_city"]}, {row['location_name']}  
    🕒 {row['event_date_str']}  
    🏷️ {row['type']}
    """)
    
    st.caption(f"Fetched: {row['datetime_swe'].strftime('%Y-%m-%d %H:%M')}")
