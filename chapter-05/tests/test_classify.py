import logging
from types import SimpleNamespace

from classifier import classify as module
from classifier.classify import classify


def fake_model(reply):
    """Return a stand-in for ask() that gives a fixed answer and records calls."""
    calls = []

    def fake_ask(question):
        calls.append(question)
        return reply

    return fake_ask, calls


def test_billing_ticket(monkeypatch):
    fake_ask, _ = fake_model("billing")
    monkeypatch.setattr(module, "ask", fake_ask)
    assert classify("My card was charged twice") == "billing"


def test_technical_ticket(monkeypatch):
    fake_ask, _ = fake_model("technical")
    monkeypatch.setattr(module, "ask", fake_ask)
    assert classify("The app crashes when I open it") == "technical"


def test_empty_input_is_other_and_makes_no_model_call(monkeypatch):
    fake_ask, calls = fake_model("billing")
    monkeypatch.setattr(module, "ask", fake_ask)
    assert classify("") == "other"
    assert classify("   ") == "other"
    assert calls == []


def test_label_is_cleaned_to_lowercase(monkeypatch):
    fake_ask, _ = fake_model("Billing.\n")
    monkeypatch.setattr(module, "ask", fake_ask)
    assert classify("I was overcharged") == "billing"


def test_unexpected_reply_becomes_other(monkeypatch):
    fake_ask, _ = fake_model("Check your API key in .env")
    monkeypatch.setattr(module, "ask", fake_ask)
    assert classify("Anything") == "other"


def test_model_call_is_logged_without_ticket_text(monkeypatch, caplog):
    fake_interaction = SimpleNamespace(
        output_text="billing",
        usage=SimpleNamespace(input_tokens=12, output_tokens=3),
    )
    fake_client = SimpleNamespace(
        interactions=SimpleNamespace(create=lambda model, input: fake_interaction)
    )
    monkeypatch.setattr(module, "_get_client", lambda: fake_client)
    with caplog.at_level(logging.INFO):
        answer = module.ask("secret ticket text")
    assert answer == "billing"
    assert "input_tokens=12" in caplog.text
    assert "output_tokens=3" in caplog.text
    assert "secret ticket text" not in caplog.text
