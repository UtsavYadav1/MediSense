import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import json
from decimal import Decimal
from datetime import date, datetime, time, timedelta

load_dotenv()

def audit_database_issues():
    print("🔍 Starting Full Database Audit...")
    
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ Error: No DATABASE_URL found.")
        return

    try:
        conn = psycopg2.connect(db_url)
        # using RealDictCursor as main.py does
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # 1. Get List of Tables
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = [r['table_name'] for r in cursor.fetchall()]
        print(f"📋 Found tables: {tables}")
        
        issues_found = 0
        
        for table in tables:
            print(f"\n--- Auditing Table: {table} ---")
            
            # Check for data
            cursor.execute(f"SELECT * FROM {table} LIMIT 1")
            row = cursor.fetchone()
            
            if not row:
                print("   ⚠️ Table is empty (skipping serialization check)")
                continue
                
            # Check 1: JSON Serialization of raw types
            # This mimics what happens if we pass this row to tojson or jsonify() without processing
            try:
                json.dumps(row)
                print("   ✅ JSON Serializable (Directly)")
            except TypeError as e:
                print(f"   ⚠️ Not JSON Serializable: {e}")
                # Analyze which columns are problematic
                bad_cols = []
                for k, v in row.items():
                    if isinstance(v, (Decimal, date, datetime, time)):
                         bad_cols.append(f"{k} ({type(v).__name__})")
                
                if bad_cols:
                    print(f"      Problematic Columns: {', '.join(bad_cols)}")
                    print("      👉 ACTION: Ensure code converting this table handles these types.")
                    issues_found += 1

            # Check 2: Boolean Integrity (MySQL TINYINT vs PG BOOLEAN)
            # If we see 0/1 integers where we expect booleans, it might be a flag.
            # However, psycopg2 usually maps PG bools to Python bools (True/False).
            # The risk is if code does `if row['flag'] == 1` vs `if row['flag']`.
            # We'll just print bool columns to be aware.
            bool_cols = [k for k, v in row.items() if isinstance(v, bool)]
            if bool_cols:
                print(f"   ℹ️ Boolean Columns (Check logic for True/False vs 1/0): {bool_cols}")

    except Exception as e:
        print(f"❌ Audit Error: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()
        
    print(f"\n🏁 Audit Complete. Issues flagged: {issues_found}")

if __name__ == "__main__":
    audit_database_issues()
