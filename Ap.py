from flask import Flask, request, jsonify
from flask_cors import CORS
from gradio_client import Client, handle_file
import tempfile




app = Flask(__name__)
CORS(app)  # Enabling Cross-Origin Resource Sharing
client = Client("Aashi/Text-Image-Analyzer")

@app.route('/analyzer', methods=['POST'])
def process_image():
    # Check if prompt is provided
    if not request.form.get('prompt'):
        return jsonify({'error': 'prompt is required'}), 400
    
    # Check if image is in the request
    if 'image' not in request.files:
        return jsonify({'error': 'image file is required'}), 400

     # Get the prompt and image from the request
    prompt1 = request.form.get('prompt')
    file1= request.files['image']
    #file1_data = file1.read()
    
    # Save the uploaded file temporarily
    temp_file1 = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_file_path1 = temp_file1.name
    file1.save(temp_file_path1)
    temp_file1.close()

    try:
        # Call the client.predict function to process the image
        result = client.predict(
            text=prompt1,
            image=handle_file(temp_file_path1),
            api_name="/predict"
        )
        # Return the result as a JSON response
        return jsonify({'output': result}), 200

    except Exception as result:
        # Handle any errors
        return jsonify({'error': str(result)}), 500

# Run the application
if __name__ == '__main__':  # Corrected to __name__ and __main__
    app.run(debug=True)
 # print("Running directly")
