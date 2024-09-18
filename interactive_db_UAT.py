
# https://www.youtube.com/watch?v=ho1hmfBipvI&list=PL4KX3oEgJcfeX1yOSIQtMH7UlOs1JP3Al&index=5

import sqlite3
import sys

#define which db to access
database = 'db/tradingdb.db'

# connect db
conn = sqlite3.connect(database)
cursor = conn.cursor()

def show_all_table(need_interactive=True):
    # 獲取所有表的名稱
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # 檢查是否有表存在
    if tables:
        print("\nTables in the database:")
        # 顯示所有表的名稱，並編號
        for index, table in enumerate(tables, start=1):
            print(f"{index}. {table[0]}")
        
        if need_interactive:
        # 提示用戶選擇特定的表來顯示其列
            table_number = int(input("\nSelect a table number to view its columns or type '0' to go back: "))
            
            if table_number > 0 and table_number <= len(tables):
                selected_table = tables[table_number - 1][0]
                show_table_columns(selected_table)
            else:
                print("Invalid selection. Returning to main menu.")
    else:
        # 如果沒有找到任何表，打印提示信息
        print("No tables found in the database.")

def show_table_columns(table_name):
    # 獲取指定表的所有列及其數據類型
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()

    if columns:
        print(f"\nColumns in table '{table_name}':")
        for column in columns:
            print(f"{column[1]} ({column[2]})")
    else:
        print(f"No columns found in table '{table_name}'.")

def create_table():
    table_name = input("請輸入要創建的table名: ")
    data_types = ['INTEGER', 'TEXT', 'BLOB', 'REAL', 'NUMERIC', 'DATE', 'BOOLEAN']
    print("可用 data types: " + ', '.join(data_types))
    columns = []
    while True:
        column_name = input("輸入column名（或輸入 'done' 完成）: ")
        if column_name.lower() == 'done':
            break
        print("Choose a data type from the list above.")
        data_type = input(f"輸入 '{column_name}' 的Data Type: ")
        columns.append(f"{column_name} {data_type}")
    
    column_definitions = ', '.join(columns)
    try:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions});")
        conn.commit()
        print(f"表 '{table_name}' 已成功創建，包含列 {column_definitions}。")
    except Exception as e:
        print(f"發生錯誤: {e}")

def delete_table():
    show_all_table(need_interactive=False)
    table_name = input("請輸入要刪除的table名: ")
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        conn.commit()
        print(f"Table '{table_name}' 已成功刪除。")
    except Exception as e:
        print(f"發生錯誤: {e}")


def exit_db():
    cursor.close()
    conn.close()
    sys.exit()

def add_column_to_table():
    show_all_table(need_interactive=False)
    table_name = input("請輸入要添加欄位的table名: ")
    
    # 檢查表是否存在於資料庫中
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    table_exists = cursor.fetchone()
    
    if not table_exists:
        print(f"表 '{table_name}' 不存在，請確認表名是否正確。")
        return
    
    # 獲取該表的現有欄位，以防止添加重複的欄位
    cursor.execute(f"PRAGMA table_info({table_name});")
    existing_columns = cursor.fetchall()
    existing_column_names = [column[1] for column in existing_columns]
    
    column_name = input("請輸入新欄位的名稱: ")
    
    if column_name in existing_column_names:
        print(f"表 '{table_name}' 中已經有名為 '{column_name}' 的欄位。")
        return

    # 提示使用者選擇欄位的數據類型
    data_types = ['INTEGER', 'TEXT', 'BLOB', 'REAL', 'NUMERIC', 'DATE', 'BOOLEAN']
    print("可用 data types: " + ', '.join(data_types))
    data_type = input(f"請選擇欄位 '{column_name}' 的數據類型: ").upper()
    
    if data_type not in data_types:
        print("無效的數據類型，操作取消。")
        return

    try:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type};")
        conn.commit()
        print(f"欄位 '{column_name}' 已成功添加到表 '{table_name}' 中。")
    except Exception as e:
        print(f"發生錯誤: {e}")

def delete_column_from_table():
    show_all_table(need_interactive=False)
    table_name = input("請輸入要刪除欄位的table名: ")
    
    # 獲取該表的現有欄位
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    
    if not columns:
        print(f"表 '{table_name}' 不存在或無欄位。")
        return
    
    # 列出現有欄位
    print(f"現有的欄位: {[column[1] for column in columns]}")
    column_name = input("請輸入要刪除的欄位名稱: ")
    
    # 確認欄位是否存在
    if column_name not in [column[1] for column in columns]:
        print(f"表 '{table_name}' 中不存在欄位 '{column_name}'。")
        return

    # 新的欄位結構，不包含要刪除的欄位
    remaining_columns = [column[1] for column in columns if column[1] != column_name]
    remaining_columns_str = ', '.join(remaining_columns)
    
    try:
        # 重命名舊表
        cursor.execute(f"ALTER TABLE {table_name} RENAME TO {table_name}_old;")
        
        # 創建新表，不包含要刪除的欄位
        column_definitions = ', '.join([f"{column[1]} {column[2]}" for column in columns if column[1] != column_name])
        cursor.execute(f"CREATE TABLE {table_name} ({column_definitions});")
        
        # 將舊表的數據插入新表
        cursor.execute(f"INSERT INTO {table_name} ({remaining_columns_str}) SELECT {remaining_columns_str} FROM {table_name}_old;")
        conn.commit()
        
        # 刪除舊表
        cursor.execute(f"DROP TABLE {table_name}_old;")
        conn.commit()
        
        print(f"欄位 '{column_name}' 已成功從表 '{table_name}' 中刪除。")
    except Exception as e:
        print(f"發生錯誤: {e}")


def select_options():
    while True:
        options = input("""
        ================================================================================
        Type '0'  : Exit
                        
        Type '1'  : Show all tables -> select a table to view columns
                        
        Type '80' : Create a table
        Type '81' : Add column to a table
                        
        Type '90' : Delete a table
        Type '91' : Delete a column from a table
        
        ================================================================================
        >>> """)
        
        if options == "0":
            exit_db()
        elif options == "1":
            show_all_table()
        elif options == "80":
            create_table()
        elif options == "81":
            add_column_to_table() 
        elif options == "90":
            delete_table()        
        elif options == "91":
            delete_column_from_table()
        else:
            print("Invalid option. Please try again.")

# Infinite Loop
select_options()
