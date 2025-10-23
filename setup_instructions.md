# Sign Language Detection Application - Setup Instructions

## 🎯 Overview
This is a professional real-time sign language detection application that converts ASL (American Sign Language) gestures into text. The application features a modern web interface with live camera feed, alphabet grid display, and text output functionality.

## 📋 Features
- **Real-time Camera Feed**: Live video capture with gesture detection overlay
- **Professional UI**: Modern, responsive design similar to professional applications
- **Alphabet Grid**: Visual ASL alphabet reference with active letter highlighting
- **Text Building**: Convert detected gestures into readable sentences
- **Model Integration**: Easy integration with your trained TensorFlow/Keras models
- **Export Functionality**: Save detected text to files
- **Performance Monitoring**: FPS counter and prediction statistics

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Webcam/Camera access
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Prepare Your Model
1. Place your trained model file (.h5 or .keras) in the project directory
2. Update the model path in `app.py`:
   ```python
   # In app.py, line ~30
   detector = SignLanguageDetector(model_path="your_model_name.h5")
   ```

### Step 3: Validate Your Model (Optional but Recommended)
```bash
python model_integration.py
```
This script will:
- Validate your model can be loaded
- Check input/output shapes
- Test predictions
- Provide integration guidance

### Step 4: Run the Application
```bash
python app.py
```

### Step 5: Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## 🎮 How to Use

### 1. Load Your Model
- Click "Load Model" button (if not already loaded)
- The status indicator will show green when ready

### 2. Start Camera
- Click "Start Camera" to begin video capture
- Grant camera permissions when prompted

### 3. Make Predictions
- Position your hand in front of the camera
- Click "Capture & Predict" to detect the sign
- The prediction will appear in real-time

### 4. Build Text
- Use "Add Letter" to add the detected letter to your text
- Use "Add Space" to add spaces between words
- Use "Clear All" to reset the text area

### 5. Save Results
- Click "Save to File" to export your text
- Files are saved in the `outputs/` directory

## 🔧 Configuration

### Model Configuration
Update these settings in `app.py` to match your model:

```python
class SignLanguageDetector:
    def __init__(self, model_path=None):
        # Update class names to match your model's output
        self.class_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
                           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 
                           'del', 'nothing', 'space']
        
        # Update image size to match your model's input
        self.image_size = (64, 64)
        
        # Adjust confidence threshold as needed
        self.confidence_threshold = 0.7
```

### Camera Settings
Modify camera resolution in `templates/index.html`:
```javascript
const stream = await navigator.mediaDevices.getUserMedia({ 
    video: { 
        width: 640,   // Adjust width
        height: 480,  // Adjust height
        facingMode: 'user'
    } 
});
```

## 📁 Project Structure
```
sign-language-app/
├── app.py                    # Main Flask application
├── model_integration.py      # Model validation helper
├── requirements.txt          # Python dependencies
├── setup_instructions.md     # This file
├── templates/
│   └── index.html           # Web interface
├── outputs/                 # Generated text files (created automatically)
└── your_model.h5           # Your trained model (add this)
```

## 🐛 Troubleshooting

### Camera Issues
- **Permission Denied**: Grant camera access in browser settings
- **Camera Not Found**: Check if camera is connected and not used by other apps
- **Poor Performance**: Reduce video resolution in camera settings

### Model Issues
- **Model Not Loading**: Check file path and model format compatibility
- **Wrong Predictions**: Verify class names match your model's training labels
- **Size Mismatch**: Ensure image_size matches your model's input dimensions

### Performance Issues
- **Slow Predictions**: Consider using a smaller model or reducing image resolution
- **High CPU Usage**: Limit prediction frequency or use GPU acceleration if available

### Browser Compatibility
- **WebRTC Issues**: Use Chrome or Firefox for best camera support
- **UI Problems**: Ensure JavaScript is enabled

## 🔒 Security Notes
- The application runs locally by default (localhost:5000)
- Camera feed is processed locally and not transmitted
- No data is stored permanently unless explicitly saved

## 🚀 Advanced Features

### Custom Model Integration
To integrate models with different architectures:
1. Modify the `preprocess_image()` method for custom preprocessing
2. Update `class_names` to match your model's output classes
3. Adjust `image_size` to match your model's input requirements

### API Endpoints
The application provides REST API endpoints:
- `POST /predict` - Make predictions on images
- `GET /get_model_info` - Get model status and information
- `POST /save_text` - Save text to file
- `POST /load_model` - Load a new model (requires implementation)

### Customization
- Modify CSS in `templates/index.html` for different styling
- Add new features by extending the Flask routes
- Integrate with databases for persistent storage

## 📞 Support
For issues or questions:
1. Check the troubleshooting section above
2. Validate your model using `model_integration.py`
3. Ensure all dependencies are correctly installed
4. Check browser console for JavaScript errors

## 📄 License
This project is provided as-is for educational and research purposes.

---

**Happy Sign Language Detection! 🤟**