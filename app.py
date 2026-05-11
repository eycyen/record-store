import streamlit as st
import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os
import requests

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
        print("Connected to the database successfully.")
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        st.stop()

# Establish database connection
conn = connect_to_database(db_config)

# Display the title of the Streamlit app
st.title("Record Store Database Interface")

@st.cache_data
def fetch_data(query):
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(results, columns=columns)
        return df
    except mysql.connector.Error as err:
        st.error(f"Error fetching data: {err}")
        return pd.DataFrame()  # Return an empty DataFrame on error
    
# Fetch albums with their formats and prices
query = f"""
    SELECT ar.Name, al.Title, v.Format, v.Price
    FROM ARTIST ar
    JOIN ARTIST_ALBUM aa ON ar.ArtistID = aa.ArtistID
    JOIN ALBUM al ON aa.AlbumID = al.AlbumID
    JOIN ALBUM_VARIANT v ON al.AlbumID = v.AlbumID;
    """

# Fetch data and store it in a DataFrame
df = fetch_data(query)

# Display albums in a grid layout
columns = st.columns(3)

# Function to fetch album cover from iTunes API
@st.cache_data
def fetch_album_cover(album_title,artist_name):
    try:
        response = requests.get(f"https://itunes.apple.com/search?term={artist_name}+{album_title}&entity=album&limit=5")
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                return data['results'][0]['artworkUrl100'].replace('100x100bb', '500x500bb')
        return None
    except Exception as e:
        print(f"Error fetching album cover: {e}")
        return None
    
# Display albums in a grid layout
for index, row in df.iterrows():
    with columns[index % 3]:
        st.subheader(f"{row['Name']} - {row['Title']} ({row['Format']})")
        st.write(f"Price: ${row['Price']}")
        cover_url = fetch_album_cover(row['Title'], row['Name'])
        if cover_url:
            st.image(cover_url, width=150)
        else:
            st.write("No cover available.")

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

