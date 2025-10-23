#!/usr/bin/env python3
"""
Sign Language Detection Application Launcher

This script provides an easy way to launch the application with proper configuration.
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path
import time

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask', 'tensorflow', 'opencv-python', 'pillow', 'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Install missing dependencies"""
    print("📦 Installing required dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def check_model_files():
    """Check for available model files"""
    model_extensions = ['.h5', '.keras', '.pb']
    model_files = []
    
    for ext in model_extensions:
        model_files.extend(Path('.').glob(f'*{ext}'))
    
    return [str(f) for f in model_files]

def main():
    print("🤖 Sign Language Detection Application Launcher")
    print("=" * 55)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        install_choice = input("📥 Install missing dependencies? (y/n): ").lower().strip()
        
        if install_choice == 'y':
            if not install_dependencies():
                print("❌ Failed to install dependencies. Please install manually:")
                print("   pip install -r requirements.txt")
                return
        else:
            print("❌ Cannot run application without required dependencies.")
            return
    else:
        print("✅ All dependencies are installed!")
    
    # Check for model files
    print("\n🔍 Checking for model files...")
    model_files = check_model_files()
    
    if model_files:
        print("✅ Found model files:")
        for i, model in enumerate(model_files, 1):
            print(f"   {i}. {model}")
        
        if len(model_files) > 1:
            try:
                choice = int(input(f"\n📋 Select model to use (1-{len(model_files)}): ")) - 1
                if 0 <= choice < len(model_files):
                    selected_model = model_files[choice]
                else:
                    selected_model = model_files[0]
                    print(f"⚠️  Invalid choice, using: {selected_model}")
            except ValueError:
                selected_model = model_files[0]
                print(f"⚠️  Invalid input, using: {selected_model}")
        else:
            selected_model = model_files[0]
        
        print(f"🎯 Using model: {selected_model}")
        
        # Update app.py with selected model
        try:
            with open('app.py', 'r') as f:
                content = f.read()
            
            # Replace the model initialization line
            updated_content = content.replace(
                'detector = SignLanguageDetector()',
                f'detector = SignLanguageDetector(model_path="{selected_model}")'
            )
            
            with open('app.py', 'w') as f:
                f.write(updated_content)
            
            print("✅ Model configuration updated!")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not auto-configure model: {e}")
            print(f"   Please manually update app.py with model path: {selected_model}")
    
    else:
        print("⚠️  No model files found in current directory")
        print("💡 Place your trained model (.h5, .keras, or .pb) in this directory")
        print("   The application will run but predictions will not work until a model is loaded")
    
    # Create necessary directories
    os.makedirs('outputs', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    print("\n🚀 Starting the application...")
    print("📱 The application will open in your default web browser")
    print("🌐 URL: http://localhost:5000")
    print("⏹️  Press Ctrl+C to stop the application")
    
    # Start the Flask application
    try:
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:5000')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Import and run the Flask app
        from app import app
        app.run(debug=False, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("💡 Try running manually: python app.py")

if __name__ == "__main__":
    main()