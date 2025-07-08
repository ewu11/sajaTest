import streamlit as st
import oracledb

# Streamlit page setup
st.title("Oracle Database Connection Checker (oracledb Thin Mode)")

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
