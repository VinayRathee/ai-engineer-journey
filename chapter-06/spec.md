# CV Summary Tool: Spec
## 1. Goal
Read one CV text file, use the Gemini API to write a two-line summary and a score from 0 to 100, and save the result in a SQLite database.

## 2. Users
A recruiter types one command with the path of a CV file, and sees the summary and score on the screen.
## 3. Inputs and outputs
Input: the path of one CV text file, given by the recruiter in the command.
Output on screen: the two-line summary and the score from 0 to 100.
Output in database: the CV text, the summary, the score, the model used and the cost of the call.
## 4. Constraints
- Use Python 3.14, the google-genai library, python-dotenv and the built-in sqlite3 module.
- Put all new code inside the chapter-06 folder. Do not change anything in chapter-03, chapter-04 or chapter-05.
- Never read, print or edit the .env file. The API key is read from the environment only.
- Write comments and documentation in British English.
- Log every model call: model name, input tokens, output tokens and cost.
- Add pinned dependencies in a new requirements.txt inside chapter-06.
## 5. Acceptance criteria
- [X] Given a valid CV text file, the tool prints a two-line summary on the screen.
- [X] The tool also prints a score, which is a whole number from 0 to 100.
- [X] The database row contains the CV text, summary, score, model name and cost.
- [X] If the file path does not exist, the tool prints a clear error message, does not crash and saves nothing.
- [X] If the file is empty, the tool prints a clear error message and saves nothing.
- [X] Tests use a mocked model and never call the real Gemini API.
## 6. Out of scope
- No web page, graphical interface or frontend. Only the command line.
- No batch mode. The tool handles one CV file per command.
- No PDF or Word files. Only plain text files.
- No login, users or permissions.
- No Postgres or Supabase. Only SQLite.
- No Docker, deployment or cloud setup.
- No changes to chapter-03, chapter-04 or chapter-05.