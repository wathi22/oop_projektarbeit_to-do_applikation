#dummy-file_for_models

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass   

class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    description: Mapped[str]
    priority: Mapped[str] = mapped_column(default="normal")
    due_date: Mapped[str | None] = mapped_column(default=None)
    status: Mapped[str] = mapped_column(default="offen")
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    def toggle_status(self):
        self.status = "erledigt" if self.status == "offen" else "offen"

    def is_overdue(self) -> bool:
        if self.due_date is None:
            return False
        return datetime.strptime(self.due_date, "%Y-%m-%d") < datetime.now()
