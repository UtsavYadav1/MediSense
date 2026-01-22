import mysql.connector
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('MYSQLHOST', os.environ.get('DB_HOST', 'localhost')),
        user=os.environ.get('MYSQLUSER', os.environ.get('DB_USER', 'root')),
        password=os.environ.get('MYSQLPASSWORD', os.environ.get('DB_PASSWORD', 'root')),
        database=os.environ.get('MYSQLDATABASE', os.environ.get('DB_NAME', 'medimind')),
        port=int(os.environ.get('MYSQLPORT', os.environ.get('DB_PORT', 3306)))
    )

def dump_db():
    print("Connecting to database...")
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
    except Exception as e:
        print(f"Error connecting: {e}")
        return

    print("Connected. Fetching tables...")
    cursor.execute("SHOW TABLES")
    tables = [t[0] for t in cursor.fetchall()]
    
    import traceback
    try:
        with open("backup.sql", "wb") as f:
            f.write(b"-- Database Backup\n")
            f.write(f"-- Generated: {datetime.datetime.now()}\n\n".encode('utf-8'))
            f.write(b"SET FOREIGN_KEY_CHECKS=0;\n\n")

            for table in tables:
                print(f"Backing up {table}...")
                
                # 1. Schema
                f.write(f"-- Table structure for `{table}`\n".encode('utf-8'))
                f.write(f"DROP TABLE IF EXISTS `{table}`;\n".encode('utf-8'))
                cursor.execute(f"SHOW CREATE TABLE `{table}`")
                create_stmt = cursor.fetchone()[1]
                f.write(f"{create_stmt};\n\n".encode('utf-8'))
                
                # 2. Data
                f.write(f"-- Dumping data for `{table}`\n".encode('utf-8'))
                cursor.execute(f"SELECT * FROM `{table}`")
                rows = cursor.fetchall()
                
                if not rows:
                    continue
                    
                # Get columns
                cursor.execute(f"SHOW COLUMNS FROM `{table}`")
                columns = [c[0] for c in cursor.fetchall()]
                col_names = ", ".join([f"`{c}`" for c in columns])
                
                for row in rows:
                    values = []
                    for val in row:
                        if val is None:
                            values.append("NULL")
                        elif isinstance(val, (int, float)):
                            values.append(str(val))
                        elif isinstance(val, (bytes, bytearray)):
                             values.append(f"0x{val.hex()}")
                        else:
                            s_val = str(val).replace("\\", "\\\\").replace("'", "''").replace("\0", "\\0")
                            values.append(f"'{s_val}'")
                    
                    val_str = ", ".join(values)
                    # Encode the whole line
                    line = f"INSERT INTO `{table}` ({col_names}) VALUES ({val_str});\n"
                    f.write(line.encode('utf-8'))
                f.write(b"\n")
                
            f.write(b"SET FOREIGN_KEY_CHECKS=1;\n")
    except Exception:
        traceback.print_exc()

    print("Done! Backup saved to 'backup.sql'")
    conn.close()

if __name__ == "__main__":
    dump_db()
