from flask import Flask, render_template, request, jsonify, Response
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import base64
import io
from PIL import Image
import json
import os
from datetime import datetime

app = Flask(__name__)

class SignLanguageDetector:
    def __init__(self, model_path=None):
        self.model = None
        self.class_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
                           'del', 'nothing', 'space']
        self.image_size = (64, 64)
        self.confidence_threshold = 0.7
        
        if model_path and os.path.exists(model_path):
            try:
                self.model = load_model(model_path)
                print(f"Model loaded successfully from {model_path}")
            except Exception as e:
                print(f"Error loading model: {e}")
                self.model = None
        else:
            print("No model provided or model file not found. Please load a model to enable predictions.")
    
    def preprocess_image(self, image):
        """Preprocess image for model prediction"""
        if isinstance(image, str):
            # If image is base64 string
            image_data = base64.b64decode(image.split(',')[1])
            image = Image.open(io.BytesIO(image_data))
            image = np.array(image)
        
        # Convert to RGB if needed
        if len(image.shape) == 3 and image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        elif len(image.shape) == 3 and image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize image
        image = cv2.resize(image, self.image_size)
        
        # Normalize pixel values
        image = image.astype(np.float32) / 255.0
        
        # Add batch dimension
        image = np.expand_dims(image, axis=0)
        
        return image
    
    def predict(self, image):
        """Make prediction on preprocessed image"""
        if self.model is None:
            return {"error": "No model loaded"}
        
        try:
            processed_image = self.preprocess_image(image)
            predictions = self.model.predict(processed_image, verbose=0)
            
            # Get the predicted class and confidence
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            
            # Get top 3 predictions for display
            top_indices = np.argsort(predictions[0])[::-1][:3]
            top_predictions = []
            
            for idx in top_indices:
                top_predictions.append({
                    'class': self.class_names[idx],
                    'confidence': float(predictions[0][idx])
                })
            
            result = {
                'predicted_class': self.class_names[predicted_class_idx],
                'confidence': confidence,
                'top_predictions': top_predictions,
                'all_predictions': {self.class_names[i]: float(predictions[0][i]) for i in range(len(self.class_names))}
            }
            
            return result
            
        except Exception as e:
            return {"error": f"Prediction error: {str(e)}"}

# Initialize the detector
detector = SignLanguageDetector()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        result = detector.predict(image_data)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/load_model', methods=['POST'])
def load_model():
    try:
        data = request.get_json()
        model_path = data.get('model_path')
        
        if not model_path or not os.path.exists(model_path):
            return jsonify({'error': 'Invalid model path'}), 400
        
        detector.model = load_model(model_path)
        return jsonify({'success': 'Model loaded successfully'})
        
    except Exception as e:
        return jsonify({'error': f'Failed to load model: {str(e)}'}), 500

@app.route('/save_text', methods=['POST'])
def save_text():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text.strip():
            return jsonify({'error': 'No text to save'}), 400
        
        # Create outputs directory if it doesn't exist
        os.makedirs('outputs', exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sign_language_output_{timestamp}.txt"
        filepath = os.path.join('outputs', filename)
        
        # Save text to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        
        return jsonify({'success': f'Text saved to {filename}', 'filename': filename})
        
    except Exception as e:
        return jsonify({'error': f'Failed to save text: {str(e)}'}), 500

@app.route('/get_model_info')
def get_model_info():
    if detector.model is None:
        return jsonify({'loaded': False, 'message': 'No model loaded'})
    else:
        return jsonify({
            'loaded': True, 
            'message': 'Model loaded successfully',
            'classes': detector.class_names,
            'input_shape': detector.image_size
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)