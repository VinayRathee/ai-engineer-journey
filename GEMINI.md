# AI Engineer Journey

## What this project is
A learning repository for the book "AI Engineering: From Zero to Production". Each chapter has its own folder (chapter-03, chapter-04, chapter-05 and so on). The current work is a support ticket classifier that sends tickets to the Gemini API and labels them.

## Stack
- Python 3.14
- pytest for tests
- python-dotenv for loading secrets from a .env file
- google-genai for calling the Gemini API

## How to run tests
Open the project folder inside the repository and run: pytest

## Rules
- Never put secrets in code. API keys live in .env only.
- Never read, print or edit the .env file.
- Pin every dependency in requirements.txt with an exact version.
- Write comments and documentation in British English.
- Log every model call: model name, input tokens, output tokens and cost.
- Mock the model in tests so they do not call the paid API.

## Behaviour rules
- Always show a plan before editing more than one file.
- Never delete files without asking.
- Do not add features, libraries or files that I did not ask for.
- After a change, run the tests and tell me the result.