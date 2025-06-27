import streamlit as st
import oracledb

# Database connection details
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_DSN = "host:port/service_name"  # Example: "192.168.1.100:1521/orclpdb1"

def search_database(search_keyword):
    try:
        # Connect using oracledb in thin mode (default if no client installed)
        connection = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_DSN
        )
        cursor = connection.cursor()
        
        # Example SQL query (adjust table and column names)
        sql_query = """
            SELECT column1, column2
            FROM your_table
            WHERE column1 LIKE :search_keyword
        """
        cursor.execute(sql_query, {'search_keyword': f'%{search_keyword}%'})
        
        # Fetch results
        results = cursor.fetchall()
        
        # Close cursor and connection
        cursor.close()
        connection.close()
        
        return results
    
    except oracledb.DatabaseError as e:
        error, = e.args
        return f"Database error: {error.message}"

# Streamlit interface
st.title("Oracle Database Search (Thin mode)")

search_query = st.text_input("Enter search keyword:")

if st.button("Search"):
    if search_query.strip() == "":
        st.warning("Please enter a keyword to search.")
    else:
        result = search_database(search_query)
        
        if isinstance(result, str):
            # If result is error message
            st.error(result)
        elif len(result) == 0:
            st.info("No records found.")
        else:
            # Display results as a table
            st.write("### Search Results")
            st.table(result)
