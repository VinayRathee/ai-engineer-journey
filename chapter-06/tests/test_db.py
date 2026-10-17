"""Tests for database management module."""
from cv_summary.db import get_summary, init_db, save_summary


def test_init_and_save_and_get_summary(tmp_path):
    db_path = tmp_path / "test_cv.db"
    init_db(db_path)

    record_id = save_summary(
        cv_text="John Doe Python Developer",
        summary="Experienced Python developer.\nStrong backend background.",
        score=85,
        model="gemini-3.8-flash",
        cost=0.0001,
        db_path=db_path,
    )

    assert record_id is not None
    assert isinstance(record_id, int)

    record = get_summary(record_id, db_path=db_path)
    assert record is not None
    assert record["cv_text"] == "John Doe Python Developer"
    assert record["summary"] == "Experienced Python developer.\nStrong backend background."
    assert record["score"] == 85
    assert record["model"] == "gemini-3.8-flash"
    assert record["cost"] == 0.0001
    assert "created_at" in record


def test_get_nonexistent_summary(tmp_path):
    db_path = tmp_path / "test_cv.db"
    init_db(db_path)
    record = get_summary(999, db_path=db_path)
    assert record is None
