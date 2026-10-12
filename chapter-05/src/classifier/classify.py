"""The model call and the classification logic."""
import logging
import os
import time
import uuid

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

LABELS = ("billing", "technical", "other")
INSTRUCTION = "Classify this ticket as billing, technical or other. Reply with one word."
ERROR_MESSAGE = "Check your API key in .env"
DEFAULT_MODEL = "gemini-3.8-flash"

_client = None


def _get_client():
    """Create the Gemini client the first time it is needed (not at import)."""
    global _client
    if _client is None:
        from google import genai

        _client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    return _client


def _read_field(usage, names):
    """Return the first token count found under any of the given names."""
    for name in names:
        value = usage.get(name) if isinstance(usage, dict) else getattr(usage, name, None)
        if value is not None:
            return value
    return None


def _log_call(request_id, model, interaction, duration):
    """Write one log line per model call: metadata only, never the text."""
    try:
        usage = getattr(interaction, "usage", None)
        logger.debug("request_id=%s raw usage: %r", request_id, usage)
        in_tokens = _read_field(usage, ("input_tokens", "total_input_tokens", "prompt_token_count"))
        out_tokens = _read_field(usage, ("output_tokens", "total_output_tokens", "candidates_token_count"))
        price_in = float(os.environ.get("PRICE_INPUT_PER_MILLION", "0"))
        price_out = float(os.environ.get("PRICE_OUTPUT_PER_MILLION", "0"))
        cost = ((in_tokens or 0) * price_in + (out_tokens or 0) * price_out) / 1_000_000
        if in_tokens is None or out_tokens is None:
            logger.warning(
                "request_id=%s token counts not found in response; run with LOG_LEVEL=DEBUG to see raw usage",
                request_id,
            )
        logger.info(
            "model_call request_id=%s model=%s input_tokens=%s output_tokens=%s cost_usd=%.6f duration_s=%.2f",
            request_id, model, in_tokens, out_tokens, cost, duration,
        )
    except Exception:  # logging must never break the app
        logger.exception("request_id=%s could not write the model-call log line", request_id)


def ask(question):
    """Send one question to the model and return the answer text."""
    model = os.environ.get("GEMINI_MODEL", DEFAULT_MODEL)
    request_id = uuid.uuid4().hex[:8]
    start = time.perf_counter()
    try:
        interaction = _get_client().interactions.create(model=model, input=question)
        _log_call(request_id, model, interaction, time.perf_counter() - start)
        return interaction.output_text
    except Exception:
        logger.exception("request_id=%s model call failed (model=%s)", request_id, model)
        return ERROR_MESSAGE


def classify(ticket):
    """Return 'billing', 'technical' or 'other' for one support ticket."""
    if not ticket or not ticket.strip():
        return "other"  # empty input: no model call, no cost
    reply = ask(f"{INSTRUCTION}\n\nTicket: {ticket}")
    label = reply.strip().lower().strip(".!?\"' \n")
    if label not in LABELS:
        logger.warning("unexpected reply from model (length=%d); using 'other'", len(reply))
        return "other"
    return label
