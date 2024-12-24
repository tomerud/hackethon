import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables (if used)
load_dotenv()

# Database connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", "112145"),
    database="eatAI"
)

cursor = db.cursor()

# Fetch tables
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()

print("Tables in 'eatAI' Database:")
for table in tables:
    table_name = table[0]
    print(f"\nTable: {table_name}")

    # Fetch columns
    cursor.execute(f"""
        SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY, EXTRA
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = 'eatAI' AND TABLE_NAME = '{table_name}';
    """)
    columns = cursor.fetchall()
    print("Columns:")
    for col in columns:
        print(f"  - {col[0]} ({col[1]}), Nullable: {col[2]}, Key: {col[3]}, Extra: {col[4]}")

    # Fetch primary keys
    cursor.execute(f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = 'eatAI' AND TABLE_NAME = '{table_name}' AND CONSTRAINT_NAME = 'PRIMARY';
    """)
    primary_keys = cursor.fetchall()
    print("Primary Keys:")
    for pk in primary_keys:
        print(f"  - {pk[0]}")

    # Fetch foreign keys
    cursor.execute(f"""
        SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
        FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = 'eatAI' AND TABLE_NAME = '{table_name}' AND REFERENCED_TABLE_NAME IS NOT NULL;
    """)
    foreign_keys = cursor.fetchall()
    print("Foreign Keys:")
    for fk in foreign_keys:
        print(f"  - {fk[0]} references {fk[1]}({fk[2]})")

cursor.close()
db.close()
