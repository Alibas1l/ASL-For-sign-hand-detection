"""
Model Integration Helper for Sign Language Detection Application

This script helps you integrate your trained model with the application.
Place your trained model (.h5 or .keras file) in the same directory as this script
and update the MODEL_PATH variable below.
"""

import os
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np

# Configuration
MODEL_PATH = "your_model.h5"  # Update this with your model file name
IMAGE_SIZE = (64, 64)  # Update this to match your model's input size
CLASS_NAMES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
               'del', 'nothing', 'space']

def validate_model(model_path):
    """Validate that the model can be loaded and get its information"""
    try:
        model = load_model(model_path)
        print(f"✅ Model loaded successfully from: {model_path}")
        print(f"📊 Model summary:")
        print(f"   - Input shape: {model.input_shape}")
        print(f"   - Output shape: {model.output_shape}")
        print(f"   - Total parameters: {model.count_params():,}")
        
        # Test with dummy data
        dummy_input = np.random.random((1, *IMAGE_SIZE, 3)).astype(np.float32)
        predictions = model.predict(dummy_input, verbose=0)
        print(f"   - Prediction output shape: {predictions.shape}")
        print(f"   - Number of classes: {predictions.shape[1]}")
        
        if predictions.shape[1] != len(CLASS_NAMES):
            print(f"⚠️  Warning: Model outputs {predictions.shape[1]} classes but {len(CLASS_NAMES)} class names defined")
        
        return True, model
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False, None

def test_prediction(model):
    """Test the model with a sample prediction"""
    try:
        # Create a dummy image
        dummy_image = np.random.random((1, *IMAGE_SIZE, 3)).astype(np.float32)
        
        # Make prediction
        predictions = model.predict(dummy_image, verbose=0)
        predicted_class_idx = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class_idx]
        
        print(f"🧪 Test prediction:")
        print(f"   - Predicted class index: {predicted_class_idx}")
        print(f"   - Predicted class: {CLASS_NAMES[predicted_class_idx] if predicted_class_idx < len(CLASS_NAMES) else 'Unknown'}")
        print(f"   - Confidence: {confidence:.4f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during test prediction: {e}")
        return False

def main():
    print("🤖 Sign Language Model Integration Validator")
    print("=" * 50)
    
    # Check if model file exists
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Model file not found: {MODEL_PATH}")
        print("📝 Please update MODEL_PATH in this script with your model file name")
        print("💡 Make sure your model file is in the same directory as this script")
        return
    
    # Validate model
    is_valid, model = validate_model(MODEL_PATH)
    
    if is_valid:
        # Test prediction
        test_success = test_prediction(model)
        
        if test_success:
            print("\n✅ Model validation successful!")
            print("🚀 Your model is ready to use with the application")
            print(f"📋 Next steps:")
            print(f"   1. Update the MODEL_PATH in app.py to: '{MODEL_PATH}'")
            print(f"   2. Run the application: python app.py")
            print(f"   3. Open your browser to: http://localhost:5000")
        else:
            print("\n❌ Model validation failed during prediction test")
    else:
        print("\n❌ Model validation failed")
        print("💡 Common issues:")
        print("   - Wrong file path")
        print("   - Corrupted model file")
        print("   - Incompatible TensorFlow version")
        print("   - Missing dependencies")

if __name__ == "__main__":
    main()