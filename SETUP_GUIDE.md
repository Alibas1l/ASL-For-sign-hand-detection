# 🚀 Quick Setup Guide

Get your Sign Language Detection Application running in 5 minutes!

## Step 1: Install Dependencies

### Option A: Using pip (Recommended)

```bash
pip install -r requirements.txt
```

### Option B: Manual Installation

```bash
pip install numpy opencv-python Pillow tensorflow mediapipe
```

### Option C: Using Conda

```bash
conda create -n sign_language python=3.9
conda activate sign_language
pip install -r requirements.txt
```

## Step 2: Prepare Your Model

### If you have a trained model:

1. Place your model file (`.h5` or `.keras`) in the `/workspace` directory
2. Open `config.py` and update:
   ```python
   MODEL_PATH = "your_model_name.h5"  # Your model filename
   IMG_SIZE = 64  # Your model's input size
   ```

### If you DON'T have a model yet:

The application will run with hand detection only. You can:
- Train a model using your notebook
- Use a pre-trained ASL model
- Download a model from online sources

## Step 3: Run the Application

### Linux/Mac:
```bash
chmod +x run_app.sh
./run_app.sh
```

### Windows:
```cmd
run_app.bat
```

### Or run directly:
```bash
python sign_language_app.py
```

## Step 4: Test the Application

1. Click **"Start Camera"**
2. Position your hand in front of the camera
3. Try making different hand signs
4. Watch the detection appear in real-time!

## 🔧 Troubleshooting Quick Fixes

### "No module named 'cv2'"
```bash
pip install opencv-python
```

### "No module named 'tensorflow'"
```bash
pip install tensorflow
# OR for CPU only:
pip install tensorflow-cpu
```

### "No module named 'mediapipe'"
```bash
pip install mediapipe
```

### Camera not working
```bash
# Test camera
python -c "import cv2; cap=cv2.VideoCapture(0); print('OK' if cap.isOpened() else 'FAIL')"
```

### Model not loading
- Check the model path in `config.py`
- Ensure model file exists
- Verify TensorFlow version compatibility

## 📋 System Check

Run this to check if everything is installed:

```bash
python -c "import cv2, tensorflow, mediapipe, numpy, PIL; print('✓ All dependencies installed!')"
```

## 🎯 Next Steps

1. ✅ Dependencies installed
2. ✅ Model configured
3. ✅ Application running
4. 📖 Read `README_APPLICATION.md` for detailed usage
5. 🎨 Customize settings in `config.py`

## 💡 Tips for Best Results

- **Good Lighting**: Use bright, even lighting
- **Plain Background**: Stand in front of a simple background
- **Steady Hands**: Hold each sign for 1-2 seconds
- **Camera Position**: Keep your hand centered in the frame
- **Distance**: Position hand 1-2 feet from camera

## 📞 Need Help?

1. Check `README_APPLICATION.md` for detailed documentation
2. Review `config.py` for configuration options
3. Test your model with `python model_wrapper.py your_model.h5`

---

**Ready to go? Start making signs! 👋🤟**
