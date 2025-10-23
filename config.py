"""
Configuration file for Sign Language Detection Application
Customize these settings based on your model and requirements
"""

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

# Path to your trained model
MODEL_PATH = "model.h5"  # Change this to your model path
# Examples: "asl_model.h5", "model.keras", "models/sign_language_model.h5"

# Input image size expected by your model
IMG_SIZE = 64  # Adjust based on your model's input size

# Class labels - customize based on your training data
# Option 1: Standard ASL Alphabet (A-Z)
CLASS_LABELS = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]

# Option 2: If your model includes numbers or special characters
# CLASS_LABELS = [
#     'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
#     'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
#     '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
#     'Space', 'Delete'
# ]

# Option 3: Load from file
# import json
# with open('class_labels.json', 'r') as f:
#     CLASS_LABELS = json.load(f)


# ============================================================================
# DETECTION CONFIGURATION
# ============================================================================

# Prediction stability - number of consistent frames needed before adding to text
STABILITY_THRESHOLD = 5  # Increase for more stable predictions, decrease for faster response

# Minimum confidence threshold for predictions (0.0 to 1.0)
MIN_CONFIDENCE = 0.7  # Only accept predictions with confidence above this value

# Hand detection confidence
HAND_DETECTION_CONFIDENCE = 0.7
HAND_TRACKING_CONFIDENCE = 0.5

# Maximum number of hands to detect
MAX_HANDS = 1


# ============================================================================
# CAMERA CONFIGURATION
# ============================================================================

# Camera device index (0 for default camera, 1 for external camera, etc.)
CAMERA_INDEX = 0

# Camera resolution (width, height)
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Frame rate (frames per second)
FPS = 30


# ============================================================================
# UI CONFIGURATION
# ============================================================================

# Window size
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

# Color scheme (hex colors)
COLORS = {
    'background': '#2C3E50',
    'panel': '#34495E',
    'primary': '#1ABC9C',
    'success': '#27AE60',
    'warning': '#F39C12',
    'danger': '#E74C3C',
    'info': '#3498DB',
    'text': '#ECF0F1'
}

# Font sizes
FONT_SIZES = {
    'title': 14,
    'normal': 12,
    'prediction': 48,
    'small': 10
}


# ============================================================================
# OUTPUT CONFIGURATION
# ============================================================================

# Output directory for saved text files
OUTPUT_DIR = "output"

# Output file prefix
OUTPUT_PREFIX = "sign_language_output"


# ============================================================================
# ADVANCED SETTINGS
# ============================================================================

# Enable GPU acceleration (if available)
USE_GPU = True

# TensorFlow logging level (0=all, 1=info, 2=warning, 3=error)
TF_LOG_LEVEL = '2'

# Enable performance monitoring
ENABLE_PERFORMANCE_STATS = False

# Debug mode - shows additional information
DEBUG_MODE = False
