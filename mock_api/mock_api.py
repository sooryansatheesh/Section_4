from flask import Flask, jsonify
from datetime import datetime
import random

#Initializing Flask app
app = Flask(__name__)

# Mock data generator
def generate_mock_data():
    item = {
        'id': random.randint(1, 1000),  # Random ID for each request
        'name': f"Item {random.randint(1, 100)}",  # Random item name
        'timestamp': datetime.now().isoformat(), #Timestamp
        'value': random.randint(1, 100) # Random value 
    }
    return item

#Mock api endpoint
@app.route('/mock_api', methods=['GET'])
def mock_api():
    data = generate_mock_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)