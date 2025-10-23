# Sign2Text Desktop App

A professional PySide6 desktop application scaffold for real-time sign-language to text. You can plug your own model via a simple Python plugin class implementing `BaseRecognizer`.

## Quick start

1. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the app:

```bash
python -m app.main
```

3. Load your model plugin: Toolbar → "Load Model Plugin" and select your `.py` file.

## Plugin API

Your plugin must implement the following interface:

```python
class BaseRecognizer(Protocol):
    labels: Sequence[str]
    def load(self) -> None: ...
    def predict(self, image_bgr: np.ndarray) -> Prediction: ...
    def get_labels(self) -> Sequence[str]: ...
```

- Input to `predict` is a NumPy `HxWx3` `uint8` BGR image cropped from the ROI.
- Return a `Prediction(label: str, confidence: float, timestamp_s: float)`.
- Emit labels such as "A".."Z", "space", "delete".

A ready-to-use example is available at `app/plugins/dummy_recognizer.py`.
