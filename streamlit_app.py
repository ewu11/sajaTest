import streamlit as st
import oracledb
from sshtunnel import SSHTunnelForwarder

st.title("Oracle DB Connection Checker (Jump Host Tunnel)")

# SSH jump host details
ssh_host = st.text_input("Jump Host IP", "jump.host.ip")
ssh_port = st.number_input("Jump Host SSH Port", value=22)
ssh_user = st.text_input("Jump Host Username")
ssh_password = st.text_input("Jump Host Password", type="password")

# DB details (INSIDE remote network)
db_host = st.text_input("DB Host", "db.internal.ip")
db_port = st.number_input("DB Port", value=1521)
sid = st.text_input("DB SID", "ORCL")
db_user = st.text_input("DB Username")
db_password = st.text_input("DB Password", type="password")

if st.button("Check Connection"):
    if not all([ssh_host, ssh_user, ssh_password, db_host, sid, db_user, db_password]):
        st.warning("Please fill in all fields.")
    else:
        # Create DSN using SID
        dsn = oracledb.makedsn("127.0.0.1",  # We connect locally
                               db_port, sid=sid)

        try:
            with SSHTunnelForwarder(
                (ssh_host, ssh_port),
                ssh_username=ssh_user,
                ssh_password=ssh_password,
                remote_bind_address=(db_host, db_port),
                local_bind_address=("127.0.0.1", db_port)  # Forward local port = remote DB port
            ) as tunnel:

                conn = oracledb.connect(
                    user=db_user,
                    password=db_password,
                    dsn=dsn
                )
                st.success("✅ Connection successful through SSH tunnel!")

                cursor = conn.cursor()
                cursor.execute("SELECT SYSDATE FROM DUAL")
                result = cursor.fetchone()
                st.write("Current DB Time:", result[0])

                cursor.close()
                conn.close()

        except Exception as e:
            st.error("❌ Connection failed.")
            st.code(str(e))
