#!/usr/bin/env python3
"""
Setup script for Sign Language Detection Application
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}:")
        print(f"   Command: {command}")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible!")
    return True

def install_requirements():
    """Install required packages"""
    return run_command("pip install -r requirements.txt", "Installing requirements")

def create_directories():
    """Create necessary directories"""
    directories = ['templates', 'static/css', 'static/js', 'models']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def check_model_file():
    """Check if model file exists"""
    model_file = 'sign_language_model.h5'
    if os.path.exists(model_file):
        print(f"✅ Model file found: {model_file}")
        return True
    else:
        print(f"⚠️  Model file not found: {model_file}")
        print("   Please run 'python convert_model.py' to create the model file")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up Sign Language Detection Application")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    print("\n📁 Creating directories...")
    create_directories()
    
    # Install requirements
    print("\n📦 Installing dependencies...")
    if not install_requirements():
        print("❌ Failed to install requirements. Please check your Python environment.")
        sys.exit(1)
    
    # Check model file
    print("\n🤖 Checking model file...")
    model_exists = check_model_file()
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    
    if model_exists:
        print("\n✅ Ready to run the application!")
        print("   Run: python app.py")
        print("   Then open: http://localhost:5000")
    else:
        print("\n⚠️  Setup completed, but model file is missing.")
        print("   Next steps:")
        print("   1. Run: python convert_model.py")
        print("   2. Run: python app.py")
        print("   3. Open: http://localhost:5000")
    
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()