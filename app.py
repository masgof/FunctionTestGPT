from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/generate-image', methods=['POST'])
def generate_image():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
            
        text = data.get('text')
        if not text:
            return jsonify({"error": "Text field is required"}), 400
        
        # Count the number of letters (excluding spaces and special characters)
        letter_count = len([char for char in text if char.isalpha()])
        
        return jsonify({
            "golf_club": text,
            "letter_count": letter_count
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    port = int(os.getenv("PORT", 3000))
    app.run(host='0.0.0.0', port=port)