from __future__ import annotations

import importlib
import inspect
from pathlib import Path
from types import ModuleType
from typing import Optional, Type

from .recognizer import BaseRecognizer


def load_plugin(module_path: str, class_name: Optional[str] = None) -> BaseRecognizer:
    """Dynamically load a recognizer plugin.

    module_path can be:
      - dotted path like 'app.plugins.digits_to_letters'
      - file path like '/path/to/mymodel.py'
    If class_name is not provided, the first class in the module implementing
    BaseRecognizer will be used.
    """
    module: ModuleType
    if module_path.endswith('.py') or Path(module_path).exists():
        # Load by file path
        import importlib.util

        spec = importlib.util.spec_from_file_location("user_plugin", module_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load module from {module_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)  # type: ignore[arg-type]
    else:
        module = importlib.import_module(module_path)

    # Find recognizer class
    recognizer_cls: Optional[Type] = None
    if class_name:
        recognizer_cls = getattr(module, class_name, None)
    else:
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if _implements_protocol(obj, BaseRecognizer):
                recognizer_cls = obj
                break
    if recognizer_cls is None:
        raise ImportError("No recognizer class found in module")

    recognizer = recognizer_cls()  # type: ignore[call-arg]
    if not _implements_protocol(recognizer, BaseRecognizer):
        raise TypeError("Loaded class does not implement BaseRecognizer")

    recognizer.load()
    return recognizer


def _implements_protocol(obj, proto):
    # Best-effort duck-typing check against Protocol
    required = ["load", "predict", "get_labels", "labels"]
    return all(hasattr(obj, name) for name in required)
