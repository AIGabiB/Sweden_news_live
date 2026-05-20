import streamlit as st
import pandas as pd
from data.supabase_client2 import get_supabase
import plotly.express as px 

st.set_page_config(layout="wide") # set page to wide

st.markdown("""
<style>
html, body, [class*="css"]  {
    font-size: 16px;
}
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True) # used to reduce font size and padding on top and bottom

@st.cache_data(ttl=300)
def load_v_hour_count(): # select all rows in VIEW "v_hour_count"
    return supabase.table("v_hour_count").select("*").execute().data 

@st.cache_data(ttl=300)
def load_city_incident_summary(): # select all rows from VIEW "city_incident_summary", limit 10 row
    return supabase.table("city_incident_summary").select("*").limit(10).execute().data 

@st.cache_data(ttl=300)
def load_v_type_count(): # select all rows from VIEW "v_type_count", limit 10 row
    return supabase.table("v_type_count").select("*").limit(10).execute().data 

@st.cache_data(ttl=300)
def load_v_news_locationname_count(): # select all rows from VIEW "v_news_locationname_count", limit 10 row
    return  supabase.table("v_news_locationname_count").select("*").limit(10).execute().data 


with st.sidebar:
    st.info("Historical data from April 19, 2024 to today. Updated continuously.")

supabase = get_supabase() # connects to my supabase project

hour_count = load_v_hour_count()

hour_count= pd.DataFrame(hour_count)

all_hours = [f"{h:02d}:00" for h in range(24)] # list with all hours as elements

template_df = pd.DataFrame({'hour_of_day': all_hours})

hour_count_complete = pd.merge(template_df, hour_count, on='hour_of_day', how='left') # merge between template_df and hour_count by column: 'hour_of_day'

hour_count_complete['total_count'] = hour_count_complete['total_count'].fillna(0).astype(int) # fill na with 0 

# cut hour hour_count_complete in two pieces
df_first_half = hour_count_complete.iloc[:12]
df_second_half = hour_count_complete.iloc[12:]


col1,col2 = st.columns(2)

with col1:
    st.markdown("#### Hourly Activity (00:00–11:00)")
    fig = px.line_polar(df_first_half, r='total_count', theta='hour_of_day', line_close=True, template="plotly_dark")
    fig.update_traces(fill='toself',line_color="#b18e01")
    fig.update_layout(height=250,
                      polar=dict(radialaxis=dict(range=[hour_count_complete["total_count"].min(), hour_count_complete["total_count"].max()])),
                      margin=dict(t=20,b=20))
    
    st.plotly_chart(fig)

with col2:
    st.markdown("#### Hourly Activity (12:00–23:00)")

    fig = px.line_polar(df_second_half, r='total_count', theta='hour_of_day', line_close=True, template="plotly_dark")

    fig.update_traces(fill='toself',line_color="#080EAD")

    fig.update_layout(height=250,
                      polar=dict(
                      radialaxis=dict(range=[hour_count_complete["total_count"].min(), hour_count_complete["total_count"].max()])),
                      margin=dict(t=20,b=20))
    
    st.plotly_chart(fig)

st.markdown("""
**Time Patterns**
- Activity is noticeably higher during the afternoon and evening.
- Most events tend to occur after midday.
""")

st.write("---")

st.markdown("#### Count Per Category (Top 10)")

svar = st.selectbox("Choose one:",["Count per City","Count per Type","Count per Region"],index = 0)

if svar == "Count per City":
    city_count = load_city_incident_summary()

    city_count_df = pd.DataFrame(city_count).sort_values(by="total_incidents",ascending=True)

    city_count_df = city_count_df.replace("", pd.NA)

    fig = px.bar(city_count_df, y = "location_city", x = "total_incidents",color= "total_incidents",color_continuous_scale= "Reds",text_auto=True,orientation="h")
    
    fig.update_coloraxes(showscale=False)
    
    fig.update_layout(height=300, 
                      margin=dict(t=0,b=0), 
                      xaxis_title="Count", 
                      yaxis_title="City")
    
    fig.update_xaxes(tickangle=45)
    
    st.plotly_chart(fig,key="Count per City")

    st.markdown("""
    **Distribution**
    - Activity decreases gradually across smaller cities.
    """)

elif svar == "Count per Type":

    type_count = load_v_type_count()

    type_count_df = pd.DataFrame(type_count).sort_values(by="count",ascending=True)

    fig = px.bar(type_count_df, x="count", y="type", orientation="h", text="count", color="count", color_continuous_scale="Reds")

    fig.update_layout(height=300, 
                      xaxis_title="Count", 
                      yaxis_title="Categori", 
                      margin=dict(l=160,t=0,b=0), 
                      yaxis=dict(automargin=False))
    
    fig.update_coloraxes(showscale=False)

    st.plotly_chart(fig,key="Count per Type")

    st.markdown("""
    **Incident Overview**
    - Traffic-related incidents are the most common category by a clear margin.
    - Other incident types are present at lower and more even levels across categories.
    """)

elif svar == "Count per Region":

    response = load_v_news_locationname_count()
    
    response = pd.DataFrame(response).sort_values(by="count",ascending=True)

    fig = px.bar(response, x="count", y="location_name", orientation="h", text="count", color="count", color_continuous_scale="Reds")

    fig.update_layout(height=300, 
                      xaxis_title="Count", 
                      yaxis_title="Region", 
                      margin=dict(l=138,t=0,b=0), 
                      yaxis=dict(automargin=False))
    
    fig.update_coloraxes(showscale=False)
    
    st.plotly_chart(fig,key="Count per Region")

    st.markdown("""
    **Geographic Patterns**
    - A few regions dominate overall activity.
    - Events are concentrated in  densely populated cities.
    """)