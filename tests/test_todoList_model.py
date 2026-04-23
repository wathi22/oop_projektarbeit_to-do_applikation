from app.models.todo_list import TodoList
from app.models.todo import Todo, Status, Priority


# Happy Path: Alle Todos einer TodoList werden korrekt zurückgegeben
def test_get_all_todos_returns_all_todos():
    # Arrange
    todo1 = Todo(title="Task 1", status=Status.BACKLOG, priority=Priority.HIGH)
    todo2 = Todo(title="Task 2", status=Status.BACKLOG, priority=Priority.LOW)

    todo_list = TodoList(name="Studium")
    todo_list.todos = [todo1, todo2]

    # Act
    todos = todo_list.get_all_todos()

    # Assert
    assert len(todos) == 2
    assert todos[0].title == "Task 1"
    assert todos[1].title == "Task 2"


# Edge Case: Eine leere TodoList soll eine leere Liste zurückgeben
def test_get_all_todos_returns_empty_list_when_no_todos_exist():
    # Arrange
    todo_list = TodoList(name="Leere Liste")
    todo_list.todos = []

    # Act
    todos = todo_list.get_all_todos()

    # Assert
    assert todos == []


# Happy Path: Todos können nach Status gefiltert werden
def test_filter_todos_by_status_returns_matching_todos():
    # Arrange
    todo1 = Todo(title="Task 1", status=Status.BACKLOG, priority=Priority.HIGH)
    todo2 = Todo(title="Task 2", status=Status.TODO, priority=Priority.LOW)
    todo3 = Todo(title="Task 3", status=Status.BACKLOG, priority=Priority.LOW)

    todo_list = TodoList(name="Studium")
    todo_list.todos = [todo1, todo2, todo3]

    # Act
    backlog_todos = todo_list.filter_todos(status=Status.BACKLOG)

    # Assert
    assert len(backlog_todos) == 2
    assert all(todo.status == Status.BACKLOG for todo in backlog_todos)


# Edge Case: Filterung nach Status ohne Treffer soll leere Liste zurückgeben
def test_filter_todos_by_status_returns_empty_list_when_no_match_exists():
    # Arrange
    todo1 = Todo(title="Task 1", status=Status.BACKLOG, priority=Priority.HIGH)
    todo2 = Todo(title="Task 2", status=Status.BACKLOG, priority=Priority.LOW)

    todo_list = TodoList(name="Studium")
    todo_list.todos = [todo1, todo2]

    # Act
    result = todo_list.filter_todos(status=Status.TODO)

    # Assert
    assert result == []


# Happy Path: Todos können nach Priorität gefiltert werden
def test_filter_todos_by_priority_returns_matching_todos():
    # Arrange
    todo1 = Todo(title="Task 1", status=Status.BACKLOG, priority=Priority.HIGH)
    todo2 = Todo(title="Task 2", status=Status.BACKLOG, priority=Priority.LOW)
    todo3 = Todo(title="Task 3", status=Status.TODO, priority=Priority.HIGH)

    todo_list = TodoList(name="Studium")
    todo_list.todos = [todo1, todo2, todo3]

    # Act
    high_priority_todos = todo_list.filter_todos(priority=Priority.HIGH)

    # Assert
    assert len(high_priority_todos) == 2
    assert all(todo.priority == Priority.HIGH for todo in high_priority_todos)


# Happy Path: Todos können gleichzeitig nach Status und Priorität gefiltert werden
def test_filter_todos_by_status_and_priority_returns_matching_todos():
    # Arrange
    todo1 = Todo(title="Task 1", status=Status.BACKLOG, priority=Priority.HIGH)
    todo2 = Todo(title="Task 2", status=Status.BACKLOG, priority=Priority.LOW)
    todo3 = Todo(title="Task 3", status=Status.TODO, priority=Priority.HIGH)

    todo_list = TodoList(name="Studium")
    todo_list.todos = [todo1, todo2, todo3]

    # Act
    result = todo_list.filter_todos(status=Status.BACKLOG, priority=Priority.HIGH)

    # Assert
    assert len(result) == 1
    assert result[0].title == "Task 1"


# Edge Case: Ohne Filter sollen alle Todos zurückgegeben werden
def test_filter_todos_without_filters_returns_all_todos():
    # Arrange
    todo1 = Todo(title="Task 1", status=Status.BACKLOG, priority=Priority.HIGH)
    todo2 = Todo(title="Task 2", status=Status.TODO, priority=Priority.LOW)

    todo_list = TodoList(name="Studium")
    todo_list.todos = [todo1, todo2]

    # Act
    result = todo_list.filter_todos()

    # Assert
    assert len(result) == 2