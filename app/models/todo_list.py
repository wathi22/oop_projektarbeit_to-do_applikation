from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .user import User
    from .todo import Todo
    from .team import Team


class TodoList(SQLModel, table=True):
    __tablename__ = "todolists"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: Optional[int] = Field(default=None, foreign_key="users.id")
    team_id: Optional[int] = Field(default=None, foreign_key="teams.id")

    owner: Optional["User"] = Relationship(back_populates="todo_lists")
    team: Optional["Team"] = Relationship(back_populates="todo_lists")
    todos: List["Todo"] = Relationship(back_populates="todo_list")

    def add_todo(self, todo: "Todo") -> None:
        self.todos.append(todo)

    def remove_todo(self, todo_id: int) -> None:
        self.todos = [todo for todo in self.todos if todo.id != todo_id]

    def get_all_todos(self) -> list["Todo"]:
        return self.todos

    def filter_todos(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None
    ) -> list["Todo"]:
        filtered = self.todos

        if status is not None:
            status_value = getattr(status, "value", status)
            filtered = [
                todo for todo in filtered
                if getattr(todo.status, "value", todo.status) == status_value
            ]

        if priority is not None:
            priority_value = getattr(priority, "value", priority)
            filtered = [
                todo for todo in filtered
                if getattr(todo.priority, "value", todo.priority) == priority_value
            ]

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
