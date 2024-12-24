import pandas as pd
import mysql.connector
import re

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


# Function to parse instructions from the 'c(...)' format
def parse_instructions(instruction_string):
    if not isinstance(instruction_string, str):  # Check if the input is valid
        return ""  # Return an empty string for invalid entries
    instruction_string = instruction_string.strip()[2:-1]  # Remove "c(" and ")"
    instructions = re.findall(r'"([^"]+)"', instruction_string)  # Extract text inside quotes
    return ' '.join(instructions)  # Combine instructions into a single string


# Variables to track inserted rows and chunk size
chunk_size = 500  # Process 500 rows at a time
total_inserted = 0  # Counter for total inserted rows
max_rows = 20000  # Target number of rows to insert

# Read and process the file in chunks
for chunk in pd.read_csv(file_path, usecols=['RecipeInstructions'], chunksize=chunk_size):
    for i, instruction_string in enumerate(chunk['RecipeInstructions'], start=total_inserted + 1):
        # Parse the instruction string
        parsed_instruction = parse_instructions(instruction_string)

        # Insert into the `instructions` table
        cursor.execute(
            "INSERT INTO instructions (instruction_id, dish_id, instructions) VALUES (%s, %s, %s)",
            (i, i, parsed_instruction)  # Use `i` as both instruction_id and dish_id
        )

    total_inserted += len(chunk)  # Update the count of inserted rows

    # Break the loop once 20,000 rows have been inserted
    if total_inserted >= max_rows:
        break

# Commit changes and close the connection
db.commit()
cursor.close()
db.close()

print(f"Instructions added successfully for {total_inserted} rows!")
