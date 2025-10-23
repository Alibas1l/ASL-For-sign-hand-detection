# Sign Language Detection Application

A professional real-time sign language detection application that converts American Sign Language (ASL) gestures into readable text and speech. Built with TensorFlow, Flask, and modern web technologies.

## Features

- 🎥 **Real-time Camera Detection**: Live video capture and processing
- 🤖 **AI-Powered Recognition**: Deep learning model for ASL letter recognition
- 📝 **Sentence Formation**: Intelligent text formation from detected letters
- 🔊 **Text-to-Speech**: Convert formed sentences to speech
- 📱 **Responsive Design**: Modern, professional UI that works on all devices
- ⚡ **High Performance**: Optimized for real-time processing
- 🎯 **High Accuracy**: Confidence-based filtering for reliable results

## Supported Gestures

The application recognizes the following ASL gestures:
- **Letters**: A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z
- **Special**: Space, Delete, Nothing (no gesture)

## Quick Start

### Prerequisites

- Python 3.8 or higher
- Webcam or camera device
- Modern web browser with camera support

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd sign-language-detection-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your model**
   
   If you have a trained model from your Jupyter notebook:
   ```bash
   python convert_model.py
   ```
   
   Or manually save your model as `sign_language_model.h5` in the project directory.

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

1. **Start Detection**: Click the "Start Detection" button to begin camera capture
2. **Position Your Hand**: Place your hand in the center detection box
3. **Make Gestures**: Perform ASL letters clearly and hold them for a moment
4. **View Results**: See detected letters and formed sentences in real-time
5. **Speak Text**: Use the "Speak" button to hear your formed sentences
6. **Copy Text**: Use the "Copy" button to copy text to clipboard

## Project Structure

```
sign-language-detection-app/
├── app.py                 # Flask application
├── convert_model.py       # Model conversion script
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── app.js        # Frontend JavaScript
└── README.md             # This file
```

## Model Integration

The application expects a TensorFlow/Keras model saved as `sign_language_model.h5` with the following specifications:

- **Input Shape**: (64, 64, 3) - RGB images
- **Output Classes**: 29 classes (A-Z + del + nothing + space)
- **Preprocessing**: Images are automatically resized and normalized

### Converting Your Model

If you have a trained model from a Jupyter notebook:

1. Save your model in the notebook:
   ```python
   model.save('sign_language_model.h5')
   ```

2. Run the conversion script:
   ```bash
   python convert_model.py
   ```

## API Endpoints

- `GET /` - Main application interface
- `POST /predict` - Predict letter from image
- `POST /process_sentence` - Process letters into sentence

## Configuration

You can modify the following parameters in `app.py`:

- `confidence_threshold`: Minimum confidence for letter detection (default: 0.7)
- `detection_interval`: Time between predictions in milliseconds (default: 500)
- `image_size`: Input image size for the model (default: 64x64)

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+

## Troubleshooting

### Camera Access Issues
- Ensure your browser has camera permissions
- Try refreshing the page and allowing camera access
- Check if another application is using the camera

### Model Loading Issues
- Verify `sign_language_model.h5` exists in the project directory
- Check that the model has the correct input/output shapes
- Run `python convert_model.py` to create a compatible model

### Performance Issues
- Close other applications using the camera
- Reduce the detection interval in the code
- Use a lower resolution camera if available

## Development

### Adding New Features

1. **New Gestures**: Retrain the model with additional classes
2. **UI Improvements**: Modify `templates/index.html` and `static/css/style.css`
3. **Functionality**: Add new endpoints in `app.py` and frontend logic in `static/js/app.js`

### Testing

Test the application with different:
- Lighting conditions
- Hand positions
- Gesture speeds
- Background environments

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- TensorFlow team for the deep learning framework
- Flask team for the web framework
- ASL community for sign language resources
- Open source contributors

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the code comments
3. Open an issue on GitHub
4. Contact the development team

---

**Note**: This application is designed for educational and accessibility purposes. For production use, consider additional testing, security measures, and performance optimizations.