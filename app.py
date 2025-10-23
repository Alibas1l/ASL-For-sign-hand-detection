from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import base64
import io
from PIL import Image
import re
import os

app = Flask(__name__)

# Global variables
model = None
class_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
               'del', 'nothing', 'space']

def load_sign_language_model():
    """Load the trained sign language model"""
    global model
    try:
        # Try to load the model from the notebook's saved format
        model = load_model('sign_language_model.h5')
        print("Model loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Please ensure your model is saved as 'sign_language_model.h5' in the project directory")
        return False

def preprocess_image(image):
    """Preprocess image for model prediction"""
    # Resize image to 64x64 as expected by the model
    image = cv2.resize(image, (64, 64))
    # Convert BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Normalize pixel values
    image = image.astype(np.float32) / 255.0
    # Add batch dimension
    image = np.expand_dims(image, axis=0)
    return image

def predict_letter(image):
    """Predict the sign language letter from image"""
    if model is None:
        return "nothing", 0.0
    
    try:
        # Preprocess the image
        processed_image = preprocess_image(image)
        
        # Make prediction
        predictions = model.predict(processed_image, verbose=0)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_idx])
        
        predicted_letter = class_names[predicted_class_idx]
        
        return predicted_letter, confidence
    except Exception as e:
        print(f"Error in prediction: {e}")
        return "nothing", 0.0

def process_sentence(letters):
    """Process detected letters into readable sentences"""
    if not letters:
        return ""
    
    # Filter out 'nothing' and very low confidence predictions
    filtered_letters = [letter for letter in letters if letter != 'nothing']
    
    if not filtered_letters:
        return ""
    
    # Join letters and handle special cases
    sentence = ''.join(filtered_letters)
    
    # Handle 'del' (delete) - remove last character
    while 'del' in sentence:
        del_index = sentence.find('del')
        if del_index > 0:
            sentence = sentence[:del_index-1] + sentence[del_index+3:]
        else:
            sentence = sentence[del_index+3:]
    
    # Handle 'space' - replace with actual spaces
    sentence = sentence.replace('space', ' ')
    
    # Clean up multiple spaces
    sentence = re.sub(r'\s+', ' ', sentence).strip()
    
    return sentence

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get image data from request
        data = request.get_json()
        image_data = data['image']
        
        # Remove data URL prefix
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert PIL image to OpenCV format
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Predict the letter
        predicted_letter, confidence = predict_letter(image_cv)
        
        return jsonify({
            'success': True,
            'letter': predicted_letter,
            'confidence': confidence
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/process_sentence', methods=['POST'])
def process_sentence_endpoint():
    try:
        data = request.get_json()
        letters = data.get('letters', [])
        
        sentence = process_sentence(letters)
        
        return jsonify({
            'success': True,
            'sentence': sentence
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    # Load the model when starting the app
    if load_sign_language_model():
        print("Starting Sign Language Detection App...")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Failed to load model. Please check your model file.")