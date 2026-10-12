"""Run the project from the project folder: python run.py  (or: python run.py --demo)"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from classifier.main import main  # noqa: E402

if __name__ == "__main__":
    main()
