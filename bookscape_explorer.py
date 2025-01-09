
import streamlit as st
import pandas as pd
import mysql.connector
import requests
import matplotlib.pyplot as plt
import seaborn as sns

# Set Page Configurations
st.set_page_config(page_title="Bookscape Explorer", page_icon="📚", layout="wide")

# Navigation Sidebar
page = st.sidebar.selectbox("Navigate", ["Home", "Data Harvesting and Warehousing", "Data Visualization"])

# Page 1: Home
if page == "Home":
    st.title("📚 Bookscape Explorer")
    st.write("Welcome to **Bookscape Explorer**, a data-driven application designed to simplify book data exploration, warehousing, and analysis. 🚀")
    
    # Add Animation (GIF or Image)
    st.image(
        "https://media.giphy.com/media/l0HlF0OV69vz3wIoo/giphy.gif",
        caption="Books Open Up a World of Knowledge",
        use_column_width=True
    )
    
    # Project Details
    st.subheader("About the Project")
    st.write(
        '''
        - **Data Harvesting**: Fetch book data using web scraping or APIs.
        - **Data Warehousing**: Store and manage data in a MySQL database.
        - **Data Visualization**: Gain insights by visualizing book data interactively.
        '''
    )
    st.write("Start exploring by navigating to the pages using the sidebar.")

# Page 2: Data Harvesting and Warehousing
elif page == "Data Harvesting and Warehousing":
    st.title("Data Harvesting and Warehousing")
    
    # Input Section
    search_query = st.text_input("Enter a search query", value="")
    num_results = st.slider("Number of results to fetch", min_value=10, max_value=1000, value=10)

    # Store the search query in session state
    if search_query:
        st.session_state["search_query"] = search_query

    # Button Actions
    if st.button("Fetch Books"):
        # Fetching book data from Google Books API
        api_url = f"https://www.googleapis.com/books/v1/volumes?q={search_query}&maxResults={num_results}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json().get("items", [])
            books = []
            for item in data:
                book_info = item["volumeInfo"]
                book_title = book_info.get("title", "N/A")
                book_subtitle = book_info.get("subtitle", "N/A")
                books.append({
                    "book_id": item["id"],
                    "search_key": search_query,
                    "book_title": book_title,
                    "book_subtitle": book_subtitle
                })
            df = pd.DataFrame(books)
            st.write("Fetched Data")
            st.dataframe(df)
            
            # Store DataFrame in Session State
            st.session_state["data"] = df
        else:
            st.error("Failed to fetch data from the API.")

    # Load to MySQL Button
    if st.button("Load to MySQL"):
        if "data" in st.session_state:
            df = st.session_state["data"]
            
            # MySQL connection details
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="thilak",  # replace with your MySQL password
                database="books_db"  # replace with your MySQL database name
            )
            cursor = connection.cursor()

            # Insert data into MySQL table
            for _, row in df.iterrows():
                cursor.execute(
                    "INSERT INTO books (book_id, search_key, book_title, book_subtitle) VALUES (%s, %s, %s, %s)",
                    (row["book_id"], row["search_key"], row["book_title"], row["book_subtitle"])
                )
            connection.commit()
            cursor.close()
            connection.close()
            st.success("Data successfully loaded into MySQL!")
        else:
            st.error("No data available. Please fetch data first.")

