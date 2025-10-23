"""
Model Wrapper for Sign Language Detection
This module helps integrate your trained model with the application
"""

import numpy as np
import cv2
import tensorflow as tf
from pathlib import Path


class SignLanguageModel:
    """Wrapper class for sign language detection model"""
    
    def __init__(self, model_path, img_size=64, class_labels=None):
        """
        Initialize the model wrapper
        
        Args:
            model_path: Path to the saved model (.h5 or .keras)
            img_size: Input image size expected by the model
            class_labels: List of class labels (default: A-Z alphabet)
        """
        self.model_path = model_path
        self.img_size = img_size
        
        # Load model
        if Path(model_path).exists():
            self.model = tf.keras.models.load_model(model_path)
            print(f"✓ Model loaded successfully from {model_path}")
        else:
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        # Set class labels
        if class_labels is None:
            # Default ASL alphabet + special commands
            self.class_labels = [
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
            ]
        else:
            self.class_labels = class_labels
        
        print(f"✓ Model ready with {len(self.class_labels)} classes")
    
    def preprocess_image(self, image):
        """
        Preprocess image for model input
        
        Args:
            image: Input image (BGR format from OpenCV)
            
        Returns:
            Preprocessed image ready for prediction
        """
        # Resize to model input size
        img_resized = cv2.resize(image, (self.img_size, self.img_size))
        
        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        
        # Normalize to [0, 1]
        img_normalized = img_rgb.astype(np.float32) / 255.0
        
        # Add batch dimension
        img_batch = np.expand_dims(img_normalized, axis=0)
        
        return img_batch
    
    def predict(self, image, return_confidence=True):
        """
        Predict sign language class from image
        
        Args:
            image: Input image (BGR format from OpenCV)
            return_confidence: If True, return (prediction, confidence), else just prediction
            
        Returns:
            prediction: Predicted class label
            confidence: Confidence score (if return_confidence=True)
        """
        # Preprocess image
        processed_img = self.preprocess_image(image)
        
        # Make prediction
        predictions = self.model.predict(processed_img, verbose=0)
        
        # Get class with highest probability
        class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][class_idx])
        
        # Get class label
        if class_idx < len(self.class_labels):
            prediction = self.class_labels[class_idx]
        else:
            prediction = f"Unknown_{class_idx}"
        
        if return_confidence:
            return prediction, confidence
        else:
            return prediction
    
    def predict_batch(self, images):
        """
        Predict multiple images at once
        
        Args:
            images: List of images
            
        Returns:
            List of (prediction, confidence) tuples
        """
        results = []
        for image in images:
            pred, conf = self.predict(image)
            results.append((pred, conf))
        return results
    
    def get_model_info(self):
        """Get information about the loaded model"""
        info = {
            'model_path': self.model_path,
            'input_shape': self.model.input_shape,
            'output_shape': self.model.output_shape,
            'num_classes': len(self.class_labels),
            'class_labels': self.class_labels,
            'img_size': self.img_size
        }
        return info
    
    def print_model_summary(self):
        """Print model architecture summary"""
        print("\n" + "="*60)
        print("MODEL SUMMARY")
        print("="*60)
        self.model.summary()
        print("="*60)
        print(f"Input Size: {self.img_size}x{self.img_size}")
        print(f"Number of Classes: {len(self.class_labels)}")
        print(f"Classes: {', '.join(self.class_labels[:10])}...")
        print("="*60 + "\n")


# Example usage and testing
if __name__ == "__main__":
    import sys
    
    print("\n🔍 Sign Language Model Wrapper - Test Mode\n")
    
    # Check if model path is provided
    if len(sys.argv) > 1:
        model_path = sys.argv[1]
    else:
        # Try to find a model in the current directory
        possible_models = ['model.h5', 'model.keras', 'asl_model.h5', 'sign_language_model.h5']
        model_path = None
        for model_file in possible_models:
            if Path(model_file).exists():
                model_path = model_file
                break
        
        if not model_path:
            print("❌ No model file found!")
            print("Usage: python model_wrapper.py <path_to_model.h5>")
            print(f"Or place one of these files in the current directory: {possible_models}")
            sys.exit(1)
    
    try:
        # Initialize model
        print(f"Loading model from: {model_path}\n")
        model = SignLanguageModel(model_path, img_size=64)
        
        # Print model info
        model.print_model_summary()
        
        # Test with a dummy image
        print("Testing with dummy image...")
        dummy_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        prediction, confidence = model.predict(dummy_image)
        print(f"✓ Prediction: {prediction} (Confidence: {confidence*100:.2f}%)")
        
        print("\n✅ Model wrapper is working correctly!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
