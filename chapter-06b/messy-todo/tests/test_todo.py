import importlib
import pytest
from pathlib import Path

storage = importlib.import_module("chapter-06b.messy-todo.storage")
manager = importlib.import_module("chapter-06b.messy-todo.manager")
formatter = importlib.import_module("chapter-06b.messy-todo.formatter")


@pytest.fixture(autouse=True)
def isolate_storage(monkeypatch, tmp_path):
    """Ensure tests do not touch the real todos.json file."""
    test_file = tmp_path / "todos.json"
    monkeypatch.setattr(storage, "FILE_PATH", str(test_file))


def test_add_task_saves_non_empty_file():
    """1) After adding a task, the saved file contains that task and is not empty."""
    mgr = manager.TaskManager()
    mgr.addTask("Buy groceries")
    
    test_file = Path(storage.FILE_PATH)
    assert test_file.exists()
    content = test_file.read_text().strip()
    assert content != ""
    assert content != "[]"
    assert "Buy groceries" in content


def test_adding_two_tasks_does_not_crash_and_saves_both():
    """2) Adding two tasks in a row does not crash and both are saved."""
    mgr = manager.TaskManager()
    mgr.addTask("Task alpha")
    mgr.addTask("Task beta")
    
    items = mgr.getItems()
    assert len(items) == 2
    assert items[0].title == "Task alpha"
    assert items[1].title == "Task beta"
    
    # Verify persistence via a fresh TaskManager instance
    mgr_reloaded = manager.TaskManager()
    reloaded_items = mgr_reloaded.getItems()
    assert len(reloaded_items) == 2
    assert reloaded_items[0].title == "Task alpha"
    assert reloaded_items[1].title == "Task beta"


def test_new_task_labelled_pending():
    """3) A new task is labelled PENDING in the formatted output."""
    mgr = manager.TaskManager()
    mgr.addTask("Test pending state")
    items = mgr.getItems()
    
    output = formatter.formatOutput(items)
    assert "PENDING" in output
    assert "Test pending state" in output
    assert "[PENDING]" in output