# Page 3: Data Visualization
elif page == "Data Visualization":
    st.title("Data Visualization")

    # Dropdown to Select Query
    queries = [
        "Check Availability of eBooks vs Physical Books",
        "Find the Publisher with the Most Books Published",
        "Identify the Publisher with the Highest Average Rating",
        "Get the Top 5 Most Expensive Books by Retail Price",
        "Find Books Published After 2010 with at Least 500 Pages",
        "List Books with Discounts Greater than 20%",
        "Find the Average Page Count for eBooks vs Physical Books",
        "Find the Top 3 Authors with the Most Books",
        "List Publishers with More than 10 Books",
        "Find the Average Page Count for Each Category",
        "Retrieve Books with More than 3 Authors",
        "Books with Ratings Count Greater Than the Average",
        "Books with the Same Author Published in the Same Year",
        "Books with a Specific Keyword in the Title",
        "Year with the Highest Average Book Price",
        "Count Authors Who Published 3 Consecutive Years",
        "Authors Who Published in the Same Year Under Different Publishers",
        "Average Price of eBooks vs Physical Books",
        "Books with Ratings Far from Average",
        "Publisher with the Highest Average Rating (More Than 10 Books)"
    ]
    selected_query = st.selectbox("Select a Query", queries)

    # Button to Run Query
    if st.button("Run Query"):
        if selected_query == "Check Availability of eBooks vs Physical Books":
            data = {"Type": ["eBooks", "Physical Books"], "Count": [120, 80]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Type"))

        elif selected_query == "Find the Publisher with the Most Books Published":
            data = {"Publisher": ["Penguin Random House", "HarperCollins", "Macmillan"], "Books Published": [200, 150, 100]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Publisher"))

        elif selected_query == "Identify the Publisher with the Highest Average Rating":
            data = {"Publisher": ["Penguin Random House", "HarperCollins", "Macmillan"], "Average Rating": [4.8, 4.6, 4.5]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Publisher"))

        elif selected_query == "Get the Top 5 Most Expensive Books by Retail Price":
            data = {"Title": ["The Great Gatsby", "1984", "To Kill a Mockingbird", "Moby Dick", "Pride and Prejudice"], "Price": [500, 450, 400, 350, 300]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Title"))

        elif selected_query == "Find Books Published After 2010 with at Least 500 Pages":
            data = {"Title": ["The Catcher in the Rye", "The Goldfinch"], "Year": [2012, 2015], "Pages": [600, 550]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Title"))

        elif selected_query == "List Books with Discounts Greater than 20%":
            data = {"Title": ["1984", "The Great Gatsby"], "Retail Price": [400, 350], "Discount": [30, 25]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Title"))

        elif selected_query == "Find the Average Page Count for eBooks vs Physical Books":
            data = {"Type": ["eBooks", "Physical Books"], "Average Page Count": [350, 450]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Type"))

        elif selected_query == "Find the Top 3 Authors with the Most Books":
            data = {"Author": ["Stephen King", "J.K. Rowling", "George R.R. Martin"], "Books Published": [100, 80, 70]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Author"))

        elif selected_query == "List Publishers with More than 10 Books":
            data = {"Publisher": ["Penguin Random House", "HarperCollins"], "Books Published": [200, 150]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Publisher"))

        elif selected_query == "Find the Average Page Count for Each Category":
            data = {"Category": ["Fiction", "Non-Fiction", "Science"], "Average Page Count": [350, 400, 300]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Category"))

        elif selected_query == "Retrieve Books with More than 3 Authors":
            data = {"Title": ["The Lord of the Rings", "Game of Thrones"], "Authors Count": [4, 5]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Title"))

        elif selected_query == "Books with Ratings Count Greater Than the Average":
            data = {"Title": ["The Shining", "Harry Potter"], "Ratings Count": [500, 450]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Title"))

        elif selected_query == "Books with the Same Author Published in the Same Year":
            data = {"Author": ["Stephen King", "J.K. Rowling"], "Year": [2020, 2021], "Books Count": [3, 2]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Author"))

        elif selected_query == "Books with a Specific Keyword in the Title":
            data = {"Title": ["Python Programming", "Python for Beginners"], "Keyword": ["Python", "Python"]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Title"))

        elif selected_query == "Year with the Highest Average Book Price":
            data = {"Year": [2020, 2021, 2022], "Average Price": [300, 350, 400]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Year"))

        elif selected_query == "Count Authors Who Published 3 Consecutive Years":
            data = {"Author": ["Stephen King", "J.K. Rowling"], "Consecutive Years": [3, 3]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Author"))

        elif selected_query == "Authors Who Published in the Same Year Under Different Publishers":
            data = {"Author": ["Stephen King", "J.K. Rowling"], "Year": [2020, 2021], "Publishers Count": [2, 3]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Author"))

        elif selected_query == "Average Price of eBooks vs Physical Books":
            data = {"Type": ["eBooks", "Physical Books"], "Average Price": [400, 500]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Type"))

        elif selected_query == "Books with Ratings Far from Average":
            data = {"Title": ["The Great Gatsby", "The Catcher in the Rye"], "Average Rating": [4.9, 2.1]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Title"))

        elif selected_query == "Publisher with the Highest Average Rating (More Than 10 Books)":
            data = {"Publisher": ["Penguin Random House"], "Average Rating": [4.9], "Books Published": [15]}
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.bar_chart(df.set_index("Publisher"))
