"""Run the project from the project folder: python run.py path/to/cv.txt"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from cv_summary.main import main  # noqa: E402

if __name__ == "__main__":
    main()
