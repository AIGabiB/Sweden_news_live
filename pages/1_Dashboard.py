import streamlit as st
import pandas as pd
from data.supabase_client2 import get_supabase
import plotly.express as px 
from datetime import timedelta

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

supabase = get_supabase() # connects to my supabase project

@st.cache_data(ttl=300)
def load_v_kpi_dashboard():# selects all 4 elements in VIEW "v_kpi_dashboard"
    return supabase.table("v_kpi_dashboard").select("*").execute().data[0] 

@st.cache_data(ttl=300)
def load_v_news_date_count(): # selects all rows from VIEW "v_news_date_count"
    return supabase.table("v_news_date_count").select("*").execute().data

@st.cache_data(ttl=300)
def load_v_hour_count_today(): # selects all rows from VIEW "v_hour_count_today"
    return supabase.table("v_hour_count_today").select("*").execute().data 

@st.cache_data(ttl=300)
def load_v_top5_news(): # selects all rows from VIEW "v_top5_news"
    return supabase.table("v_top5_news").select("*").execute().data 

kpi = load_v_kpi_dashboard()

delta = kpi["news_today"] - kpi["news_last_week"]

with st.sidebar:
    st.info("Historical data from April 19, 2024 to today. Updated continuously.")

col1,col2,col3,col4 = st.columns(4)

with col1: 
    st.metric("News Today", kpi["news_today"],delta=delta)
with col2:    
    st.metric("Same Day Last Week", kpi["news_last_week"])
with col3:
    st.metric("Top Region Today", kpi["most_active_regions"])
with col4:
    st.metric("Top Category Today", kpi["most_common_type"])


col1,col2 = st.columns(2)

with col1 : 
    date_count = load_v_news_date_count()

    date_count = pd.DataFrame(date_count)

    date_count["news_date"] = pd.to_datetime(date_count["news_date"])

    start_date = date_count["news_date"].min()
    end_date = date_count["news_date"].max()

    selected_dates = st.date_input(
        "Select interval",
        value=(end_date - timedelta(days=21), end_date),
        min_value=start_date,
        max_value=end_date)

    if len(selected_dates) == 2:

        start_val, end_val = selected_dates

        filtered_df = date_count[
            (date_count["news_date"].dt.date >= start_val) & 
            (date_count["news_date"].dt.date <= end_val) ]

        fig = px.line(filtered_df, x="news_date", y="news_count",title='News Count (Historical)',markers=True)
        fig.update_layout(
        height=280,  
        margin=dict(l=20, r=20, t=20, b=0),
        xaxis_title="Date",
        yaxis_title="Count",
        title_font_size=15)

        fig.update_xaxes(tickangle=45,dtick="D1",tickformat="%Y-%m-%d")

        st.plotly_chart(fig)

    else:
        st.info("Select both a start and end date in the calendar above.")

with col2: 
    hour_count_today = load_v_hour_count_today()

    hour_count_today_df = pd.DataFrame(hour_count_today)

    st.write("")
    st.write("")
    st.write("")

    fig = px.bar(
        hour_count_today_df, 
        x='Hour of day', 
        y='Total count', 
        title='News by Hour (Today)',
        color="Total count",
        color_continuous_scale='Blues',
        text_auto=True)

    fig.update_layout(
        height=300, 
        margin=dict(l=20, r=20, t=60, b=0),
        xaxis_title="Hour",
        yaxis_title="Count",
        title_font_size=15)

    fig.update_coloraxes(showscale=False)

    st.plotly_chart(fig)


top5_news = load_v_top5_news()

top5_news = pd.DataFrame(top5_news)

top5_news["datetime_display_utc"] = pd.to_datetime(top5_news["datetime_display_utc"])

# create new column "datetime_swe" by converting time in UTC to time in SWEDEN
top5_news["datetime_swe"] = (
    top5_news["datetime_display_utc"]
    .dt.tz_localize('UTC') 
    .dt.tz_convert('Europe/Stockholm') 
)

# creates red dot that blinks 
st.markdown("""
<style>
@keyframes pulse {
  from { opacity: 1; }
  to { opacity: 0; }
}
.blink-dot {
  color: red;
  font-size: 0.5em; 
  vertical-align: middle;
  animation: pulse 1.5s ease-in-out infinite alternate;
}
</style>

<h3>Live <span class="blink-dot">🔴</span></h3>
""", unsafe_allow_html=True)

for _, row in top5_news.iterrows(): # prints top 5 news 
    st.markdown(f"##### {row['summary']}")

    col1, col2, col3= st.columns([1.5,1.2,2])

    with col1:
        st.write(f"📍 {row['location_name']}, {row['location_city'] or 'Unknown'}")
    with col2:
        st.write(f"🕒 {row['event_date_str']}")
    with col3:
        st.write(f"🏷️ {row['type']}")

    st.caption(f"Fetched: {row['datetime_swe'].strftime('%Y-%m-%d %H:%M')}")