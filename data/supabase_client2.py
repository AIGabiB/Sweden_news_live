import streamlit as st
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("SU_URL")
key = os.getenv("SU_API_KEY")

@st.cache_resource
def get_supabase():
    return create_client(url, key)