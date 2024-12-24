import pandas as pd
import mysql.connector

# Path to the CSV file
file_path = '/recipe_final.csv'

# Database connection
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='112145',
    database='eatAI'
)
cursor = db.cursor()

# Load only the 'Name' column and select the first 100 rows
df = pd.read_csv(file_path, usecols=['Name']).head(20000)

# Insert 'Name' values into the `dishes` table
for name in df['Name']:
    cursor.execute(
        "INSERT INTO dishes (dish_name) VALUES (%s)",
        (name,)
    )

# Commit changes and close the connection
db.commit()
cursor.close()
db.close()

print("First 100 names inserted successfully!")
