"""Tests for CV analyzer module."""
import logging
from types import SimpleNamespace

import pytest

from cv_summary import analyzer as module
from cv_summary.analyzer import analyze_cv, parse_response


def test_parse_response_success():
    response_text = "Summary: Experienced software engineer with Python skills.\nStrong background in system design.\nScore: 90"
    summary, score = parse_response(response_text)
    assert score == 90
    assert "Experienced software engineer" in summary


def test_parse_response_missing_score():
    response_text = "Summary: Experienced software engineer with Python skills."
    with pytest.raises(ValueError, match="Missing 'Score:' line"):
        parse_response(response_text)


def test_parse_response_score_out_of_range():
    response_text = "Summary: Summary text here.\nScore: 150"
    with pytest.raises(ValueError, match="outside the allowed range"):
        parse_response(response_text)


def test_parse_response_invalid_score_format():
    response_text = "Summary: Summary text here.\nScore: abc"
    with pytest.raises(ValueError, match="not a whole number"):
        parse_response(response_text)


def test_analyze_cv_success(monkeypatch):
    fake_interaction = SimpleNamespace(
        output_text="Summary: Python developer.\nGood communication.\nScore: 88",
        usage=SimpleNamespace(input_tokens=20, output_tokens=10),
    )
    fake_client = SimpleNamespace(
        interactions=SimpleNamespace(create=lambda model, input: fake_interaction)
    )
    monkeypatch.setattr(module, "_get_client", lambda: fake_client)

    result = analyze_cv("CV text content here")
    assert result["score"] == 88
    assert result["summary"] == "Python developer.\nGood communication."
    assert result["model"] == module.DEFAULT_MODEL
    assert result["cv_text"] == "CV text content here"
    assert result["cost"] >= 0.0


def test_empty_cv_raises_value_error():
    with pytest.raises(ValueError, match="CV text is empty"):
        analyze_cv("")
    with pytest.raises(ValueError, match="CV text is empty"):
        analyze_cv("   ")
