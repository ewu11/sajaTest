import streamlit as st
import cx_Oracle

# Streamlit page setup
st.title("Oracle Database Connection Checker")

# Input fields for credentials and DB details
user = st.text_input("Username")
password = st.text_input("Password", type="password")
host = st.text_input("Host (IP or hostname)", "10.x.x.x")
port = st.text_input("Port", "1521")
service = st.text_input("Service Name or SID", "service")

# Connect button
if st.button("Check Connection"):
    if not all([user, password, host, port, service]):
        st.warning("Please fill in all fields.")
    else:
        dsn = f"{host}:{port}/{service}"
        try:
            # Attempt connection
            conn = cx_Oracle.connect(user, password, dsn)
            st.success("✅ Connection successful!")

            # Execute simple test query
            cursor = conn.cursor()
            cursor.execute("SELECT SYSDATE FROM DUAL")
            result = cursor.fetchone()
            st.write("Current DB Time:", result[0])

            # Close resources
            cursor.close()
            conn.close()

        except cx_Oracle.DatabaseError as e:
            error, = e.args
            st.error("❌ Connection failed.")
            st.code(f"Oracle-Error-Code: {error.code}\nOracle-Error-Message: {error.message}")
