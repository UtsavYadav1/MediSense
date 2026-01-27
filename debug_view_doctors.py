import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
import utils

load_dotenv()

def debug_view_doctors():
    print("--- Debugging View Doctors ---")
    
    # 1. Connect
    try:
        db_url = os.environ.get('DATABASE_URL')
        conn = psycopg2.connect(db_url)
        # Use RealDictCursor to mimic main.py
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        print("✅ Database Connected")
    except Exception as e:
        print(f"❌ Database Connection Error: {e}")
        return

    # 2. Mimic Fetch Doctors
    try:
        cmd = "SELECT * FROM doctors"
        cursor.execute(cmd)
        doctors_list = cursor.fetchall()
        print(f"✅ Fetched {len(doctors_list)} doctors")
        if len(doctors_list) > 0:
            print(f"   Sample Doctor Keys: {list(doctors_list[0].keys())}")
            print(f"   Sample Doctor Lat type: {type(doctors_list[0].get('lat'))}")
    except Exception as e:
        print(f"❌ Error fetching doctors: {e}")
        return

    # 3. Mimic Fetch Patient (Use a known email or just first user)
    try:
        # Get a user ID to test with
        cursor.execute("SELECT id, lat, lng FROM users LIMIT 1")
        patient = cursor.fetchone()
        if not patient:
            print("⚠️ No patients found to test with.")
            return

        print(f"✅ Fetched Patient ID: {patient['id']}")
        print(f"   Lat: {patient['lat']}, Lng: {patient['lng']}")
        print(f"   Type: {type(patient['lat'])}")
    except Exception as e:
        print(f"❌ Error fetching patient: {e}")
        return

    # 4. Call utils.process_doctors_data
    try:
        print("🔄 Calling utils.process_doctors_data...")
        # Note: utils.py function signature: process_doctors_data(doctors_list, patient_lat, patient_lng)
        processed = utils.process_doctors_data(doctors_list, patient['lat'], patient['lng'])
        print("✅ utils.process_doctors_data completed successfully!")
        
        # Check first result distance
        if len(processed) > 0:
             print(f"   First doctor distance: {processed[0].get('distance')}")

    except Exception as e:
        print(f"❌ Error in utils.process_doctors_data: {e}")
        import traceback
        traceback.print_exc()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    debug_view_doctors()
