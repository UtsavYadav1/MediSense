"""
Generate admin credentials SQL for Railway MySQL
Run this script and copy the generated SQL to MySQL Workbench
"""
from werkzeug.security import generate_password_hash

email = "admin@wellsure.com"
password = "admin123"
hashed = generate_password_hash(password)

print("\n" + "="*60)
print("COPY THIS SQL TO MYSQL WORKBENCH:")
print("="*60)
print(f"""
USE railway;

DELETE FROM admins WHERE email = '{email}';

INSERT INTO admins (name, email, password) VALUES (
    'Admin',
    '{email}',
    '{hashed}'
);
""")
print("="*60)
print(f"\nAdmin Email: {email}")
print(f"Admin Password: {password}")
print("="*60)
