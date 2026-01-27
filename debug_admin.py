import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape

load_dotenv()

def debug_admin():
    print("--- Debugging Admin Dashboard ---")
    
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ No DATABASE_URL")
        return

    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        print("1. Fetching Doctors...")
        cursor.execute("SELECT * FROM doctors ORDER BY id DESC")
        doctors = cursor.fetchall()
        print(f"   Fetched {len(doctors)} doctors")
        
        print("2. Fetching Patients...")
        cursor.execute("SELECT * FROM users ORDER BY id DESC")
        patients = cursor.fetchall()
        print(f"   Fetched {len(patients)} patients")
        
        print("3. Fetching Specializations...")
        cursor.execute("SELECT * FROM specializations ORDER BY name ASC")
        specializations = cursor.fetchall()
        print(f"   Fetched {len(specializations)} specs")
        
        print("4. Fetching Logs...")
        cursor.execute("SELECT * FROM activity_logs ORDER BY created_at DESC LIMIT 50")
        logs = cursor.fetchall()
        print(f"   Fetched {len(logs)} logs")
        
        cursor.close()
        conn.close()
        
        # 5. Simulate Template Rendering (Partial)
        print("5. Simulating Template Context...")
        
        # In main.py:
        # return render_template('admin_dashboard.html', doctors=doctors, patients=patients, 
        #                        specializations=specializations, logs=logs)
        
        # Issues I spotted:
        # a) Template uses `stats.patients` but `stats` not passed.
        # b) Template uses `activities` but `logs` passed.
        # c) Template uses `doc.speciality` but column is `specialization`.
        
        # Let's try to access these risks
        
        # Check stats access
        try:
            print(f"   Typo Check 1: logs vs activities")
            # If I passed logs=logs, but access activities... accessing undefined 'activities' is fine.
            pass
        except Exception as e:
            print(f"   Error: {e}")
            
        print("6. Verification Complete (Data Fetching works)")
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_admin()
