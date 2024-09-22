# This cod eis applying the Github API so whenever user submit the data
# it will submit the data to the github
import streamlit as st
import sqlite3
from datetime import date
import os
import requests
import base64

# GitHub 配置
GITHUB_TOKEN = st.secrets["GITHUB_TOKEN"]  # 在 Streamlit Secrets 中儲存 GitHub Token
GITHUB_REPO = 'your_username/your_repo'  # GitHub 儲存庫名稱
GITHUB_API = 'https://api.github.com'

db_name = 'db/tradingdb.db'

# 連接到 SQLite 資料庫
def connect_db():
    conn = sqlite3.connect(db_name)
    return conn, conn.cursor()

# 插入數據到 'test' 表格
def insert_data(date_hkt, mum_bo, qqq, mum_saving):
    conn, c = connect_db()
    c.execute('''
        INSERT INTO test (date_hkt, mum_bo, qqq, mum_saving)
        VALUES (?, ?, ?, ?)
    ''', (date_hkt, mum_bo, qqq, mum_saving))
    conn.commit()
    conn.close()

# 使用 GitHub API 上傳檔案到 GitHub
def upload_to_github(file_path, commit_message):
    try:
        with open(file_path, 'rb') as file:
            content = base64.b64encode(file.read()).decode('utf-8')

        url = f'{GITHUB_API}/repos/{GITHUB_REPO}/contents/{file_path}'
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }

        data = {
            'message': commit_message,
            'content': content
        }

        response = requests.put(url, json=data, headers=headers)

        if response.status_code == 201:
            st.success('檔案已成功推送到 GitHub！')
        else:
            st.error(f'推送檔案失敗: {response.status_code}, {response.text}')

    except Exception as e:
        st.error(f'上傳過程中發生錯誤: {e}')

# Streamlit 應用程式
st.title('Trade Record Input')

# 輸入區
st.header('輸入數據')

# 讓用戶選擇日期
date_hkt = st.date_input('選擇日期', value=date.today()).strftime("%Y-%m-%d")

# 輸入 mum_bo、qqq、mum_saving
mum_bo = st.number_input('mum_bo', min_value=0.0, step=0.01)
qqq = st.number_input('qqq', min_value=0.0, step=0.01)
mum_saving = st.number_input('mum_saving', min_value=0.0, step=0.01)

# 按鈕來儲存數據
if st.button('儲存數據'):
    insert_data(date_hkt, mum_bo, qqq, mum_saving)
    st.success(f'數據已成功儲存！\n日期: {date_hkt}\nmum_bo: {mum_bo}\nqqq: {qqq}\nmum_saving: {mum_saving}')
    # 推送變更到 GitHub
    upload_to_github(db_name, 'Updated tradingdb.db')

# 顯示已儲存的數據
st.header('已儲存的數據')

def fetch_data():
    conn, c = connect_db()
    c.execute('SELECT * FROM test')
    data = c.fetchall()
    conn.close()
    return data

# 顯示資料庫中的所有數據
data = fetch_data()
if data:
    for row in data:
        st.write(f'Date: {row[0]}, mum_bo: {row[1]}, qqq: {row[2]}, mum_saving: {row[3]}')
else:
    st.write('尚未有數據')

if os.path.exists(db_name):
    with open(db_name, 'rb') as f:
        st.download_button(label="Download Database", data=f, file_name="tradingdb.db")
