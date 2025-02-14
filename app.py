from flask import Flask, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.get_json()
    text = data['text']  # Get golf course name from ElevenLabs
    
    try:
        # Process through ChatGPT
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Given a golf course name, return only the number of letters (excluding spaces and special characters). Return just the number, nothing else."},
                {"role": "user", "content": text}
            ]
        )
        
        # Get the response from ChatGPT
        count = completion.choices[0].message.content
        
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