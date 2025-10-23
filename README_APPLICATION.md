# Sign Language Detection Application

A professional real-time sign language alphabet recognition system with a modern GUI interface.

![Application Screenshot](screenshot.png)

## Features

✨ **Real-time Detection**: Live camera feed with hand detection and sign language recognition  
📝 **Text Conversion**: Automatically converts detected signs to readable text  
💾 **Save Functionality**: Export detected text to files  
🎯 **High Accuracy**: Uses TensorFlow/Keras models with MediaPipe hand detection  
🎨 **Modern UI**: Professional interface with visual feedback  
🔄 **Stability Control**: Prevents false detections with prediction stabilization  

## Prerequisites

- Python 3.8 or higher
- Webcam/Camera
- (Optional) GPU with CUDA support for better performance

## Installation

### 1. Clone or Download

```bash
cd /workspace
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: If you have GPU support, you can use `tensorflow-gpu` instead of `tensorflow` for better performance.

### 3. Prepare Your Model

Place your trained model file in the workspace directory. Supported formats:
- `.h5` (Keras HDF5)
- `.keras` (Keras native format)

Update the model path in `config.py`:

```python
MODEL_PATH = "your_model_name.h5"
IMG_SIZE = 64  # Your model's input size
```

## Quick Start

### Basic Usage

```bash
python sign_language_app.py
```

### Using Custom Model

1. Edit `config.py` to specify your model path and settings
2. Run the application:

```bash
python sign_language_app.py
```

### Testing Your Model

Test if your model loads correctly:

```bash
python model_wrapper.py your_model.h5
```

## Application Interface

### Main Components

1. **Camera Feed (Left Panel)**
   - Live video from your webcam
   - Hand detection with bounding boxes
   - Current detection display with confidence score

2. **Control Panel (Right Panel)**
   - ASL Alphabet Reference Grid
   - Detected Text Display
   - Control Buttons:
     - **Start/Stop Camera**: Toggle camera capture
     - **Clear All**: Clear detected text
     - **Save to Text File**: Export text to file
     - **Quit**: Exit application

3. **Status Bar (Bottom)**
   - Shows current application status

## How to Use

1. **Start the Application**
   ```bash
   python sign_language_app.py
   ```

2. **Click "Start Camera"**
   - Your webcam will activate
   - Position your hand in front of the camera

3. **Make Sign Language Gestures**
   - Hold each sign steady for a moment
   - The application will detect and add letters to the text area
   - Watch the "Current Detection" box for real-time feedback

4. **Build Sentences**
   - Keep making signs to form words
   - Use the "Space" sign to add spaces (if your model supports it)
   - Use the "Delete" sign to remove characters (if supported)

5. **Save Your Text**
   - Click "Save to Text File" when done
   - Files are saved with timestamp: `sign_language_output_YYYYMMDD_HHMMSS.txt`

## Configuration

Edit `config.py` to customize:

### Model Settings
```python
MODEL_PATH = "model.h5"           # Your model file
IMG_SIZE = 64                      # Model input size
CLASS_LABELS = ['A', 'B', 'C'...]  # Your classes
```

### Detection Settings
```python
STABILITY_THRESHOLD = 5            # Frames needed for stable prediction
MIN_CONFIDENCE = 0.7               # Minimum confidence threshold
```

### Camera Settings
```python
CAMERA_INDEX = 0                   # Camera device (0=default)
CAMERA_WIDTH = 640                 # Video width
CAMERA_HEIGHT = 480                # Video height
```

## Integrating Your Model

### Model Requirements

Your model should:
- Accept input shape: `(batch_size, IMG_SIZE, IMG_SIZE, 3)`
- Output: Class probabilities for each sign
- Be saved in `.h5` or `.keras` format

### Example Model Integration

```python
from model_wrapper import SignLanguageModel

# Load your model
model = SignLanguageModel(
    model_path="your_model.h5",
    img_size=64,
    class_labels=['A', 'B', 'C', ...]  # Your classes
)

