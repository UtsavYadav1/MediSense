import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import json
from decimal import Decimal
from datetime import date, datetime, time, timedelta

load_dotenv()

def verify_json_serialization():
    print("--- Verifying JSON Serialization (Round 2) ---")
    
    try:
        db_url = os.environ.get('DATABASE_URL')
        if not db_url:
            print("❌ No DATABASE_URL found")
            return
            
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cursor.execute("SELECT * FROM doctors LIMIT 1")
        doc = cursor.fetchone()
        
        if not doc:
            print("⚠️ No doctors found.")
            return

        print(f"Sample Doctor Keys: {list(doc.keys())}")
        
        # Check specific time columns
        for col in ['available_start_time', 'available_end_time']:
            val = doc.get(col)
            print(f"Key: {col}, Type: {type(val)}, Value: {val}")

        print("\nAttempting json.dumps...")
        try:
            # Replicate the logic currently in main.py (simulate the partial fix)
            # My previous fix handled Decimal, date, datetime, timedelta
            for k, v in doc.items():
                if isinstance(v, Decimal):
                    doc[k] = float(v)
                elif isinstance(v, (date, datetime)): # This does NOT catch datetime.time
                    doc[k] = str(v)
                elif isinstance(v, timedelta):
                    doc[k] = str(v)
            
            # Now try dumping - if it contains datetime.time, it should fail
            json.dumps(doc)
            print("✅ JSON dump successful!")
        except TypeError as e:
            print(f"❌ JSON dump failed: {e}")
            print("   (This confirms datetime.time is definitely the culprit)")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    verify_json_serialization()
