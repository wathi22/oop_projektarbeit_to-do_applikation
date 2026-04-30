from typing import Optional
from datetime import date
from sqlmodel import Session, select
from app.models.todo import Todo, Priority, Status
from app.services.BaseHandler import BaseHandler

#by matthias
class TodoHandler(BaseHandler):

# Festlegen des Modells, das von diesem Handler verwaltet wird
    model = Todo

    # Aktualisieren eines To-Dos anhand seiner ID und optionaler Felder
    def update(
        self,
        todo_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        status: Optional[str] = None,
        progress: Optional[int] = None,
        start_date: Optional[date] = None,
        due_date: Optional[date] = None,
        labels: Optional[str] = None,
    ) -> Optional[Todo]:
        todo = self.session.get(Todo, todo_id)
        if not todo:
            return None
        
        if priority is not None:
            # Wenn String reingegeben wird, gegen Enum prüfen
            if priority not in Priority._value2member_map_ and priority not in Priority:
                raise ValueError(f"Ungültige Priorität: {priority}")
            todo.priority = priority
        
        if status is not None:
            if status not in Status._value2member_map_ and status not in Status:
                raise ValueError(f"Ungültiger Status: {status}")
            todo.status = status

        if title is not None:
            todo.title = title
        if description is not None:
            todo.description = description
        if priority is not None:
            todo.priority = priority
        if status is not None:
            todo.status = status
        if progress is not None:
            todo.progress = progress
        if start_date is not None:
            todo.start_date = start_date
        if due_date is not None:
            todo.due_date = due_date
        if labels is not None:
            todo.labels = labels

        self.session.commit()
        self.session.refresh(todo)
        return todo

    # Abrufen aller To-Dos einer bestimmten To-Do-Liste anhand ihrer ID
    def get_todos_for_list(self, todo_list_id: int) -> list[Todo]:
        statement = select(Todo).where(Todo.todo_list_id == todo_list_id)
        return self.session.exec(statement).all()

    # Umschalten des Status eines To-Dos zwischen "offen" und "erledigt"
    def toggle_status(self, todo_id: int) -> Optional[Todo]:
        todo = self.session.get(Todo, todo_id)
        if not todo:
            return None

        todo.toggle_status()
        self.session.commit()
        self.session.refresh(todo)
        return todo

    # Aktualisieren des Fortschritts eines To-Dos
    def update_progress(self, todo_id: int, progress: int) -> Optional[Todo]:
        todo = self.session.get(Todo, todo_id)
        if not todo:
            return None

        todo.update_progress(progress)
        self.session.commit()
        self.session.refresh(todo)
        return todo