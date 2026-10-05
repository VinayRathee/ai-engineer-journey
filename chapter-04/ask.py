import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def ask(question):
    try:
        interaction = client.interactions.create(
            model="gemini-3.8-flash",
            input=question
        )

        return interaction.output_text

    except Exception:
        return "Check your API key in .env"


answer1 = ask("What is Python?")
answer2 = ask("What is an API?")


data = {
    "answers": [
        {
            "question": "What is Python?",
            "answer": answer1
        },
        {
            "question": "What is an API?",
            "answer": answer2
        }
    ]
}


with open("answers.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)