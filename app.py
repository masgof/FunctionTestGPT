from flask import Flask, request, jsonify
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
claude = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.get_json()
    text = data['text']  # Get golf course name from ElevenLabs
    
    try:
        # Process through Claude
        completion = claude.completion(
            prompt=f"{anthropic.HUMAN_PROMPT} How many letters (excluding spaces and special characters) are in this golf course name: {text}? Return just the number, nothing else.{anthropic.AI_PROMPT}",
            model="claude-2",
            max_tokens_to_sample=1000,
        )
        
        # Get the response from Claude
        count = completion.completion
        
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