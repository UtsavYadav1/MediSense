import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def check_db():
    db_url = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    
    print("--- Users Table Diagnostics ---")
    
    # Check Max ID
    cursor.execute("SELECT MAX(id) FROM users;")
    max_id = cursor.fetchone()[0]
    print(f"Max ID in users: {max_id}")
    
    # Check Sequence Value
    # Note: 'pd_user_id_seq' or 'users_id_seq'? Schema says SERIAL, typically 'users_id_seq'
    try:
        cursor.execute("SELECT last_value FROM users_id_seq;")
        seq_val = cursor.fetchone()[0]
        print(f"Sequence (users_id_seq) last_value: {seq_val}")
    except Exception as e:
        print(f"Could not read sequence: {e}")
        conn.rollback()

    # Check if we can verify the error 0 behavior
    # This part implies we suspect 'e' is weird.
    
    conn.close()

if __name__ == "__main__":
    check_db()
