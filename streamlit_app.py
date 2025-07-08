import streamlit as st
import oracledb

# Streamlit page setup
st.title("Oracle Database Connection Checker (using SID)")

# Input fields for credentials and DB details
user = st.text_input("Username")
password = st.text_input("Password", type="password")
host = st.text_input("Host (IP or hostname)", "10.x.x.x")
port = st.text_input("Port", "1521")
sid = st.text_input("SID", "ORCL")

# Connect button
if st.button("Check Connection"):
    if not all([user, password, host, port, sid]):
        st.warning("Please fill in all fields.")
    else:
        # Create DSN using SID
        dsn = oracledb.makedsn(host, port, sid=sid)
        try:
            # Attempt connection using oracledb in thin mode
            conn = oracledb.connect(user=user, password=password, dsn=dsn)
            st.success("✅ Connection successful!")

            # Execute simple test query
            cursor = conn.cursor()
            cursor.execute("SELECT SYSDATE FROM DUAL")
            result = cursor.fetchone()
            st.write("Current DB Time:", result[0])

            # Close resources
            cursor.close()
            conn.close()

        except Exception as e:
            # Handle connection failure
            st.error("❌ Connection failed.")
            st.code(str(e))
