import streamlit as st
import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

# Database connection parameters
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME')
}

# Connect to the database
@st.cache_resource
def connect_to_database(config):
    try:
        conn = mysql.connector.connect(**config)
        st.success("Connected to the database successfully.")
        return conn
    except mysql.connector.Error as err:
        st.error(f"Error connecting to the database: {err}")
        st.stop()

# Establish database connection
conn = connect_to_database(db_config)

