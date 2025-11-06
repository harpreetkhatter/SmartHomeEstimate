from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS, cross_origin
import util
import os

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes


@app.route('/get_location_names', methods=['GET'])
@cross_origin()  # Additional CORS support
def get_location_names():
    try:
        locations = util.get_location_names()
        response = jsonify({
            'locations': locations
        })
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predict_home_price', methods=['POST'])
@cross_origin()  # Additional CORS support
def predict_home_price():
    try:
        # Check if request has JSON data
        if request.is_json:
            data = request.get_json()
        else:
            # Try form data as fallback
            data = request.form

        print("Received data:", data)

        if not data:
            return jsonify({'error': 'No data received'}), 400

        total_sqft = data.get('total_sqft')
        location = data.get('location')
        bhk = data.get('bhk')
        bath = data.get('bath')

        # Validate all fields exist
        if None in [total_sqft, location, bhk, bath]:
            return jsonify({'error': 'Missing required fields'}), 400

        # Convert types
        total_sqft = float(total_sqft)
        bhk = int(bhk)
        bath = int(bath)

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)

        return jsonify({
            'estimated_price': estimated_price,
            'currency': 'lakhs',
            'location': location,
            'total_sqft': total_sqft,
            'bhk': bhk,
            'bath': bath
        })

    except ValueError as e:
        return jsonify({'error': f'Invalid data format: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/test', methods=['GET'])
@cross_origin()
def test():
    return jsonify({'message': 'Server is working!'})


@app.route('/')
def home():
    # Read the HTML file and serve it
    html_path = os.path.join(os.path.dirname(__file__), '..', 'client', 'app.html')
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        # Update API URLs in HTML for production
        html_content = html_content.replace('http://127.0.0.1:5000/', '/')
        return html_content
    except FileNotFoundError:
        return "HTML file not found", 404


if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
else:
    # For production deployment
    util.load_saved_artifacts()