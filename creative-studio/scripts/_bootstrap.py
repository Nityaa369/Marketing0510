"""Lets `python scripts/<name>.py` import the studio package without installing it."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from studio.config import load_env  # noqa: E402

load_env()
