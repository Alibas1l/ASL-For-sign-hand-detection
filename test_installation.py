#!/usr/bin/env python3
"""
Installation Test Script
Checks if all dependencies are properly installed
"""

import sys
import os

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_module(module_name, package_name=None):
    """Check if a module can be imported"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"✓ {package_name:20s} - Installed")
        return True
    except ImportError:
        print(f"✗ {package_name:20s} - NOT INSTALLED")
        return False

def check_camera():
    """Check if camera is accessible"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            cap.release()
            print("✓ Camera Access       - OK")
            return True
        else:
            print("✗ Camera Access       - FAILED (camera not found)")
            return False
    except:
        print("✗ Camera Access       - FAILED")
        return False

def check_model_file():
    """Check if a model file exists"""
    model_files = ['model.h5', 'model.keras', 'asl_model.h5', 'sign_language_model.h5']
    for model_file in model_files:
        if os.path.exists(model_file):
            print(f"✓ Model File          - Found: {model_file}")
            return True
    print("⚠ Model File          - No model found (you'll need to add one)")
    return False

def get_version(module_name):
    """Get version of a module"""
    try:
        module = __import__(module_name)
        if hasattr(module, '__version__'):
            return module.__version__
        return "unknown"
    except:
        return "N/A"

def main():
    print_header("Sign Language Detection - Installation Test")
    
    print(f"\nPython Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    
    print_header("Checking Dependencies")
    
    # Core dependencies
    all_ok = True
    dependencies = [
        ('numpy', 'NumPy'),
        ('cv2', 'OpenCV'),
        ('PIL', 'Pillow'),
        ('tensorflow', 'TensorFlow'),
        ('mediapipe', 'MediaPipe'),
    ]
    
    for module, name in dependencies:
        if not check_module(module, name):
            all_ok = False
    
    # Check tkinter (usually built-in)
    try:
        import tkinter
        print(f"✓ {'Tkinter':20s} - Installed")
    except ImportError:
        print(f"✗ {'Tkinter':20s} - NOT INSTALLED (required for GUI)")
        all_ok = False
    
    print_header("Checking System Components")
    
    # Check camera
    camera_ok = check_camera()
    
    # Check model file
    model_ok = check_model_file()
    
    print_header("Version Information")
    
    print(f"NumPy:      {get_version('numpy')}")
    print(f"OpenCV:     {get_version('cv2')}")
    print(f"TensorFlow: {get_version('tensorflow')}")
    print(f"MediaPipe:  {get_version('mediapipe')}")
    print(f"Pillow:     {get_version('PIL')}")
    
    print_header("Installation Summary")
    
    if all_ok and camera_ok:
        print("\n✅ All dependencies installed correctly!")
        print("✅ Camera is accessible!")
        
        if model_ok:
            print("✅ Model file found!")
            print("\n🚀 You're ready to run the application!")
            print("\nRun: python sign_language_app.py")
        else:
            print("\n⚠️  No model file found.")
            print("   Add your trained model (.h5 or .keras) to the directory")
            print("   or update MODEL_PATH in config.py")
            print("\n   You can still run the app for testing (hand detection only)")
    else:
        print("\n❌ Some components are missing!")
        print("\n📦 Install missing dependencies:")
        print("   pip install -r requirements.txt")
        
        if not camera_ok:
            print("\n📷 Camera issues:")
            print("   - Check camera permissions")
            print("   - Ensure no other app is using the camera")
            print("   - Try a different camera index in config.py")
    
    print("\n" + "="*60)
    print()
    
    return 0 if (all_ok and camera_ok) else 1

if __name__ == "__main__":
    exit(main())
