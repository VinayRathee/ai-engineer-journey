"""Entry point: ties classify.py and storage.py together."""
import argparse
import logging
import os
import time
from pathlib import Path

from classifier.classify import ask, classify
from classifier.storage import read_tickets, save_json, write_results

ROOT = Path(__file__).resolve().parents[2]
logger = logging.getLogger(__name__)


def setup_logging():
    """Log to the screen and to logs/classifier.log."""
    level = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_dir = ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_dir / "classifier.log", encoding="utf-8")],
    )


def pick_evenly(tickets, limit):
    """Pick `limit` tickets spread evenly across the list (all of them if limit is None)."""
    if limit is None or limit >= len(tickets):
        return tickets
    return [tickets[int(i * len(tickets) / limit)] for i in range(limit)]


def run_pipeline(input_path, output_path, limit=None):
    tickets = pick_evenly(read_tickets(input_path), limit)
    logger.info("classifying %d tickets", len(tickets))
    delay = float(os.environ.get("REQUEST_DELAY_SECONDS", "0"))
    rows = []
    for t in tickets:
        rows.append({"id": t["id"], "text": t["text"], "label": classify(t["text"])})
        time.sleep(delay)
    write_results(output_path, rows)
    logger.info("wrote %s", output_path)


def run_demo(output_path):
    """The original chapter 4 behaviour: two questions saved to answers.json."""
    questions = ["What is Python?", "What is an API?"]
    data = {"answers": [{"question": q, "answer": ask(q)} for q in questions]}
    save_json(output_path, data)
    logger.info("wrote %s", output_path)


def main():
    parser = argparse.ArgumentParser(description="Support ticket classifier")
    parser.add_argument("--demo", action="store_true", help="run the chapter 4 two-question demo")
    parser.add_argument("--limit", type=int, help="classify only this many tickets (spread evenly)")
    args = parser.parse_args()
    setup_logging()
    if args.demo:
        run_demo(ROOT / "answers.json")
    else:
        run_pipeline(ROOT / "tickets.csv", ROOT / "classified.csv", args.limit)


if __name__ == "__main__":
    main()