# Messy To-Do CLI Application

A simple command-line to-do list application built in Python as part of Chapter 6b of the "AI Engineering: From Zero to Production" learning repository.

## Features

- **Add Tasks**: Add new task items with custom titles to your to-do list.
- **List Tasks**: View all stored tasks along with their current status (e.g. `[PENDING]`).
- **Persistent Storage**: Automatically serialises and persists tasks to local JSON storage (`todos.json`).

## Running the Application

All commands must be executed from the repository root directory using Python's module execution flag (`-m`).

### Adding a Task
```bash
python -m chapter-06b.messy-todo.main add "Buy groceries"
```

### Listing Tasks
```bash
python -m chapter-06b.messy-todo.main list
```

## Running Tests

The test suite uses `pytest` to verify task creation, formatting, and state management. To run the tests from the repository root, execute:

```bash
pytest chapter-06b/messy-todo/tests
```
