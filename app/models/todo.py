from datetime import datetime, date
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .todo_list import TodoList

STATUS_BACKLOG = "Backlog"
STATUS_TODO = "To-Do"
STATUS_IN_PROGRESS = "In Progress"
STATUS_DONE = "Done"

PRIORITY_LOW = "low"
PRIORITY_MEDIUM = "medium"
PRIORITY_HIGH = "high"
PRIORITY_CRITICAL = "critical"


class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str = ""
    priority: str = PRIORITY_LOW
    status: str = STATUS_BACKLOG
    progress: int = 0
    start_date: Optional[date] = None
    due_date: Optional[date] = None
    labels: str = ""
    created_at: datetime = Field(default_factory=datetime.now)

    todo_list_id: Optional[int] = Field(default=None, foreign_key="todolists.id")
    todo_list: Optional["TodoList"] = Relationship(back_populates="todos")

    def toggle_status(self) -> None:
        if self.status == STATUS_BACKLOG:
            self.status = STATUS_TODO
        elif self.status == STATUS_TODO:
            self.status = STATUS_IN_PROGRESS
        elif self.status == STATUS_IN_PROGRESS:
            self.status = STATUS_DONE
        else:
            self.status = STATUS_BACKLOG

    def is_overdue(self) -> bool:
        if self.due_date is None:
            return False
        return self.status != STATUS_DONE and self.due_date < date.today()

    def update_progress(self, value: int) -> None:
        if 0 <= value <= 100:
            self.progress = value