import sqlite3
import streamlit as st

def create_database():
    # 建立連接資料庫，如果資料庫不存在則創建一個新的
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    # 創建一個名為 users 的表
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    email TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

def insert_user(name, age, email):
    # 插入用戶資料進入 users 表
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", (name, age, email))
    conn.commit()
    conn.close()

def app():
    st.title('簡單的用戶輸入網站')
    st.write("請輸入你的資料並點擊按鈕提交。")
    
    # 建立輸入框
    name = st.text_input("名字:")
    age = st.number_input("年齡:", min_value=1, max_value=120, step=1)
    email = st.text_input("電子郵件:")
    
    # 當按下"提交"按鈕時，插入用戶數據進入資料庫
    if st.button("提交"):
        if name and age and email:
            insert_user(name, age, email)
            st.success("用戶資料已成功提交！")
        else:
            st.error("請填寫所有欄位！")

def main():
    create_database()
    app()

if __name__ == "__main__":
    main()
