"""Entry point: ties analyzer.py and db.py together."""
import argparse
import logging
import os
import sys
from pathlib import Path

from cv_summary.analyzer import analyze_cv
from cv_summary.db import init_db, save_summary

ROOT = Path(__file__).resolve().parents[2]
logger = logging.getLogger(__name__)


def setup_logging():
    """Log to the screen and to logs/cv_summary.log."""
    level = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_dir = ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_dir / "cv_summary.log", encoding="utf-8")],
    )


def main():
    parser = argparse.ArgumentParser(description="CV Summary Tool")
    parser.add_argument("cv_path", type=str, help="path to the CV text file")
    parser.add_argument("--db", type=str, default="cv_summary.db", help="path to SQLite database")
    args = parser.parse_args()

    setup_logging()

    cv_path = Path(args.cv_path)
    if not cv_path.exists():
        print(f"Error: File '{cv_path}' does not exist.", file=sys.stderr)
        return

    try:
        cv_text = cv_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error: Could not read file '{cv_path}': {e}", file=sys.stderr)
        return

    if not cv_text or not cv_text.strip():
        print(f"Error: File '{cv_path}' is empty.", file=sys.stderr)
        return

    try:
        result = analyze_cv(cv_text)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return
    except Exception as e:
        print(f"Error analyzing CV: {e}", file=sys.stderr)
        return

    try:
        init_db(args.db)
        save_summary(
            cv_text=result["cv_text"],
            summary=result["summary"],
            score=result["score"],
            model=result["model"],
            cost=result["cost"],
            db_path=args.db,
        )
    except Exception as e:
        print(f"Error saving to database: {e}", file=sys.stderr)
        return

    print("Summary:")
    print(result["summary"])
    print(f"Score: {result['score']}")


if __name__ == "__main__":
    main()
