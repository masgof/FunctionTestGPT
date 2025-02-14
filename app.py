from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/generate-image', methods=['POST'])
def generate_image():
    try:
        # Print request details for debugging
        print("Headers:", dict(request.headers))
        print("Data:", request.get_data().decode('utf-8'))
        
        # Try different ways to get the data
        try:
            data = request.get_json(force=True)  # Force JSON parsing
        except:
            try:
                data = json.loads(request.get_data().decode('utf-8'))
            except:
                data = request.form.to_dict()

        print("Processed data:", data)  # Debug print
        
        # Get text from various possible locations
        text = None
        if isinstance(data, dict):
            text = data.get('text') or data.get('transcribed_text')
        
        if not text and request.form:
            text = request.form.get('text') or request.form.get('transcribed_text')
            
        if not text:
            return jsonify({"error": "No text found in request"}), 400
            
        # Count letters
        letter_count = len([char for char in text if char.isalpha()])
        
        response = {
            "golf_club": text,
            "letter_count": letter_count
        }
        print("Sending response:", response)  # Debug print
        return jsonify(response)
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)