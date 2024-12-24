import mysql.connector


def get_possible_dishes():
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='112145',
        database='eatAI'
    )
    cursor = db.cursor()

    # Ask the user for their available ingredients
    user_ingredients = input("Enter the ingredients you have, separated by commas: ").strip().lower().split(',')

    # Clean up and format the input
    user_ingredients = [ingredient.strip() for ingredient in user_ingredients]

    # Create a query to find dishes made exclusively with these ingredients
    query = f"""
        SELECT 
            d.dish_name
        FROM 
            dishes d
        JOIN 
            dishingredients di ON d.dish_id = di.dish_id
        JOIN 
            ingredients i ON di.ingredient_id = i.ingredient_id
        GROUP BY 
            d.dish_id, d.dish_name
        HAVING 
            SUM(i.ingredient_name NOT IN ({','.join('%s' for _ in user_ingredients)})) = 0
            AND COUNT(DISTINCT i.ingredient_name) <= %s;
    """

    # Execute the query
    cursor.execute(query, (*user_ingredients, len(user_ingredients)))

    # Fetch results
    dishes = cursor.fetchall()

    # Close the connection
    cursor.close()
    db.close()

    # Return the results
    if dishes:
        print("\nYou can make the following dishes with your ingredients:")
        for dish in dishes:
            print(f"- {dish[0]}")
    else:
        print("\nNo dishes can be made with the provided ingredients.")


# Call the function
get_possible_dishes()
