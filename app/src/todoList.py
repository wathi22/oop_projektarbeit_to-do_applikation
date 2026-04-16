from app.src.todo import Todo

class TodoList:

    def __init__ (
            self,
            id: int = None,
            name: str = '',
            owner_id: int = None
            ):
        
        self.id = id
        self.name = name
        self.owner_id = owner_id
        self.todos = []

    def add_todo(self, todo: Todo):
        # Fügt ein To-Do-Item zur Liste hinzu und setzt die todo_list_id des To-Dos auf die ID dieser Liste
        self.todos.append(todo)

    def remove_todo(self, todo_id: int):
        # Entfernt ein To-Do-Item anhand seiner ID aus der Liste
        for todo in self.todos:
            if todo.id == todo_id:
                self.todos.remove(todo)
                break

    def get_all_todos(self):
        # Gibt alle To-Do-Items in dieser Liste zurück
        return self.todos
    
    def filter_todos(self, status: str = None, priority: str = None) -> list[Todo]:
        # Filtert die To-Do-Items nach Status und/oder Priorität
        filtered = self.todos
        if status:
            filtered = [todo for todo in filtered if todo.status == status]
        if priority:
            filtered = [todo for todo in filtered if todo.priority == priority]
        return filtered
    