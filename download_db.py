import streamlit as st
import os

st.title("Download SQLite Database")

# 提供下載資料庫的功能
db_file = 'db/tradingdb.db'

if os.path.exists(db_file):
    with open(db_file, 'rb') as f:
        st.download_button(label="Download Database", data=f, file_name="tradingdb.db")
else:
    st.error("Database file not found!")
