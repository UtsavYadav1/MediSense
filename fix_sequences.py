import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Tables and their corresponding sequence names (assumed standard naming convention tablename_id_seq)
tables = [
    'users',
    'doctors', 
    'admins',
    'specializations',
    'appointments',
    'symptoms_logs',
    'doctor_feedback',
    'activity_logs'
]

def fix_sequences():
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ Error: DATABASE_URL not found in .env")
        return

    try:
        print(f"Connecting to database...")
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        print("🔄 Checking and resetting sequences...")
        
        for table in tables:
            seq_name = f"{table}_id_seq"
            
            # The SQL logic:
            # 1. Get the max ID from the table.
            # 2. Set the sequence to that max ID (so the next insert will be max + 1).
            # 3. Use COALESCE(MAX(id), 0) + 1? No, setval sets the *current* value. 
            #    If we setval to X, nextval will be X+1.
            #    So setval to MAX(id). If table is empty, we might want to reset to 1.
            
            # This query sets the sequence to the maximum ID value found in the table.
            # If the table is empty (MAX(id) is NULL), it defaults to 1.
            # We use is_called=true (default) so next value is +1.
            query = f"""
                SELECT setval(
                    '{seq_name}', 
                    COALESCE((SELECT MAX(id) FROM {table}), 0) + 1, 
                    false
                );
            """
            # Note: setval(seq, val, false) means "next value returned will be val". 
            # So if max is 4, we setval(seq, 5, false). Next insert gets 5.
            # Alternatively: setval(seq, 4, true). Next insert gets 5. 
            # Let's use setval(seq, MAX(id)) which implies is_called=true.
            
            query = f"SELECT setval('{seq_name}', (SELECT MAX(id) FROM {table}));"
            
            try:
                cursor.execute(query)
                # Fetch result to ensure it executed
                res = cursor.fetchone()
                print(f"✅ {table}: Sequence reset to {res[0]}")
            except Exception as e:
                print(f"⚠️ {table}: Could not reset (might be empty or seq missing). Error: {e}")
                conn.rollback() 
        
        conn.commit()
        conn.close()
        print("\n✨ Sequence fix complete! You can now sign up without 'duplicate key' errors.")
        
    except Exception as e:
        print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    fix_sequences()
