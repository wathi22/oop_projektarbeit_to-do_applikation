from app.src.todo import Todo
import pytest

def test_todo_creation():
    todo = Todo(
        id=1, 
        title="Test To-Do", 
        description="Dies ist ein Test-To-Do", 
        priority=Todo.PRIORITY_HIGH,
        status=Todo.STATUS_TODO,
        progress=50,
        start_date="2024-01-01",
        due_date="2024-01-31",
        labels="Test,Pytest",
        todo_list_id=1
    )

    # Überprüfen, ob die Attribute korrekt gesetzt wurden
    assert todo.id == 1
    assert todo.title == "Test To-Do"  
    assert todo.description == "Dies ist ein Test-To-Do"
    assert todo.priority == Todo.PRIORITY_HIGH
    assert todo.status == Todo.STATUS_TODO
    assert todo.progress == 50
    assert todo.start_date == "2024-01-01"
    assert todo.due_date == "2024-01-31"
    assert todo.labels == "Test,Pytest"
    assert todo.todo_list_id == 1

def test_toggle_status():
    # Testet die Status-Übergänge: Backlog → To-Do → In Progress → Done → Backlog
    todo = Todo(status=Todo.STATUS_BACKLOG)
    todo.toggle_status()
    assert todo.status == Todo.STATUS_TODO
    todo.toggle_status()
    assert todo.status == Todo.STATUS_IN_PROGRESS
    todo.toggle_status()
    assert todo.status == Todo.STATUS_DONE
    todo.toggle_status()
    assert todo.status == Todo.STATUS_BACKLOG

def test_is_overdue():
    # Testfall 1: To-Do ist nicht abgeschlossen und hat ein Fälligkeitsdatum in der Vergangenheit
    todo1 = Todo(status=Todo.STATUS_TODO, due_date="2024-01-01")
    assert todo1.is_overdue() == True

    # Testfall 2: To-Do ist nicht abgeschlossen und hat ein Fälligkeitsdatum in der Zukunft
    todo2 = Todo(status=Todo.STATUS_TODO, due_date="2099-12-31")
    assert todo2.is_overdue() == False

    # Testfall 3: To-Do ist abgeschlossen (Status Done) und hat ein Fälligkeitsdatum in der Vergangenheit
    todo3 = Todo(status=Todo.STATUS_DONE, due_date="2024-01-01")
    assert todo3.is_overdue() == False

    # Testfall 4: To-Do ist abgeschlossen (Status Done) und hat ein Fälligkeitsdatum in der Zukunft
    todo4 = Todo(status=Todo.STATUS_DONE, due_date="2099-12-31")
    assert todo4.is_overdue() == False

def test_update_progress():
    todo = Todo(progress=0)
    assert todo.progress == 0

    todo.update_progress(50)
    assert todo.progress == 50

    todo.update_progress(100)
    assert todo.progress == 100

    todo.update_progress(150)   # ungültiger Wert → wird ignoriert
    assert todo.progress == 100  # bleibt bei 100