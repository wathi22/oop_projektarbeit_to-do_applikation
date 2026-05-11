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
    
    def __lt__(self, other: "Todo") -> bool:
        # 1. Type-Check: ist 'other' überhaupt ein Todo?
        if not isinstance(other, Todo):
            return NotImplemented
        # 2. Falls beide kein due_date haben → sind "gleich" → False
        if self.due_date is None and other.due_date is None:
            return False
        # 3. Falls self kein due_date hat, other aber schon → self ist "größer" → False
        if self.due_date is None and other.due_date is not None:
            return False
        # 4. Falls self ein due_date hat, other nicht → self ist "kleiner" → True
        if self.due_date is not None and other.due_date is None:
            return True
        # 5. Beide haben due_dates → vergleiche die Daten
        return self.due_date < other.due_date
    
    @classmethod
    def from_dict(cls, data: dict) -> "Todo":
        priority_value = data.get("priority", Priority.LOW)
        if isinstance(priority_value, str):
            priority_value = Priority(priority_value)

        status_value = data.get("status", Status.BACKLOG)
        if isinstance(status_value, str):
            status_value = Status(status_value)

        start_date_value = data.get("start_date")
        if isinstance(start_date_value, str):
            start_date_value = date.fromisoformat(start_date_value)

        due_date_value = data.get("due_date")
        if isinstance(due_date_value, str):
            due_date_value = date.fromisoformat(due_date_value)

        return cls(
            # Pflichtfeld "Title" muss immer vorhanden sein, sonst werfen wir eine Exception
            title=data["title"],
            # Optionale Felder mit .get() und Default-Werten
            description=data.get("description", ""),
            # Priority-Enum aus String erstellen, Default ist LOW
            priority=priority_value,
            # Status-Enum aus String erstellen, Default ist BACKLOG
            status=status_value,
            progress=data.get("progress", 0),
            start_date=start_date_value,
            due_date=due_date_value,
            labels=data.get("labels", ""),
        )