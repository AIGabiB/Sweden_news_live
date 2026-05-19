import streamlit as st

st.set_page_config(layout="wide")

st.markdown("""
<style>
html, body, [class*="css"]  {
    font-size: 12px;
}
.block-container {
    padding-top: 2.5rem;
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

spaces = "&nbsp;" * 30

st.markdown("""## AI-Powered Swedish News Intelligence

Stay updated with real-world events in Sweden through an interactive AI-driven platform that transforms raw news data into searchable insights and intelligent answers.

---

### What You Can Do

##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Ask Questions About Current Events
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Interact with an AI assistant that answers questions using real Swedish news and police event data.

##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Explore News Data
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Search, filter, and browse structured news articles from a continuously updated database.

##### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Discover Trends & Insights
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Analyze patterns, activity, and developments through interactive visualizations and analytics.
            
---
### How It Works

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This platform combines modern AI, data engineering, and visualization technologies to create an intelligent news exploration system:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Real-time data ingestion pipeline**<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; News data is continuously fetched from an external API (APIverket), processed, and stored in a PostgreSQL database (Supabase).            

            
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Semantic search (vector embeddings)**<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Converts Swedish news into high-dimensional embeddings using OpenAI, enabling meaning-based search instead of keyword matching.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Large Language Models (OpenAI GPT)**<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Used for question understanding, structured filtering (city, county, date)
            
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Retrival-Augmented Generation (RAG pipeline)**<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Retrieves relevant news from a Supabase vector database and uses a large language model (GPT) to generate contextual, natural language answers.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Interactive analytics layer (Streamlit + Plotly)**<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Provides dashboards, trend analysis, and visual exploration of historical and real-time news data.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Automated data updates (GitHub Actions)**<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; A scheduled workflow runs every hour to keep the dataset fresh and up to date without manual intervention.
            
Instead of manually reading through large volumes of news articles, you can ask direct questions and receive context-aware answers based on real events happening across Sweden.

---

### Data Source

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; News event data is retrieved from the Swedish Police event feed via the **APIverket API** (endpoint: /police/events).

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The dataset is automatically updated every hour using GitHub Actions to ensure fresh and continuously available information.
""", unsafe_allow_html=True)