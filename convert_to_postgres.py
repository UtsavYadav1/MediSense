"""
MySQL Backup to PostgreSQL Converter (Fixed - FK Order)
Properly orders INSERT statements to respect foreign key constraints.
"""
import re
import os

# Define table order based on foreign key dependencies
# Tables with no dependencies first, then dependent tables
TABLE_ORDER = [
    'admins',           # No FK
    'users',            # No FK  
    'doctors',          # No FK
    'specializations',  # No FK
    'symptoms_logs',    # FK: users
    'appointments',     # FK: users, doctors
    'doctor_feedback',  # FK: appointments, doctors, users
    'activity_logs',    # No FK constraint but references users
]

def get_table_name(insert_statement):
    """Extract table name from INSERT statement."""
    match = re.search(r'INSERT INTO ["`]?(\w+)["`]?', insert_statement, re.IGNORECASE)
    return match.group(1).lower() if match else None

def convert_mysql_to_postgres(input_file='backup.sql', output_file='backup_postgres.sql'):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Run dump_db.py first.")
        return False
    
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Replace Windows line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Process line by line, handling multi-line INSERT statements
    lines = content.split('\n')
    insert_statements = []
    buffer = ""
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('--'):
            continue
            
        buffer += " " + line if buffer else line
        
        # Check if this is a complete statement (ends with ;)
        if buffer.endswith(';'):
            if buffer.upper().startswith('INSERT'):
                # Fix backticks to double quotes
                buffer = buffer.replace('`', '"')
                
                # Fix escaped single quotes from MySQL (\') to PostgreSQL ('')
                buffer = buffer.replace("\\'", "''")
                
                # Fix backslash escapes for paths
                buffer = buffer.replace('\\\\', '/')
                
                insert_statements.append(buffer)
            buffer = ""
    
    # Group INSERT statements by table
    table_inserts = {table: [] for table in TABLE_ORDER}
    other_inserts = []
    
    for stmt in insert_statements:
        table_name = get_table_name(stmt)
        if table_name and table_name in table_inserts:
            table_inserts[table_name].append(stmt)
        else:
            other_inserts.append(stmt)
    
    # Write output in correct order
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- PostgreSQL Data Import (converted from MySQL)\n")
        f.write("-- Run this in Supabase SQL Editor after creating schema with schema_postgres.sql\n")
        f.write("-- Tables are ordered to respect foreign key constraints.\n\n")
        
        for table in TABLE_ORDER:
            if table_inserts[table]:
                f.write(f"-- {table.upper()} ({len(table_inserts[table])} rows)\n")
                for stmt in table_inserts[table]:
                    f.write(stmt + '\n')
                f.write('\n')
        
        # Any other tables (shouldn't be any, but just in case)
        if other_inserts:
            f.write("-- OTHER TABLES\n")
            for stmt in other_inserts:
                f.write(stmt + '\n')
    
    total = len(insert_statements)
    print(f"Converted! Output saved to {output_file}")
    print(f"Total INSERT statements: {total}")
    for table in TABLE_ORDER:
        if table_inserts[table]:
            print(f"  - {table}: {len(table_inserts[table])} rows")
    return True

if __name__ == "__main__":
    convert_mysql_to_postgres()
