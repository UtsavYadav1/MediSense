"""
Create admin for Railway MySQL database
"""
import mysql.connector
from werkzeug.security import generate_password_hash
import os

# Railway MySQL connection - get these from Railway dashboard
# Go to MySQL service -> Variables tab
RAILWAY_HOST = input("Enter MYSQLHOST from Railway: ").strip()
RAILWAY_PORT = input("Enter MYSQLPORT from Railway (default 3306): ").strip() or "3306"
RAILWAY_USER = input("Enter MYSQLUSER from Railway: ").strip()
RAILWAY_PASSWORD = input("Enter MYSQLPASSWORD from Railway: ").strip()
RAILWAY_DATABASE = input("Enter MYSQLDATABASE from Railway: ").strip()

try:
    conn = mysql.connector.connect(
        host=RAILWAY_HOST,
        port=int(RAILWAY_PORT),
        user=RAILWAY_USER,
        password=RAILWAY_PASSWORD,
        database=RAILWAY_DATABASE
    )
    cursor = conn.cursor()
    
    email = "admin@wellsure.com"
    password = "admin123"
    hashed = generate_password_hash(password)
    
    # Delete existing
    cursor.execute("DELETE FROM admins WHERE email=%s", (email,))
    
    # Insert new
    cursor.execute("INSERT INTO admins (name, email, password) VALUES (%s, %s, %s)", ("Admin", email, hashed))
    print(f"\n✅ Created admin account!")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
        
    conn.commit()
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")
