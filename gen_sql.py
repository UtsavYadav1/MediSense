from werkzeug.security import generate_password_hash

h = generate_password_hash('admin123')

sql = f"""USE railway;

DELETE FROM admins;

INSERT INTO admins (name, email, password) VALUES (
    'Admin',
    'admin@wellsure.com',
    '{h}'
);
"""

with open('admin_sql.txt', 'w') as f:
    f.write(sql)

print("SQL saved to admin_sql.txt")
print(sql)
