
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the cleaned data
books_df = pd.read_json('cleaned_books_data.json')

# Streamlit title
st.title("Bookscape Explorer")

# Sidebar Filters
st.sidebar.header("Filters")

# Filter by categories
categories = books_df['categories'].dropna().unique()
selected_category = st.sidebar.selectbox("Select Category", categories)

# Filter by eBook vs Physical Book
ebook_option = st.sidebar.selectbox("Select eBook or Physical Book", ['All', 'eBook', 'Physical Book'])

# Filter books by year range
min_year, max_year = int(books_df['year'].min()), int(books_df['year'].max())
selected_year = st.sidebar.slider('Select Year Range', min_year, max_year, (min_year, max_year))

# Apply filters
filtered_books = books_df[
    books_df['categories'].str.contains(selected_category, na=False)
]
if ebook_option == 'eBook':
    filtered_books = filtered_books[filtered_books['isEbook'] == True]
elif ebook_option == 'Physical Book':
    filtered_books = filtered_books[filtered_books['isEbook'] == False]

filtered_books = filtered_books[(filtered_books['year'] >= selected_year[0]) & (filtered_books['year'] <= selected_year[1])]

# Query selection box
st.sidebar.header("Select a Query to Run")
query_options = [
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
    "Authors Who Published Books in the Same Year but Under Different Publishers",
    "Average Retail Price of eBooks vs Physical Books",
    "Books with an Average Rating More Than Two Standard Deviations Away from the Overall Average Rating",
    "Publisher with the Highest Average Rating (More Than 10 Books)"
]

selected_query = st.sidebar.selectbox("Select a Query", query_options)

# Search functionality
search_query = st.text_input("Search for a Book by Title")
search_button = st.button("Search")

if search_button and search_query:
    search_results = filtered_books[filtered_books['book_title'].str.contains(search_query, case=False, na=False)]
    st.write(f"Found {len(search_results)} book(s) matching '{search_query}'")
    st.dataframe(search_results[['book_title', 'book_authors', 'year', 'categories']])

# Execute the selected query
execute_button = st.button("Execute Query")

if execute_button:
    if selected_query == "Check Availability of eBooks vs Physical Books":
        ebook_count = filtered_books['isEbook'].sum()
        physical_book_count = len(filtered_books) - ebook_count
        st.write(f"eBooks: {ebook_count}")
        st.write(f"Physical Books: {physical_book_count}")

    elif selected_query == "Find the Publisher with the Most Books Published":
        publisher_count = filtered_books['publisher'].value_counts().head(1)
        st.write(publisher_count)

    elif selected_query == "Identify the Publisher with the Highest Average Rating":
        publisher_avg_rating = filtered_books.groupby('publisher')['averageRating'].mean().idxmax()
        avg_rating = filtered_books.groupby('publisher')['averageRating'].mean().max()
        st.write(f"Publisher: {publisher_avg_rating}")
        st.write(f"Average Rating: {avg_rating}")

    elif selected_query == "Get the Top 5 Most Expensive Books by Retail Price":
        top_expensive_books = filtered_books.nlargest(5, 'amount_retailPrice')
        st.write(top_expensive_books[['book_title', 'amount_retailPrice']])

    elif selected_query == "Find Books Published After 2010 with at Least 500 Pages":
        books_filtered = filtered_books[(filtered_books['year'] > 2010) & (filtered_books['pageCount'] >= 500)]
        st.write(books_filtered[['book_title', 'year', 'pageCount']])

    elif selected_query == "List Books with Discounts Greater than 20%":
        books_filtered = filtered_books[filtered_books['amount_listPrice'] > filtered_books['amount_retailPrice']]
        books_filtered['discount_percentage'] = ((books_filtered['amount_listPrice'] - books_filtered['amount_retailPrice']) / books_filtered['amount_listPrice']) * 100
        books_filtered = books_filtered[books_filtered['discount_percentage'] > 20]
        st.write(books_filtered[['book_title', 'amount_listPrice', 'amount_retailPrice', 'discount_percentage']])

    # Additional queries can be implemented similarly...

    # Display filtered books based on the selected query
    st.header(f"Filtered Books in {selected_category} Category")
    st.dataframe(filtered_books)
