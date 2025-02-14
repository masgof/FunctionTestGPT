from flask import Flask, request, jsonify
from anthropic import Anthropic
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.get_json()
    text = data['text']  # Get golf course name from ElevenLabs
    
    try:
        # Process through Claude
        message = anthropic.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"How many letters (excluding spaces and special characters) are in this golf course name: {text}? Return just the number, nothing else."
            }]
        )
        
        # Get the response from Claude
        count = message.content[0].text
        
        return jsonify({
            "text": text,
            "count": count
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 3000))
    app.run(host='0.0.0.0', port=port)