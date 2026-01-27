import os
import psycopg2
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Load environment variables
load_dotenv()

def reset_admin_password():
    print("🔐 starting Admin Password Reset...")
    
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ Error: No DATABASE_URL found.")
        return

    # Creds to set
    TARGET_EMAIL = "admin@wellsure.ai"
    TARGET_PASSWORD = "Admin@123" 
    
    try:
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # 1. Check if ANY admin exists
        cursor.execute("SELECT id, email FROM admins")
        admins = cursor.fetchall()
        
        if not admins:
            print("⚠️ No admins found. Creating new admin...")
            hashed = generate_password_hash(TARGET_PASSWORD)
            cursor.execute(
                "INSERT INTO admins (name, email, password) VALUES (%s, %s, %s)",
                ("Super Admin", TARGET_EMAIL, hashed)
            )
            print(f"✅ Created new admin: {TARGET_EMAIL}")
            
        else:
            print(f"ℹ️ Found {len(admins)} existing admins.")
            # Update the first one found, or specific one
            target_id = admins[0][0]
            existing_email = admins[0][1]
            
            print(f"🔄 Resetting password for: {existing_email}")
            hashed = generate_password_hash(TARGET_PASSWORD)
            
            cursor.execute(
                "UPDATE admins SET password=%s WHERE id=%s",
                (hashed, target_id)
            )
            print(f"✅ Password reset to default for: {existing_email}")
            TARGET_EMAIL = existing_email # Update for final print

        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n" + "="*40)
        print(f"USER: {TARGET_EMAIL}")
        print(f"PASS: {TARGET_PASSWORD}")
        print("="*40)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    reset_admin_password()
