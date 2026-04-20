from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User
    from .todo import Todo


class TodoList(SQLModel, table=True):
    __tablename__ = "todolists"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: Optional[int] = Field(default=None, foreign_key="users.id")

    owner: Optional["User"] = Relationship(back_populates="todo_lists")
    todos: List["Todo"] = Relationship(back_populates="todo_list")

    def get_all_todos(self) -> list["Todo"]:
        return self.todos

    def filter_todos(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None
    ) -> list["Todo"]:
        filtered = self.todos

        if status is not None:
            filtered = [todo for todo in filtered if todo.status == status]

        if priority is not None:
            filtered = [todo for todo in filtered if todo.priority == priority]

        return filtered