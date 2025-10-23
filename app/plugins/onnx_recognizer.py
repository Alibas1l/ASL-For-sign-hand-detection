from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence, List

import numpy as np
import cv2
import onnxruntime as ort

from app.core.recognizer import BaseRecognizer, Prediction


class OnnxRecognizer:
    """Generic ONNX classifier recognizer.

    Expected model: image classification with a single output of class scores.
    Input shape is assumed to be (1, 3, H, W) with RGB values in [0,1].
    You can modify preprocessing as needed.
    """

    def __init__(self, model_path: str | None = None, labels_path: str | None = None, input_size: int = 224):
        self.model_path = model_path or str(Path(__file__).resolve().parents[1] / "assets" / "sign_letters.onnx")
        self.labels_path = labels_path or str(Path(__file__).resolve().parents[1] / "assets" / "labels.txt")
        self.input_size = input_size
        self.session: ort.InferenceSession | None = None
        self._labels: List[str] = []

    @property
    def labels(self) -> Sequence[str]:
        return self._labels

    def load(self) -> None:
        mp = Path(self.model_path)
        if not mp.exists():
            raise FileNotFoundError(f"ONNX model not found at {mp}. Update path in OnnxRecognizer().")

        so = ort.SessionOptions()
        providers = ["CPUExecutionProvider"]
        self.session = ort.InferenceSession(str(mp), sess_options=so, providers=providers)

        lp = Path(self.labels_path)
        if lp.exists():
            self._labels = [line.strip() for line in lp.read_text(encoding="utf-8").splitlines() if line.strip()]
        else:
            # Default: A-Z, space, delete
            self._labels = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + ["space", "delete"]

    def predict(self, image_bgr: np.ndarray) -> Prediction:
        assert self.session is not None, "Call load() before predict()"

        # Preprocess
        img = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (self.input_size, self.input_size), interpolation=cv2.INTER_AREA)
        img = img.astype(np.float32) / 255.0
        # CHW
        img = np.transpose(img, (2, 0, 1))[None, ...]

        input_name = self.session.get_inputs()[0].name
        outputs = self.session.run(None, {input_name: img})
        logits = outputs[0].squeeze()
        # Softmax
        exp = np.exp(logits - np.max(logits))
        probs = exp / np.sum(exp)
        idx = int(np.argmax(probs))
        label = self._labels[idx] if idx < len(self._labels) else str(idx)
        conf = float(probs[idx])
        return Prediction(label=label, confidence=conf, timestamp_s=float(cv2.getTickCount() / cv2.getTickFrequency()))

    def get_labels(self) -> Sequence[str]:
        return self._labels
