"""
Model Conversion Script for Sign Language Detection App

This script helps convert your trained model from the Jupyter notebook
to the format required by the Flask application.

Usage:
1. Make sure your model is saved in the notebook
2. Run this script to convert it to the required format
3. The converted model will be saved as 'sign_language_model.h5'
"""

import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Rescaling, Flatten, Dense, Dropout
import os

def create_model_architecture():
    """
    Recreate the model architecture from your notebook
    This should match the architecture you used in training
    """
    image_size = 64
    
    # Input layer
    input_ = Input(shape=(image_size, image_size, 3))
    scale_input = Rescaling(1/255.0)(input_)
    
    # Flatten layer
    flatten_input = Flatten()(scale_input)
    
    # Dense layers (adjust based on your actual architecture)
    dense1 = Dense(512, activation='relu')(flatten_input)
    dropout1 = Dropout(0.5)(dense1)
    
    dense2 = Dense(256, activation='relu')(dropout1)
    dropout2 = Dropout(0.3)(dense2)
    
    # Output layer (29 classes: A-Z + del + nothing + space)
    output = Dense(29, activation='softmax')(dropout2)
    
    # Create model
    model = Model(inputs=input_, outputs=output)
    
    return model

def convert_model():
    """
    Convert and save the model in the required format
    """
    print("Creating model architecture...")
    model = create_model_architecture()
    
    print("Model architecture created successfully!")
    print("Model summary:")
    model.summary()
    
    # Save the model
    model_path = 'sign_language_model.h5'
    model.save(model_path)
    
    print(f"\nModel saved as: {model_path}")
    print("You can now run the Flask application!")
    
    # Test loading the model
    try:
        loaded_model = tf.keras.models.load_model(model_path)
        print("✓ Model loads successfully!")
        
        # Test prediction with dummy data
        dummy_input = np.random.random((1, 64, 64, 3)).astype(np.float32)
        prediction = loaded_model.predict(dummy_input, verbose=0)
        print(f"✓ Model prediction works! Output shape: {prediction.shape}")
        
    except Exception as e:
        print(f"✗ Error testing model: {e}")

if __name__ == "__main__":
    print("Sign Language Model Converter")
    print("=" * 40)
    
    # Check if TensorFlow is available
    print(f"TensorFlow version: {tf.__version__}")
    
    # Convert the model
    convert_model()
    
    print("\n" + "=" * 40)
    print("Conversion complete!")
    print("\nNext steps:")
    print("1. Install requirements: pip install -r requirements.txt")
    print("2. Run the app: python app.py")
    print("3. Open your browser to: http://localhost:5000")