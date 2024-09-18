import sqlite3

# 連接到 SQLite 數據庫
conn = sqlite3.connect('tradingdb.db')
cursor = conn.cursor()

# 執行 SQL 查詢
table_name='momentum_stocks'
cursor.execute(f"SELECT * FROM {table_name}")

# 獲取並列印所有記錄
records = cursor.fetchall()
for record in records:
    print(record)

# 關閉連接
cursor.close()
conn.close()
