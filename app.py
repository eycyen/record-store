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

# Execute the selected query based on user input
if selected_query == "List all tracks in a specific album":
    album_id = st.number_input("Enter Album ID:", min_value=1, step=1)
    query = f"""
    SELECT t.TrackID, t.Title, t.Duration
    FROM TRACK t
    WHERE t.AlbumID = {album_id};
    """
    execute_query(query)

elif selected_query == "Find all albums made by a specific artist":
    artist_id = st.number_input("Enter Artist Id:", min_value=1, step=1)
    query = f"""
        SELECT ar.Name AS Artist_Name, al.Title AS Album_Title, al.Genre
        FROM ARTIST ar
        JOIN ARTIST_ALBUM aa ON ar.ArtistID = aa.ArtistID
        JOIN ALBUM al ON aa.AlbumID = al.AlbumID
        WHERE ar.ARTISTID = {artist_id};
    """
    execute_query(query)

elif selected_query == "Show stock levels and prices for each album":
    query = """
        SELECT al.Title AS Album_Title, v.Format, v.StockQuantity, v.Price
        FROM ALBUM al
        JOIN ALBUM_VARIANT v ON al.AlbumID = v.AlbumID;
    """
    execute_query(query)

elif selected_query == "Calculate total amount spent by each customer":
    query = """
        SELECT c.FirstName, c.LastName AS Customer_Name, SUM(oi.Quantity * oi.UnitPrice) AS Total_Spent
        FROM CUSTOMER c
        JOIN CUSTOMER_ORDER co ON c.CustomerID = co.CustomerID
        JOIN ORDER_ITEM oi ON co.OrderID = oi.OrderID
        GROUP BY c.CustomerID;
    """
    execute_query(query)

elif selected_query == "Detailed order summary showing products inside an order":
    order_id = st.number_input("Enter Order ID:", min_value=1, step=1)
    query = f"""
        SELECT co.OrderID, c.FirstName, c.LastName AS Customer_Name, v.Format, oi.Quantity, oi.UnitPrice
        FROM CUSTOMER_ORDER co
        JOIN CUSTOMER c ON co.CustomerID = c.CustomerID
        JOIN ORDER_ITEM oi ON co.OrderID = oi.OrderID
        JOIN ALBUM_VARIANT v ON oi.VariantID = v.VariantID
        WHERE co.OrderID = {order_id};
    """
    execute_query(query)

