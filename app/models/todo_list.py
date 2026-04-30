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
    
# Magic-Method Happy Path __str__ gibt den Namen der TodoList zurück
    def __str__(self) -> str:
        return f"TodoList Name: {self.name}"
    
# Magic-Method Happy Path __repr__ gibt eine detaillierte Darstellung der TodoList zurück
    def __repr__(self) -> str:
        return (
            f"TodoList(id={self.id!r}, "
            f"name={self.name!r}, "
            f"owner_id={self.owner_id!r})"
        )
    
# Magic-Method Happy Path __eq__ vergleicht zwei TodoList-Objekte basierend auf ihrer ID
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TodoList):
            return NotImplemented
        return self.id == other.id