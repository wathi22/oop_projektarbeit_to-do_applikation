from sqlalchemy.orm import Session
from app.database.database import engine
from app.models.models import Todo 

class TodoListHandler:

    def save(self, todo: Todo):
        with Session(engine) as session:
            session.add(todo)
            session.commit()

    def delete(self, todo_id: int):
        with Session(engine) as session:
            todo = session.get(Todo, todo_id)
            if todo:
                session.delete(todo)
                session.commit()

    def get_all(self) -> list[Todo]:
        with Session(engine) as session:
            return session.query(Todo).all()
        
    def get_by_id(self, todo_id: int) -> Todo | None:
        with Session(engine) as session:
            return session.get(Todo, todo_id)
        
    def update(self, todo_id: int, description: str | None = None, priority: str | None = None, due_date: str | None = None):
        with Session(engine) as session:
            todo = session.get(Todo, todo_id)
            if not todo:
                return
            if description is not None:
                todo.description = description
            if priority is not None:
                todo.priority = priority
            if due_date is not None:
                todo.due_date = due_date
            session.commit()