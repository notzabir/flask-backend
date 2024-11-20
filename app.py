from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})  # Allow only requests from React Vite

# Nutritionix API credentials
NUTRITIONIX_APP_ID = '67816ba0'  # Replace with your actual Nutritionix App ID
NUTRITIONIX_APP_KEY = '2915968c5d98045435f85f513f11a493'  # Replace with your actual Nutritionix App Key

@app.route('/api/nutrition', methods=['POST'])
def get_nutrition():
    data = request.get_json()
    query = data.get('query')  # The message/query from the React frontend

    if not query:
        return jsonify({'error': 'No query provided'}), 400

    # Call the Nutritionix API with the user's query
    nutritionix_url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    headers = {
        'x-app-id': NUTRITIONIX_APP_ID,
        'x-app-key': NUTRITIONIX_APP_KEY,
        'Content-Type': 'application/json'
    }
    body = {
        'query': query
    }

    response = requests.post(nutritionix_url, json=body, headers=headers)

    if response.status_code != 200:
        return jsonify({'error': 'Nutritionix API request failed'}), 500

    # Return the Nutritionix API response to the frontend
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)
