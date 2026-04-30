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

# Magic-Method Happy Path: __str__ gibt den Namen der TodoList zurück
def test_str_returns_todo_list_name():
    # Arrange
    todo_list = TodoList(name="Studium")

    # Act
    result = str(todo_list)

    # Assert
    assert result == "TodoList Name: Studium"

# Magic-Method Happy Path: __repr__ gibt eine detaillierte Darstellung der TodoList zurück
def test_repr_returns_detailed_representation():
    # Arrange
    todo_list = TodoList(id=1, name="Studium", owner_id=42)

    # Act
    result = repr(todo_list)

    # Assert
    assert result == "TodoList(id=1, name='Studium', owner_id=42)"

# Magic-Method Happy Path: __eq__ vergleicht zwei TodoList-Objekte basierend auf ihrer ID
def test_eq_returns_true_for_same_id():
    # Arrange
    todo_list1 = TodoList(id=1, name="Studium", owner_id=42)
    todo_list2 = TodoList(id=1, name="Freizeit", owner_id=99)

    # Act
    result = (todo_list1 == todo_list2)

    # Assert
    assert result is True

# Magic-Method Happy Path: __eq__ vergleicht zwei TodoList-Objekte mit unterschiedlichen IDs als ungleich und gleiche Attribute als gleich
def test_eq_returns_false_for_different_id():
    # Arrange
    todo_list1 = TodoList(id=1, name="Studium", owner_id=42)
    todo_list2 = TodoList(id=2, name="Studium", owner_id=42)

    # Act
    result = (todo_list1 == todo_list2)

    # Assert
    assert result is False

# Magic-Method Edge Case: __eq__ vergleicht ein TodoList-Objekt mit einem Objekt eines anderen Typs und gibt false zurück
def test_eq_returns_false_for_different_type():
    # Arrange
    todo_list = TodoList(id=1, name="Studium", owner_id=42)
    not_a_todo_list = "Ich bin kein TodoList-Objekt"

    # Act
    result = (todo_list == not_a_todo_list)

    # Assert
    assert result is False