from flask import Flask, request, jsonify
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

@app.route('/')
def home():
    return jsonify({"message": "API is running. Use /generate-image endpoint for requests."})

@app.route('/generate-image', methods=['POST'])
def generate_image():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debug print
        
        if not data or 'text' not in data:
            return jsonify({"error": "Missing text field"}), 400
            
        text = data['text']
        print(f"Processing text: {text}")  # Debug print
        
        # For now, let's just return a simple count without Claude
        # to verify the endpoint is working
        letter_count = len([char for char in text if char.isalpha()])
        
        return jsonify({
            "text": text,
            "count": letter_count
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 3000))
    app.run(host='0.0.0.0', port=port)