"""Reading and writing files (CSV and JSON). Later: the database."""
import csv
import json


def read_tickets(path):
    """Read tickets.csv (columns: id, text) and return a list of dicts."""
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_results(path, rows):
    """Write classified rows (id, text, label) to a CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "text", "label"])
        writer.writeheader()
        writer.writerows(rows)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
