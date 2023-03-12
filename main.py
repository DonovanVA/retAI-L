import os
import base64
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from roboflow import Roboflow
from PIL import Image
import requests
from io import BytesIO
from flask_cors import CORS
from dotenv import dotenv_values
from flask import send_file

import numpy as np

app = Flask(__name__)
CORS(app)
config = dotenv_values(".env")
# Load the trained model

rf = Roboflow(api_key=config["ROBOFLOW_API_KEY"])
project = rf.workspace("school-oxayw").project("shoe-classifier")
model = project.version(3).model

# Define the allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image):
    # Resize image to match the input shape of the model
    image = image.resize((224, 224))
    # Convert PIL image to numpy array
    image_array = np.array(image)
    # Normalize pixel values to be between 0 and 1
    image_array = image_array / 255.0
    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)
    return image_array

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file selected', 400

    file = request.files['file']
    filename = secure_filename(file.filename)

    if not allowed_file(filename):
        return 'Invalid file type', 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Save uploaded image to the server
    file.save(file_path)
    predictions = model.predict(file_path).json()
   
    with open(file_path, "rb") as f:
        image_bytes = f.read()
    encoded_image = base64.b64encode(image_bytes).decode()
    prediction=predictions["predictions"][0]["predictions"][0]["class"]
    # Return the predictions and encoded image as a JSON response
    response_data = {
        'prediction':prediction,
        'image': encoded_image
    }
    return response_data, 200

def create_app():
   return app

if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app
    serve(app, host="0.0.0.0", port=8080)