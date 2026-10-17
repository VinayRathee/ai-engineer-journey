"""Tests for main entry point module."""
import sys
from types import SimpleNamespace

import pytest

from cv_summary import main as module
from cv_summary.db import get_summary


def test_main_file_does_not_exist(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["run.py", "nonexistent_cv.txt"])
    module.main()
    captured = capsys.readouterr()
    assert "does not exist" in captured.err


def test_main_file_empty(monkeypatch, capsys, tmp_path):
    empty_file = tmp_path / "empty.txt"
    empty_file.write_text("")
    monkeypatch.setattr(sys, "argv", ["run.py", str(empty_file)])
    module.main()
    captured = capsys.readouterr()
    assert "is empty" in captured.err


def test_main_analyzer_value_error(monkeypatch, capsys, tmp_path):
    cv_file = tmp_path / "cv.txt"
    cv_file.write_text("Some CV text")

    def mock_analyze(text):
        raise ValueError("Invalid model output format")

    monkeypatch.setattr(module, "analyze_cv", mock_analyze)
    monkeypatch.setattr(sys, "argv", ["run.py", str(cv_file)])
    module.main()
    captured = capsys.readouterr()
    assert "Error: Invalid model output format" in captured.err


def test_main_success(monkeypatch, capsys, tmp_path):
    cv_file = tmp_path / "cv.txt"
    cv_file.write_text("Senior developer with Python experience.")
    db_file = tmp_path / "test_summary.db"

    def mock_analyze(text):
        return {
            "cv_text": text,
            "summary": "Great developer.\nPython expert.",
            "score": 92,
            "model": "gemini-3.8-flash",
            "cost": 0.0002,
        }

    monkeypatch.setattr(module, "analyze_cv", mock_analyze)
    monkeypatch.setattr(sys, "argv", ["run.py", str(cv_file), "--db", str(db_file)])

    module.main()
    captured = capsys.readouterr()
    assert "Summary:" in captured.out
    assert "Score: 92" in captured.out

    # Verify saved in DB
    from cv_summary.db import get_connection
    with get_connection(db_file) as conn:
        cursor = conn.execute("SELECT * FROM cv_summaries")
        row = cursor.fetchone()
        assert row is not None
        assert row["score"] == 92
        assert row["model"] == "gemini-3.8-flash"
