"""
Export Model from Jupyter Notebook
This script helps you export your trained model from the notebook
and prepare it for use with the sign language detection application
"""

import os
import json
from pathlib import Path

def create_model_export_instructions():
    """Create instructions for exporting model from notebook"""
    
    instructions = """
╔════════════════════════════════════════════════════════════════╗
║  How to Export Your Model from Jupyter Notebook               ║
╚════════════════════════════════════════════════════════════════╝

Follow these steps in your Jupyter notebook (LSignLD.ipynb):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1: After Training Your Model
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Add this code cell at the end of your notebook:

```python
# Save the model
model.save('asl_model.h5')
print("✓ Model saved as 'asl_model.h5'")

# Alternative: Save in Keras format
# model.save('asl_model.keras')
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2: Save Class Labels (Important!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Add this code to save your class labels:

```python
import json

# Your class labels (update based on your dataset)
class_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 
                'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 
                'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# Save to JSON
with open('class_labels.json', 'w') as f:
    json.dump(class_labels, f)
print("✓ Class labels saved")
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3: Save Model Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
# Get input shape from your model
input_shape = model.input_shape
img_size = input_shape[1]  # Assuming square images

model_config = {
    'model_file': 'asl_model.h5',
    'img_size': img_size,
    'input_shape': list(input_shape),
    'num_classes': len(class_labels),
    'class_labels': class_labels
}

with open('model_config.json', 'w') as f:
    json.dump(model_config, f, indent=2)
print("✓ Model configuration saved")
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 4: Test Your Saved Model
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```python
# Load and test the saved model
import tensorflow as tf
import numpy as np

loaded_model = tf.keras.models.load_model('asl_model.h5')
print("✓ Model loaded successfully!")

# Test with a random image
test_input = np.random.rand(1, img_size, img_size, 3)
prediction = loaded_model.predict(test_input)
print(f"✓ Model prediction works! Shape: {prediction.shape}")
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 5: Update Application Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Open 'config.py' and update:

```python
MODEL_PATH = "asl_model.h5"  # Your model filename
IMG_SIZE = 64                # Your model's input size
CLASS_LABELS = [...]         # Your class labels
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALTERNATIVE: Quick Export Function
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Add this complete function to your notebook:

```python
def export_model_for_app(model, class_labels, model_name='asl_model'):
    \"\"\"Export model and configuration for the app\"\"\"
    import json
    
    # Save model
    model.save(f'{model_name}.h5')
    print(f"✓ Model saved: {model_name}.h5")
    
    # Get model info
    img_size = model.input_shape[1]
    
    # Save configuration
    config = {
        'model_file': f'{model_name}.h5',
        'img_size': img_size,
        'input_shape': list(model.input_shape),
        'num_classes': len(class_labels),
        'class_labels': class_labels
    }
    
    with open('model_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    print("✓ Configuration saved: model_config.json")
    
    # Save just class labels
    with open('class_labels.json', 'w') as f:
        json.dump(class_labels, f)
    print("✓ Class labels saved: class_labels.json")
    
    # Test loading
    import tensorflow as tf
    loaded = tf.keras.models.load_model(f'{model_name}.h5')
    print("✓ Model verified - ready to use!")
    
    print("\\n" + "="*60)
    print("🎉 Export complete! Your model is ready for the app!")
    print("="*60)
    print(f"\\nNext steps:")
    print(f"1. Update config.py: MODEL_PATH = '{model_name}.h5'")
    print(f"2. Update config.py: IMG_SIZE = {img_size}")
    print(f"3. Run: python sign_language_app.py")

# Usage:
# export_model_for_app(model, class_labels, 'my_asl_model')
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FILES YOU SHOULD HAVE AFTER EXPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ asl_model.h5          - Your trained model
✓ model_config.json     - Model configuration (optional)
✓ class_labels.json     - Class labels (optional)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMMON ISSUES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Issue: "Can't save model"
→ Use model.save('model.h5') not model.save_weights()

Issue: "Model won't load in app"
→ Check TensorFlow versions match between notebook and app

Issue: "Wrong predictions"
→ Verify CLASS_LABELS order matches training order

Issue: "Input shape error"
→ Check IMG_SIZE in config.py matches model input size

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For more help, see README_APPLICATION.md

"""
    
    return instructions

def check_exported_files():
    """Check if model files have been exported"""
    print("\n" + "="*60)
    print("Checking for exported model files...")
    print("="*60 + "\n")
    
    files_to_check = {
        'Model Files': ['model.h5', 'model.keras', 'asl_model.h5', 'sign_language_model.h5'],
        'Configuration Files': ['model_config.json', 'class_labels.json']
    }
    
    found_model = False
    found_config = False
    
    for category, files in files_to_check.items():
        print(f"\n{category}:")
        for file in files:
            if os.path.exists(file):
                size = os.path.getsize(file)
                size_mb = size / (1024 * 1024)
                print(f"  ✓ {file:30s} ({size_mb:.2f} MB)")
                if category == 'Model Files':
                    found_model = True
                else:
                    found_config = True
            else:
                print(f"  ✗ {file:30s} (not found)")
    
    print("\n" + "="*60)
    
    if found_model:
        print("✅ Model file found!")
        if found_config:
            print("✅ Configuration files found!")
            print("\n🚀 Ready to use with the application!")
        else:
            print("\n⚠️  Configuration files missing (optional)")
            print("   You can still use the app, just update config.py manually")
    else:
        print("\n❌ No model file found!")
        print("   Please export your model from the notebook first")
        print("   See instructions above")
    
    print("="*60 + "\n")

def create_notebook_cell_snippets():
    """Create code snippets for notebook"""
    
    snippets = {
        'save_model.py': """# Save your trained model
model.save('asl_model.h5')
print("✓ Model saved successfully!")
""",
        
        'export_complete.py': """# Complete export function
import json

def export_model_for_app(model, class_labels, model_name='asl_model'):
    # Save model
    model.save(f'{model_name}.h5')
    
    # Get model info
    img_size = model.input_shape[1]
    
    # Save configuration
    config = {
        'model_file': f'{model_name}.h5',
        'img_size': img_size,
        'num_classes': len(class_labels),
        'class_labels': class_labels
    }
    
    with open('model_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    with open('class_labels.json', 'w') as f:
        json.dump(class_labels, f)
    
    print(f"✓ Export complete: {model_name}.h5")
    print(f"✓ Image size: {img_size}x{img_size}")
    print(f"✓ Classes: {len(class_labels)}")

# Define your class labels
class_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 
                'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 
                'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

# Export
export_model_for_app(model, class_labels, 'my_asl_model')
"""
    }
    
    # Save snippets
    snippets_dir = Path('notebook_snippets')
    snippets_dir.mkdir(exist_ok=True)
    
    for filename, code in snippets.items():
        filepath = snippets_dir / filename
        with open(filepath, 'w') as f:
            f.write(code)
    
    print(f"✓ Code snippets saved to '{snippets_dir}/' directory")
    print("  You can copy-paste these into your notebook")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  Model Export Helper")
    print("="*60)
    
    # Show instructions
    instructions = create_model_export_instructions()
    print(instructions)
    
    # Check for existing files
    check_exported_files()
    
    # Create code snippets
    print("\nCreating notebook code snippets...")
    create_notebook_cell_snippets()
    print()
