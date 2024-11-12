import sqlite3
import streamlit as st

def create_database():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    email TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

def insert_user(name, age, email):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", (name, age, email))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_all_users():
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    rows = c.fetchall()
    conn.close()
    return rows

def app():
    st.title('簡單的用戶輸入網站')
    st.write("請輸入你的資料並點擊按鈕提交。")
    
    # 建立輸入框
    name = st.text_input("名字:")
    age = st.number_input("年齡:", min_value=1, max_value=120, step=1)
    email = st.text_input("電子郵件:")
    
    if st.button("提交"):
        if name and age and email:
            insert_user(name, age, email)
            st.success("用戶資料已成功提交！")
        else:
            st.error("請填寫所有欄位！")
    
    # 使用 container 顯示所有用戶資料
    with st.container(border=True):
        st.write("\n## 所有用戶資料")
        users = get_all_users()
        
        if users:
            user_data = []
            for user in users:
                user_data.append({
                    'ID': user[0],
                    '名字': user[1],
                    '年齡': user[2],
                    '電子郵件': user[3]
                })
            
            # 顯示用戶資料為表格形式
            st.table(user_data)
            
            # 添加刪除按鈕和確認框
            for user in users:
                delete_container = st.container()
                with delete_container:
                    st.write(f"用戶 {user[0]}: {user[1]}")
                    
                    # 使用 session state 追蹤確認狀態
                    confirm_key = f"confirm_{user[0]}"
                    if confirm_key not in st.session_state:
                        st.session_state[confirm_key] = False
                    
                    # 添加刪除確認
                    if st.checkbox(f"確認刪除用戶 {user[0]}", key=f"checkbox_{user[0]}"):
                        st.session_state[confirm_key] = True
                    
                    if st.session_state[confirm_key] and st.button(f"刪除", key=f"delete_{user[0]}"):
                        delete_user(user[0])
                        st.success(f"用戶 {user[0]} 已刪除！")
                        # 重置確認狀態
                        st.session_state[confirm_key] = False
                        st.rerun()
        else:
            st.write("目前沒有用戶資料。")
        
        # 刷新按鈕
        if st.button("刷新資料", key="refresh"):
            st.rerun()

def main():
    create_database()
    app()

if __name__ == "__main__":
    main()
