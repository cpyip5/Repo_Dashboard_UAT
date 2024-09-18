import sqlite3

# 連接到 SQLite3 數據庫，如果數據庫不存在則會創建一個名為 example.db 的文件
# Run below in Powershell terminal is ok, NO NEED change to db/trading.db
# PS C:\Users\SY\Desktop\Repo_MyTradeFunction\db> python .\create_table.py
# Becasue you are running the script under db folder already
# so python will aware the 'tradingdb.db' is already under db fodler
conn = sqlite3.connect('tradingdb.db')

# 創建一個 cursor 對象使用 cursor 來執行 SQL 命令
c = conn.cursor()

# 創建一個表格
c.execute('''
CREATE TABLE stocks
(date TEXT, trans TEXT, symbol TEXT, qty REAL, price REAL)
''')

# 提交事務
conn.commit()

# 關閉連接
conn.close()
