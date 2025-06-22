# database_setup.py

import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect('threat_data.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# --- Define the table schema ---
# We use "IF NOT EXISTS" to prevent errors if we run the script multiple times.
create_table_query = """
CREATE TABLE IF NOT EXISTS analysis_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    message_body TEXT NOT NULL,
    threat_score INTEGER NOT NULL,
    findings_json TEXT NOT NULL
);
"""

# Execute the query to create the table
cursor.execute(create_table_query)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database 'threat_data.db' and table 'analysis_results' created successfully.")