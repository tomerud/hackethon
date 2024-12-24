import mysql.connector
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enables Cross-Origin Resource Sharing for all routes

@app.route('/api/get_recipe', methods=['POST'])
def get_recipe():
    data = request.get_json()
    user_ingredients = data.get('ingredients', [])

    # Clean up and format the input
    user_ingredients = [ingredient.strip().lower() for ingredient in user_ingredients]

    # Connect to the MySQL database
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='112145',
        database='eatAI'
    )
    cursor = db.cursor()

    # Build the query string
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

    # Execute the query using all user_ingredients plus the length of user_ingredients
    cursor.execute(query, (*user_ingredients, len(user_ingredients)))
    dishes = cursor.fetchall()

    # Close connections
    cursor.close()
    db.close()

    # Convert list of tuples into a list of dish names
    dish_names = [dish[0] for dish in dishes]

    # Return JSON for your React front end: { "dishes": [... ] }
    return jsonify({"dishes": dish_names})

if __name__ == '__main__':
    app.run(debug=True)
