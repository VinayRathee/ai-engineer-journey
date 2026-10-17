"""Database management module for storing CV summaries using SQLite."""
import sqlite3
from pathlib import Path
from typing import Any, Dict, Optional, Union

DEFAULT_DB_PATH = Path("cv_summary.db")


def get_connection(db_path: Union[str, Path] = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Create and return a database connection."""
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Union[str, Path] = DEFAULT_DB_PATH) -> None:
    """Initialise the SQLite database and create required tables if they do not exist."""
    with get_connection(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cv_summaries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cv_text TEXT NOT NULL,
                summary TEXT NOT NULL,
                score INTEGER NOT NULL,
                model TEXT NOT NULL,
                cost REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def save_summary(
    cv_text: str,
    summary: str,
    score: int,
    model: str,
    cost: float,
    db_path: Union[str, Path] = DEFAULT_DB_PATH,
) -> int:
    """Save a CV summary record to the database and return the inserted row ID."""
    init_db(db_path)
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            INSERT INTO cv_summaries (cv_text, summary, score, model, cost)
            VALUES (?, ?, ?, ?, ?)
            """,
            (cv_text, summary, score, model, cost),
        )
        conn.commit()
        return cursor.lastrowid


def get_summary(
    record_id: int,
    db_path: Union[str, Path] = DEFAULT_DB_PATH,
) -> Optional[Dict[str, Any]]:
    """Retrieve a single CV summary record by its ID."""
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            """
            SELECT id, cv_text, summary, score, model, cost, created_at
            FROM cv_summaries
            WHERE id = ?
            """,
            (record_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return dict(row)
