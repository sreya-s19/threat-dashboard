# view_db.py
import sqlite3

conn = sqlite3.connect('threat_data.db')
cursor = conn.cursor()

print("--- Contents of 'analysis_results' table ---")
for row in cursor.execute("SELECT id, timestamp, threat_score, message_body, findings_json FROM analysis_results ORDER BY id"):
    print(f"\nID: {row[0]}")
    print(f"Timestamp: {row[1]}")
    print(f"Score: {row[2]}")
    print(f"Message: {row[3]}")
    print(f"Findings: {row[4]}")
    print("-" * 20)

conn.close()