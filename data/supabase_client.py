from supabase import create_client
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

url = st.secrets.get("SU_URL") or os.getenv("SU_URL")
key = st.secrets.get("SU_API_KEY") or os.getenv("SU_API_KEY")


def get_supabase():
    return create_client(url, key)