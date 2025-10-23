# 🚀 QUICK START - Sign Language Detection App

Get started in 3 simple steps!

## ⚡ Fast Setup (5 minutes)

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Export Your Model

In your Jupyter notebook, add this cell at the end:

```python
# Save your trained model
model.save('asl_model.h5')
print("✓ Model saved!")
```

### 3️⃣ Run the App

```bash
python sign_language_app.py
```

That's it! 🎉

---

## 📱 Using the App

1. Click **"Start Camera"**
2. Show hand signs to the camera
3. Watch text appear automatically
4. Click **"Save to Text File"** when done

---

## ⚙️ Configuration (Optional)

Edit `config.py` to customize:

```python
MODEL_PATH = "asl_model.h5"  # Your model filename
IMG_SIZE = 64                 # Model input size (64, 128, etc.)
STABILITY_THRESHOLD = 5       # Lower = faster, Higher = more stable
```

---

## 🔍 Verify Installation

Check if everything is installed correctly:

```bash
python test_installation.py
```

---

## 📚 Need More Help?

- **Detailed Guide**: See `README_APPLICATION.md`
- **Setup Help**: See `SETUP_GUIDE.md`
- **Model Export**: Run `python export_model_from_notebook.py`

---

## 🎯 What You Get

✅ Real-time sign language detection  
✅ Professional GUI interface  
✅ Text conversion and saving  
✅ ASL alphabet reference  
✅ High accuracy with stability control  

---

## 💡 Tips

- Use good lighting
- Keep hand centered in frame
- Hold each sign for 1-2 seconds
- Use plain background

---

**Ready? Let's go! 🤟**

```bash
python sign_language_app.py
```
