import streamlit as st
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
import asyncio
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv
from os import getenv


# Initialize connection.
# @st.cache_resource
def init_connection():
    opts = ClientOptions().replace(schema="data_entry")
    try:
        load_dotenv()
        url = getenv("SUPA_URL")
        key = getenv("SUPA_KEY")
        return create_client(url, key, options=opts)
    except:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key, options=opts)


async def log_in(_conn, credentials):
    # credentials is a json containing the following structure:
    # {"email": "email@example.com", "password": "example-password"}
    response = await _conn.auth.sign_in_with_password(credentials)
    asyncio.sleep(3)
    return response

# Perform query.
# Uses st.cache_resource to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_select(_conn, _table_name, atributes):
    return _conn.table(_table_name).select(atributes).execute()

# Perform insert.
@st.cache_data(ttl=600)
def run_insert(_conn, _table_name, values):
    return _conn.table(_table_name).insert(values, returning='minimal').execute()


# Get data from a view in Supabase and return it as a DataFrame.
# @st.cache_data(ttl=600)
def load_data(_conn, view_name):
    response = _conn.table(view_name).select('*').execute()
    df_response = pd.DataFrame(response.data[:])
    if 'dia' in df_response.columns: # quick fix, maybe this shouldn't be inside the loader func? This should be usable for any view/table
        df_response['dia'] = pd.to_datetime(df_response['dia']).dt.date.astype('datetime64[ns]')
    return df_response






