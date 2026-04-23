from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

if TYPE_CHECKING:
    from .todo_list import TodoList


# Status- und Prioritäts-Enums für bessere Lesbarkeit und Wartbarkeit
class Status(str, Enum):
    BACKLOG = "Backlog"
    TODO = "To-Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str = ""
    priority: Priority = Priority.LOW
    status: Status = Status.BACKLOG
    progress: int = 0
    start_date: Optional[date] = None
    due_date: Optional[date] = None
    labels: str = ""
    created_at: datetime = Field(default_factory=datetime.now)

    todo_list_id: Optional[int] = Field(default=None, foreign_key="todolists.id")
    todo_list: Optional["TodoList"] = Relationship(back_populates="todos")

    def toggle_status(self) -> None:
        if self.status == Status.BACKLOG:
            self.status = Status.TODO
        elif self.status == Status.TODO:
            self.status = Status.IN_PROGRESS
        elif self.status == Status.IN_PROGRESS:
            self.status = Status.DONE
        else:
            self.status = Status.BACKLOG

    def is_overdue(self) -> bool:
        if self.due_date is None:
            return False
        return self.status != Status.DONE and self.due_date < date.today()

    def update_progress(self, value: int) -> None:
        if 0 <= value <= 100:
            self.progress = value



    # Maigc-Method für bessere Debugging- und Logging-Ausgaben
    def __str__(self) -> str:
        return f"{self.title} [{self.status.value}]"
    
    def __repr__(self) -> str:
        return (
            f"Todo(id={self.id!r}, "
            f"title={self.title!r}, "
            f"description={self.description!r}, "
            f"priority={self.priority!r}, "
            f"status={self.status!r}, "
            f"progress={self.progress!r}, "
            f"start_date={self.start_date!r}, "
            f"due_date={self.due_date!r}, "
            f"labels={self.labels!r})"
        )
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Todo):
            return NotImplemented
        return self.id == other.id