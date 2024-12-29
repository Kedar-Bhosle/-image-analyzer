from flask import Flask, request, jsonify
from flask_cors import CORS
from gradio_client import Client, handle_file
import tempfile
import os

app = Flask(__name__)
CORS(app)  # Enabling Cross-Origin Resource Sharing

#client = Client("Romaniac974/jewlery")
@app.route('/style', methods=['POST'])
def process_image():
    # Check if image is in the request
    if 'image' not in request.files:
        # Return an error response if no image is provided
        return jsonify({'error': 'Image file is required'}), 400

    # Get the image from the request
    file1 = request.files['image']

    try:
        # Save the uploaded file temporarily
        temp_file1 = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
        temp_file_path1 = temp_file1.name
        file1.save(temp_file_path1)
        temp_file1.close()
        client = Client("Romaniac974/jewlery")
        # Call the Gradio client predict function
        result = client.predict(
            img=handle_file(temp_file_path1),
            api_name="/predict"
        )

        # Return the result as a JSON response
        return jsonify({'output': result}), 200

    except Exception as e:
        # Return an error response in case of an exception
        return jsonify({'error': str(e)}), 500

    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path1):
            os.remove(temp_file_path1)

# Run the application
if __name__ == '__main__':  # Corrected to __name__ and __main__
    app.run(debug=True)