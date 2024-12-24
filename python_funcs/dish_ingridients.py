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

# Function to parse 'c(...)' format
def parse_c_format(column_value):
    if not isinstance(column_value, str):  # Check if the value is a valid string
        return []  # Return an empty list for invalid or missing values
    column_value = column_value.strip()[2:-1]  # Remove "c(" and ")"
    return re.findall(r'"([^"]+)"', column_value)  # Extract text inside quotes

# Load the required columns for the first 20,000 rows
df = pd.read_csv(file_path, usecols=['RecipeIngredientParts', 'RecipeIngredientQuantities']).head(20000)

# Process each row to populate the `dishingredients` table
for dish_id, row in enumerate(df.itertuples(index=False), start=1):  # dish_id starts at 1
    ingredients = parse_c_format(row.RecipeIngredientParts)  # Parse ingredients
    quantities = parse_c_format(row.RecipeIngredientQuantities)  # Parse quantities

    for ingredient, quantity in zip(ingredients, quantities):
        # Find the ingredient_id for the current ingredient
        cursor.execute(
            "SELECT ingredient_id FROM ingredients WHERE ingredient_name = %s",
            (ingredient,)
        )
        result = cursor.fetchone()
        if result:
            ingredient_id = result[0]

            # Check if the (dish_id, ingredient_id) combination already exists
            cursor.execute(
                "SELECT 1 FROM dishingredients WHERE dish_id = %s AND ingredient_id = %s",
                (dish_id, ingredient_id)
            )
            exists = cursor.fetchone()

            if not exists:
                # Insert into the dishingredients table
                cursor.execute(
                    "INSERT INTO dishingredients (dish_id, ingredient_id, quantity_required) VALUES (%s, %s, %s)",
                    (dish_id, ingredient_id, quantity)
                )

# Commit changes and close the connection
db.commit()
cursor.close()
db.close()

print("Dishingredients table populated successfully!")
