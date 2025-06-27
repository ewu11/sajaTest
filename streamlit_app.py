import streamlit as st

# Title of your app
st.title("Simple Database Search Interface")

# Input field
search_query = st.text_input("Enter your search keyword:")

# Search button
if st.button("Search"):
    # Placeholder for actual database search logic
    # For example, you will call your database function here
    # result = search_database(search_query)
    
    # Dummy result for illustration
    result = f"You searched for: {search_query}"
    
    # Output field
    st.write("### Search Result:")
    st.write(result)
