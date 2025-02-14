from flask import Flask, request, jsonify
from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.get_json()
    text = data['text']  # Get golf course name from ElevenLabs
    
    try:
        # Process through Claude
        completion = client.completions.create(
            model="claude-2",
            prompt=f"{HUMAN_PROMPT}Count only the letters (excluding spaces and special characters) in this golf course name: {text}. Return just the number, nothing else.{AI_PROMPT}",
            max_tokens_to_sample=100,
            temperature=0
        )
        
        # Get the response from Claude
        count = completion.completion.strip()
        
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