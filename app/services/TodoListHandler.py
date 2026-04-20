from typing import Optional
from sqlmodel import Session, select
from app.models.todo_list import TodoList


class TodoListHandler:
    def __init__(self, session: Session):
        self.session = session

    def save(self, todo_list: TodoList) -> TodoList:
        self.session.add(todo_list)
        self.session.commit()
        self.session.refresh(todo_list)
        return todo_list

    def delete(self, todo_list_id: int) -> bool:
        todo_list = self.session.get(TodoList, todo_list_id)
        if not todo_list:
            return False

        self.session.delete(todo_list)
        self.session.commit()
        return True

    def get_by_id(self, todo_list_id: int) -> Optional[TodoList]:
        return self.session.get(TodoList, todo_list_id)

    def get_all(self) -> list[TodoList]:
        return self.session.exec(select(TodoList)).all()

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
            todo_list.name = name
        if owner_id is not None:
            todo_list.owner_id = owner_id

        self.session.commit()
        self.session.refresh(todo_list)
        return todo_list

    def get_lists_for_user(self, user_id: int) -> list[TodoList]:
        statement = select(TodoList).where(TodoList.owner_id == user_id)
        return self.session.exec(statement).all()

    def create_list(self, user_id: int, name: str) -> TodoList:
        new_todo_list = TodoList(name=name, owner_id=user_id)
        self.session.add(new_todo_list)
        self.session.commit()
        self.session.refresh(new_todo_list)
        return new_todo_list