import requests
import sqlite3
import json
import time

API_URL = "http://127.0.0.1:5000/analyze" 
DB_FILE = "threat_data.db"

SAMPLE_MESSAGES = [
    "Hello, this is a friendly reminder about our meeting tomorrow.",
    "URGENT: Your account has been locked due to suspicious activity. Click http://192.168.1.5/login to unlock.",
    "Congratulations! You've won a $1000 gift card. Claim it now at totally-legit-site.com",
    "Hi team, please see the attached quarterly report. Let me know if you have questions.",
    "This is the IT department admin. Your final invoice payment is due now. Please transfer the funds immediately.",
    "Let's catch up for coffee next week!",
    "Your Amazon password has been reset. If you did not request this, please contact support immediately."
]

def ingest_data():
    print("Starting data ingestion...")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for message in SAMPLE_MESSAGES:
        print(f"Analyzing message: '{message[:50]}...'")
        try:
            
            response = requests.post(API_URL, json={"body": message})
            response.raise_for_status() 

            data = response.json()
            threat_score = data.get("threat_score")
            findings_list = data.get("report", {}).get("findings", [])

            findings_json = json.dumps(findings_list)

            insert_query = """
            INSERT INTO analysis_results (message_body, threat_score, findings_json)
            VALUES (?, ?, ?)
            """
            cursor.execute(insert_query, (message, threat_score, findings_json))
            conn.commit()
            
            print(f"  -> Success! Score: {threat_score}. Stored in DB.")

        except requests.exceptions.RequestException as e:
            print(f"  -> ERROR: Could not connect to API at {API_URL}. Is the Flask server running?")
            print(f"     Details: {e}")
            break 
        
        time.sleep(1) 

    conn.close()
    print("\nData ingestion complete.")

if __name__ == "__main__":
    ingest_data()