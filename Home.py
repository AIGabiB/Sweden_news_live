import streamlit as st

st.set_page_config(layout="wide")

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
""", unsafe_allow_html=True)

st.markdown("""
## AI-Powered Swedish News Intelligence

Explore real-time Swedish news and police event data through AI-powered search, analytics, and interactive visualizations.

---

### Pages

**Home**  
Overview of the platform and technologies

**Dashboard**  
View key metrics, charts, and the latest news updates in real time.

**Chatbot**  
Ask questions about Swedish news using natural language and receive AI-generated answers based on real events.

**Analytics**  
Analyze historical trends and patterns through interactive visualizations.

**News Feed**  
Search, filter, and browse all collected news articles from the database.

---

### Technologies

- OpenAI GPT + Embeddings
- Retrieval-Augmented Generation (RAG)
- Supabase Vector Database
- Streamlit + Plotly
- GitHub Actions automation

---

### Data Source

News event data is retrieved from the Swedish Police event feed via the **APIverket API (endpoint: /police/events)** and updated automatically every hour.
""")