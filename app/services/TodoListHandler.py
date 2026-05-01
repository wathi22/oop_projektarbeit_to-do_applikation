from typing import Optional
from sqlmodel import Session, select
from app.models.todo_list import TodoList
from app.services.BaseHandler import BaseHandler


class TodoListHandler(BaseHandler):

    # Festlegen des Modells, das von diesem Handler verwaltet wird
    model = TodoList

    # Aktualisieren einer To-Do-Liste anhand ihrer ID und optionaler Felder
    def update(
        self,
        todo_list_id: int,
        name: Optional[str] = None,
        owner_id: Optional[int] = None,
    ) -> Optional[TodoList]:
        todo_list = self.session.get(TodoList, todo_list_id)
        if not todo_list:
            return None

        if name is not None:
            if not name.strip():
                raise ValueError("TodoList name cannot be empty")
            todo_list.name = name

        if owner_id is not None:
            todo_list.owner_id = owner_id

        self.session.commit()
        self.session.refresh(todo_list)
        return todo_list

    # Abrufen aller To-Do-Listen eines bestimmten Benutzers anhand seiner ID
    def get_lists_for_user(self, user_id: int) -> list[TodoList]:
        statement = select(TodoList).where(TodoList.owner_id == user_id)
        return self.session.exec(statement).all()

    # Erstellen einer neuen To-Do-Liste für einen bestimmten Benutzer
    def create_list(self, user_id: int, name: str) -> TodoList:
        if not name.strip():
            raise ValueError("TodoList name cannot be empty")
        new_todo_list = TodoList(name=name, owner_id=user_id)
        return self.save(new_todo_list)