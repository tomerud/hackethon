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

# Load the 'RecipeIngredientParts' column for the first 20,000 rows
df = pd.read_csv(file_path, usecols=['RecipeIngredientParts']).head(20000)

# Function to parse ingredients from the 'c(...)' format
def parse_ingredients(ingredient_list):
    if not isinstance(ingredient_list, str):  # Check if it's a valid string
        return []  # Return an empty list for invalid entries
    ingredient_list = ingredient_list.strip()[2:-1]  # Remove "c(" and ")"
    ingredients = re.findall(r'"([^"]+)"', ingredient_list)  # Extract ingredients within quotes
    return ingredients

# Process each row to insert unique ingredients
for ingredient_list in df['RecipeIngredientParts']:
    # Parse the ingredient string into a list
    ingredients = parse_ingredients(ingredient_list)

    for ingredient in ingredients:
        # Check if the ingredient already exists in the table
        cursor.execute(
            "SELECT ingredient_id FROM ingredients WHERE ingredient_name = %s",
            (ingredient,)
        )
        result = cursor.fetchone()

        if result is None:
            # If the ingredient is not in the table, insert it
            cursor.execute(
                "INSERT INTO ingredients (ingredient_name) VALUES (%s)",
                (ingredient,)
            )

# Commit changes and close the connection
db.commit()
cursor.close()
db.close()

print("Ingredients populated successfully!")
