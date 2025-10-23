#!/usr/bin/env python3
"""
Test script for Sign Language Detection Application
"""

import requests
import json
import base64
import numpy as np
from PIL import Image
import io

def create_test_image():
    """Create a test image for testing the API"""
    # Create a simple test image (64x64 RGB)
    image_array = np.random.randint(0, 255, (64, 64, 3), dtype=np.uint8)
    image = Image.fromarray(image_array)
    
    # Convert to base64
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    image_data = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/jpeg;base64,{image_data}"

def test_predict_endpoint():
    """Test the predict endpoint"""
    print("🧪 Testing predict endpoint...")
    
    try:
        # Create test image
        test_image = create_test_image()
        
        # Send request
        response = requests.post('http://localhost:5000/predict', 
                               json={'image': test_image},
                               timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Predict endpoint working!")
                print(f"   Predicted letter: {result.get('letter', 'N/A')}")
                print(f"   Confidence: {result.get('confidence', 0):.2f}")
                return True
            else:
                print(f"❌ Predict endpoint returned error: {result.get('error')}")
                return False
        else:
            print(f"❌ Predict endpoint returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the application. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Error testing predict endpoint: {e}")
        return False

def test_process_sentence_endpoint():
    """Test the process sentence endpoint"""
    print("\n🧪 Testing process sentence endpoint...")
    
    try:
        # Test with sample letters
        test_letters = ['H', 'E', 'L', 'L', 'O', 'space', 'W', 'O', 'R', 'L', 'D']
        
        response = requests.post('http://localhost:5000/process_sentence',
                               json={'letters': test_letters},
                               timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print(f"✅ Process sentence endpoint working!")
                print(f"   Input letters: {test_letters}")
                print(f"   Processed sentence: '{result.get('sentence', 'N/A')}'")
                return True
            else:
                print(f"❌ Process sentence endpoint returned error: {result.get('error')}")
                return False
        else:
            print(f"❌ Process sentence endpoint returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the application. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Error testing process sentence endpoint: {e}")
        return False

def test_main_page():
    """Test if the main page loads"""
    print("\n🧪 Testing main page...")
    
    try:
        response = requests.get('http://localhost:5000/', timeout=10)
        
        if response.status_code == 200:
            if 'Sign Language Detector' in response.text:
                print("✅ Main page loads successfully!")
                return True
            else:
                print("❌ Main page content seems incorrect")
                return False
        else:
            print(f"❌ Main page returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the application. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Error testing main page: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Sign Language Detection Application")
    print("=" * 50)
    
    # Check if requests is available
    try:
        import requests
    except ImportError:
        print("❌ 'requests' library not found. Install it with: pip install requests")
        return
    
    # Run tests
    tests = [
        test_main_page,
        test_predict_endpoint,
        test_process_sentence_endpoint
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the application setup.")
        print("\nTroubleshooting:")
        print("1. Make sure the application is running: python app.py")
        print("2. Check that the model file exists: sign_language_model.h5")
        print("3. Verify all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()