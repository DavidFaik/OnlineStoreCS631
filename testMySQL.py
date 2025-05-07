import mysql.connector

# Step 1: Connect to MySQL server (not to a specific DB yet)
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="KHlovesburton13!",
    port=3306
)
cursor = conn.cursor()

# Step 2: Create the database (if not exists)
cursor.execute("CREATE DATABASE IF NOT EXISTS OnlineStoreDB")

# Step 3: Switch to the new database
conn.database = "OnlineStoreDB"

# Step 4: Create the SILVER_AND_ABOVE table
create_table_query = """
CREATE TABLE IF NOT EXISTS SILVER_AND_ABOVE (
    CID CHAR(10) NOT NULL,
    CREDITLINE INT
);
"""
cursor.execute(create_table_query)

print("Database and table created successfully.")

# Step 5: Clean up
cursor.close()
conn.close()

