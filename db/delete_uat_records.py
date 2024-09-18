import sqlite3

# Connect to the SQLite database (if the database does not exist, it will be created)
conn = sqlite3.connect('tradingdb.db')  # Replace 'your_database_name.db' with your database name
cursor = conn.cursor()

# Define the deletion condition
table_name='momentum_stocks'
uat_flag = 'Y'

# Write the SQL DELETE statement
delete_query = f"""
DELETE FROM {table_name}
WHERE uat = ?
"""

# Execute the SQL DELETE statement
cursor.execute(delete_query, (uat_flag,))

# Commit the changes
conn.commit()

# Confirm that the deletion operation is complete
print(f"Deleted rows with uat='{uat_flag}' from table {table_name}.")

# Close the database connection
conn.close()
