from datetime import date
from typing import Optional

from sqlmodel import select

from app.models.todo import Todo, Priority, Status
from app.services.BaseHandler import BaseHandler


# by Matthias
class TodoHandler(BaseHandler):

    # Festlegen des Modells, das von diesem Handler verwaltet wird
    model = Todo

    # Aktualisieren eines To-Dos anhand seiner ID und optionaler Felder
    def update(
        self,
        todo_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        link: Optional[str] = None,
        attachment_path: Optional[str] = None,
        attachment_name: Optional[str] = None,
        priority: Optional[str] = None,
        status: Optional[str] = None,
        progress: Optional[int] = None,
        start_date: Optional[date] = None,
        due_date: Optional[date] = None,
        labels: Optional[str] = None,
    ) -> Optional[Todo]:
        # Zuerst wird das bestehende To-Do aus der Datenbank geholt
        todo = self.session.get(Todo, todo_id)
        if todo is None:
            # Wenn kein To-Do gefunden wurde, gibt die Methode None zurueck
            return None

        # Nur Felder mit einem neuen Wert werden aktualisiert
        if title is not None:
            todo.title = title
        if description is not None:
            todo.description = description
        if link is not None:
            todo.link = link
        if attachment_path is not None:
            todo.attachment_path = attachment_path
        if attachment_name is not None:
            todo.attachment_name = attachment_name
        if priority is not None:
            try:
                # String-Werte werden in das Priority-Enum umgewandelt
                todo.priority = Priority(priority)
            except ValueError:
                raise ValueError(f"Ungültige Priorität: {priority}")
        if status is not None:
            try:
                # String-Werte werden in das Status-Enum umgewandelt
                todo.status = Status(status)
            except ValueError:
                raise ValueError(f"Ungültiger Status: {status}")
        if progress is not None:
            if not 0 <= progress <= 100:
                raise ValueError("Fortschritt muss zwischen 0 und 100 liegen")
            todo.progress = progress
        if start_date is not None:
            todo.start_date = start_date
        if due_date is not None:
            todo.due_date = due_date
        if labels is not None:
            todo.labels = labels

        # Speichern laeuft ueber die geerbte Methode aus BaseHandler
        self.save(todo)
        return todo

    # Abrufen aller To-Dos einer bestimmten To-Do-Liste anhand ihrer ID
    def get_todos_for_list(
        self,
        todo_list_id: int,
        status_filter: Optional[str] = None,
        priority_filter: Optional[str] = None,
    ) -> list[Todo]:
        # Erstellen einer Abfrage, um alle To-Dos mit der angegebenen todo_list_id zu erhalten
        statement = select(Todo).where(Todo.todo_list_id == todo_list_id)
        if status_filter is not None:
            # Hinzufügen eines Filters für den Status, wenn ein status_filter angegeben ist
            statement = statement.where(Todo.status == Status(status_filter))
        if priority_filter is not None:
            # Hinzufügen eines Filters für die Priorität, wenn ein priority_filter angegeben ist
            statement = statement.where(Todo.priority == Priority(priority_filter))
        return self.session.exec(statement).all()

    # Umschalten des Status eines To-Dos zwischen "offen" und "erledigt"
    def toggle_status(self, todo_id: int) -> Optional[Todo]:
        # To-Do suchen, bevor der Status veraendert wird
        todo = self.session.get(Todo, todo_id)
        if todo is None:
            return None

        todo.toggle_status()
        # Aenderung speichern und Objekt aktualisieren
        self.save(todo)
        return todo

    # Aktualisieren des Fortschritts eines To-Dos
    def update_progress(self, todo_id: int, progress: int) -> Optional[Todo]:
        # To-Do suchen, bevor der Fortschritt veraendert wird
        todo = self.session.get(Todo, todo_id)
        if todo is None:
            return None

        todo.update_progress(progress)
        # Aenderung speichern und Objekt aktualisieren
        self.save(todo)
        return todo
