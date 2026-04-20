from typing import Optional
from datetime import date
from sqlmodel import Session, select
from app.models.todo import Todo


class TodoHandler:
    def __init__(self, session: Session):
        self.session = session

    def save(self, todo: Todo) -> Todo:
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def delete(self, todo_id: int) -> bool:
        todo = self.session.get(Todo, todo_id)
        if not todo:
            return False

        self.session.delete(todo)
        self.session.commit()
        return True

    def get_by_id(self, todo_id: int) -> Optional[Todo]:
        return self.session.get(Todo, todo_id)

    def get_all(self) -> list[Todo]:
        return self.session.exec(select(Todo)).all()

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

    def get_todos_for_list(self, todo_list_id: int) -> list[Todo]:
        statement = select(Todo).where(Todo.todo_list_id == todo_list_id)
        return self.session.exec(statement).all()

    def toggle_status(self, todo_id: int) -> Optional[Todo]:
        todo = self.session.get(Todo, todo_id)
        if not todo:
            return None

        todo.toggle_status()
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def update_progress(self, todo_id: int, progress: int) -> Optional[Todo]:
        todo = self.session.get(Todo, todo_id)
        if not todo:
            return None

        todo.update_progress(progress)
        self.session.commit()
        self.session.refresh(todo)
        return todo