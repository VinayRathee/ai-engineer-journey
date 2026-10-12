# Support ticket classifier

Reads support tickets from `tickets.csv`, asks a Gemini model to label each one
(`billing`, `technical` or `other`), and writes `classified.csv`.

## Setup

1. Create and activate a virtual environment:
   - `python -m venv .venv`
   - Windows PowerShell: `.venv\Scripts\Activate.ps1`
2. Install the pinned dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and put your Gemini API key in it.

## Run

- Classify the tickets: `python run.py`
- The chapter 4 two-question demo: `python run.py --demo`

Every model call writes a log line (model, tokens, cost, duration) to
`logs/classifier.log` and to the screen.

## Test

`pytest` (the tests use a fake model, so they cost nothing and need no key).

## What each file is for

<!-- Step 2 of the build: write one line per file, in your own words. -->

- `run.py`: to start the application
- `src/classifier/classify.py`:helps in classifying and shorting data
- `src/classifier/storage.py`:helps in saving and loading data
- `src/classifier/main.py`:main coordinater 
- `tests/test_classify.py`:it verify the work or code
- `pytest.ini`:it sets the rules for the pytest testing
- `.env.example`:sample for api key
- `.gitignore`:helps to hide secret folders
- `requirements.txt`:all external python libraries jo install karte time..
- `tickets.csv`:these are datafiles in which theor is info. of tickets

## Why dependencies are pinned

dependence are pinned so that kalko koi new verson project ko tod na sake

## Log level for a live system

<!-- Try it yourself: which level, and why? -->
