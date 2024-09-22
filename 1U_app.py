import streamlit as st
import sqlite3
from datetime import date
import os

db_name='db/tradingdb.db'

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


################# Add display OS part
import streamlit as st
import subprocess
import shutil
from datetime import datetime

def upload_to_github():
    # 資料庫原始檔案名稱
    original_db = 'db/tradingdb.db'
    
    # 生成時間戳記
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_db_name = f"db/tradingdb_{timestamp}.db"
    
    # 複製並重命名資料庫檔案
    shutil.copy(original_db, new_db_name)
    
    # 使用 git 指令將帶有時間戳記的新資料庫檔案推送到 GitHub
    subprocess.run(['git', 'add', new_db_name])
    subprocess.run(['git', 'commit', '-m', f'Update database with timestamp: {new_db_name}'])
    subprocess.run(['git', 'push', 'origin', 'main'])  # 或是你的分支名稱

# 創建一個按鈕，當按下時觸發上傳動作
st.button("Upload Database to GitHub", on_click=upload_to_github)
