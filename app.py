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

# Display the title of the Streamlit app
st.title("Record Store Database Interface")

# Sidebar for query selection
st.sidebar.header("Database Queries")
query_options = [
    "List all tracks in a specific album",
    "Find all albums made by a specific artist",
    "Show stock levels and prices for each album",
    "Calculate total amount spent by each customer",
    "Detailed order summary showing products inside an order"
]
selected_query = st.sidebar.selectbox("Select a query to execute:", query_options)

# Function to execute the selected query
def execute_query(query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(results, columns=columns)
        st.dataframe(df)
    except mysql.connector.Error as err:
        st.error(f"Error executing query: {err}")