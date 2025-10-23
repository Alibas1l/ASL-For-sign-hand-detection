# 🤖 Professional Sign Language Detection Application

A modern, real-time American Sign Language (ASL) detection application with a professional web interface. This application converts ASL gestures into text using computer vision and machine learning.

![Application Preview](https://img.shields.io/badge/Status-Ready-green) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13+-orange) ![Flask](https://img.shields.io/badge/Flask-2.3+-red)

## ✨ Features

### 🎥 Real-Time Detection
- **Live Camera Feed**: High-quality video capture with gesture detection overlay
- **Real-Time Predictions**: Instant sign language recognition with confidence scores
- **Performance Monitoring**: FPS counter and prediction statistics

### 🎨 Professional Interface
- **Modern UI Design**: Clean, responsive interface similar to professional applications
- **Alphabet Grid**: Interactive ASL alphabet reference with active letter highlighting
- **Visual Feedback**: Real-time prediction display with confidence bars and top predictions

### 📝 Text Building
- **Sentence Construction**: Convert detected gestures into readable sentences
- **Smart Controls**: Add letters, spaces, delete characters, and clear text
- **Export Functionality**: Save detected text to timestamped files

### 🔧 Easy Integration
- **Model Flexibility**: Support for TensorFlow/Keras models (.h5, .keras)
- **Auto-Configuration**: Automatic model detection and setup
- **Validation Tools**: Built-in model testing and validation scripts

## 🚀 Quick Start

### Method 1: Easy Launch (Recommended)
```bash
python run_app.py
```
This launcher will:
- Check and install dependencies automatically
- Detect and configure your model
- Open the application in your browser

### Method 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Place your model file in the project directory
# Update model path in app.py (line ~30)

# Run the application
python app.py

# Open browser to http://localhost:5000
```

## 📋 Requirements

- **Python**: 3.8 or higher
- **Camera**: Webcam or external camera
- **Browser**: Modern web browser (Chrome, Firefox, Safari, Edge)
- **Model**: Trained TensorFlow/Keras model for ASL detection

## 🏗️ Project Structure

```
sign-language-app/
├── 📱 app.py                    # Main Flask application
├── 🚀 run_app.py               # Easy launcher script
├── 🔧 model_integration.py     # Model validation helper
├── 📄 requirements.txt         # Python dependencies
├── 📚 setup_instructions.md    # Detailed setup guide
├── 📁 templates/
│   └── 🌐 index.html          # Professional web interface
├── 📁 outputs/                # Generated text files (auto-created)
├── 📁 static/                 # Static assets (auto-created)
└── 🤖 your_model.h5           # Your trained model (add this)
```

## 🎮 How to Use

### 1. **Start the Application**
   - Run `python run_app.py` for automatic setup
   - Or manually run `python app.py`

### 2. **Load Your Model**
   - Place your trained model in the project directory
   - The application will auto-detect and load it
   - Green status indicator confirms model is ready

### 3. **Begin Detection**
   - Click "Start Camera" to activate video feed
   - Grant camera permissions when prompted
   - Position your hand clearly in the camera view

### 4. **Make Predictions**
   - Click "Capture & Predict" to detect signs
   - View real-time predictions with confidence scores
   - See top 3 predictions and alphabet grid highlighting

### 5. **Build Text**
   - Use "Add Letter" to build sentences
   - "Add Space" for word separation
   - "Clear All" to reset text area
   - "Save to File" to export results

## 🔧 Configuration

### Model Settings
Update in `app.py` to match your model:

```python
class SignLanguageDetector:
    def __init__(self, model_path=None):
        # Update class names to match your model
        self.class_names = ['A', 'B', 'C', ..., 'Z', 'del', 'nothing', 'space']
        
        # Update input size to match your model
        self.image_size = (64, 64)
        
        # Adjust confidence threshold
        self.confidence_threshold = 0.7
```

### Camera Settings
Modify resolution in `templates/index.html`:
```javascript
video: { 
    width: 640,
    height: 480,
    facingMode: 'user'
}
```

## 🛠️ API Endpoints

The application provides REST API endpoints for integration:

- `POST /predict` - Make predictions on images
- `GET /get_model_info` - Get model status and information
- `POST /save_text` - Save text to file
- `POST /load_model` - Load a new model

## 🐛 Troubleshooting

### Common Issues

**Camera Problems:**
- Grant camera permissions in browser settings
- Ensure camera isn't used by other applications
- Try different browsers (Chrome recommended)

**Model Issues:**
- Verify model file format (.h5 or .keras)
- Check that class names match your training labels
- Ensure image size matches model input dimensions

**Performance Issues:**
- Reduce video resolution for better performance
- Use GPU acceleration if available
- Consider using a smaller/optimized model

## 📊 Model Requirements

Your model should:
- Accept RGB images of size (64, 64, 3) or update `image_size`
- Output predictions for ASL alphabet (A-Z) plus special classes
- Be saved in TensorFlow/Keras format (.h5 or .keras)
- Include classes: ['A'-'Z', 'del', 'nothing', 'space']

## 🔒 Security & Privacy

- Application runs locally (no data transmission)
- Camera feed processed locally only
- No permanent data storage unless explicitly saved
- All predictions happen on your device

## 📈 Performance Optimization

- **Model Optimization**: Use TensorFlow Lite for mobile deployment
- **Caching**: Implement model prediction caching
- **Batch Processing**: Process multiple frames for stability
- **GPU Acceleration**: Enable GPU support for faster inference

## 🤝 Contributing

Feel free to contribute by:
- Adding new features
- Improving the UI/UX
- Optimizing performance
- Adding support for more sign languages
- Creating better documentation

## 📄 License

This project is provided for educational and research purposes. Please ensure compliance with your local regulations regarding accessibility applications.

## 🎯 Future Enhancements

- [ ] Multi-language support (ASL, BSL, etc.)
- [ ] Mobile app version
- [ ] Real-time continuous recognition
- [ ] Voice synthesis for detected text
- [ ] Advanced gesture tracking
- [ ] Cloud deployment options

---

**Built with ❤️ for the deaf and hard-of-hearing community**

🤟 **Happy Sign Language Detection!** 🤟