# Make predictions
prediction, confidence = model.predict(image)
print(f"Detected: {prediction} ({confidence*100:.1f}%)")
```

### Custom Class Labels

If your model has custom classes (e.g., numbers, special signs):

```python
# In config.py
CLASS_LABELS = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'Space', 'Delete', 'Nothing'
]
```

## Troubleshooting

### Camera Not Working

```bash
# Test camera access
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera FAILED')"
```

If it fails:
- Check camera permissions
- Try different CAMERA_INDEX values (0, 1, 2...)
- Ensure no other application is using the camera

### Model Not Loading

```bash
# Test model loading
python model_wrapper.py your_model.h5
```

Common issues:
- Wrong file path - check `MODEL_PATH` in `config.py`
- Incompatible TensorFlow version - ensure model was saved with compatible version
- Corrupted model file - re-save your model

### Low Accuracy

- Ensure good lighting conditions
- Position hand clearly in camera view
- Adjust `STABILITY_THRESHOLD` for more/less sensitive detection
- Adjust `MIN_CONFIDENCE` threshold
- Retrain model with more diverse data

### Installation Issues

**MediaPipe installation fails:**
```bash
pip install mediapipe --upgrade
# Or for Apple Silicon Macs:
pip install mediapipe-silicon
```

**TensorFlow installation fails:**
```bash
# Try CPU version
pip install tensorflow-cpu
```

## Performance Tips

### Speed Up Detection

1. **Use GPU**: Install `tensorflow-gpu` if you have NVIDIA GPU
2. **Reduce Resolution**: Lower `CAMERA_WIDTH` and `CAMERA_HEIGHT`
3. **Optimize Model**: Use model quantization or pruning
4. **Adjust Threshold**: Increase `STABILITY_THRESHOLD` for fewer predictions

### Improve Accuracy

1. **Better Lighting**: Ensure consistent, bright lighting
2. **Hand Position**: Keep hand within bounding box
3. **Hold Steady**: Hold each sign for 1-2 seconds
4. **Clean Background**: Use plain background for better hand detection
5. **Train More**: Add more training data to your model

## Project Structure

```
/workspace/
├── sign_language_app.py      # Main application
├── model_wrapper.py           # Model integration helper
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── README_APPLICATION.md      # This file
├── your_model.h5              # Your trained model (add this)
└── output/                    # Saved text files (created automatically)
```

## Advanced Usage

### Running with Custom Configuration

```python
# custom_run.py
from sign_language_app import SignLanguageDetector
import tkinter as tk

root = tk.Tk()
app = SignLanguageDetector(
    root, 
    model_path="custom_model.h5"
)
root.mainloop()
```

### Batch Processing

```python
from model_wrapper import SignLanguageModel
import cv2

model = SignLanguageModel("model.h5")

# Process multiple images
images = [cv2.imread(f"image_{i}.jpg") for i in range(10)]
results = model.predict_batch(images)

for i, (pred, conf) in enumerate(results):
    print(f"Image {i}: {pred} ({conf*100:.1f}%)")
```

### Headless Mode (No GUI)

```python
# headless_detection.py
from model_wrapper import SignLanguageModel
import cv2

model = SignLanguageModel("model.h5")
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    prediction, confidence = model.predict(frame)
    print(f"Detected: {prediction} ({confidence*100:.1f}%)")
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
```

## System Requirements

### Minimum
- Python 3.8+
- 4GB RAM
- Webcam
- CPU: Intel i5 or equivalent

### Recommended
- Python 3.9+
- 8GB RAM
- HD Webcam (720p or higher)
- GPU: NVIDIA with CUDA support
- CPU: Intel i7 or equivalent

## Contributing

To improve this application:

1. Add support for sentence prediction
2. Implement hand gesture smoothing
3. Add multi-hand detection
4. Include word suggestions
5. Add dark/light theme toggle
6. Support for video file input

## License

This application is provided as-is for educational and research purposes.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review configuration in `config.py`
3. Test model with `model_wrapper.py`
4. Check TensorFlow and OpenCV versions

## Acknowledgments

- **MediaPipe** for hand detection
- **TensorFlow** for deep learning
- **OpenCV** for computer vision
- **ASL Alphabet Dataset** contributors

---

**Made with ❤️ for Sign Language Recognition**

Version: 1.0.0  
Last Updated: 2025-10-23
