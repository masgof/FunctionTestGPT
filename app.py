from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/generate-image', methods=['POST'])
def generate_image():
    try:
        # Try to get JSON data
        if request.is_json:
            data = request.get_json()
        else:
            # If not JSON, try to get form data
            data = request.form.to_dict()
            
        # If neither worked, check raw data
        if not data:
            data = request.get_data()
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            if data.startswith('{'):
                import json
                data = json.loads(data)
        
        text = data.get('text', '')
        
        # Count the number of letters (excluding spaces and special characters)
        letter_count = len([char for char in text if char.isalpha()])
        
        return jsonify({
            "golf_club": text,
            "letter_count": letter_count
        })
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 3000))
    app.run(host='0.0.0.0', port=port)