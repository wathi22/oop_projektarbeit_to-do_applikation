from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .team_membership import Membership
    from .todo_list import TodoList


class Team(SQLModel, table=True):
    __tablename__ = "teams"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str = ""
    created_at: datetime = Field(default_factory=datetime.now)
    created_by_id: Optional[int] = Field(default=None, foreign_key="users.id")

    memberships: List["Membership"] = Relationship(back_populates="team")
    todo_lists: List["TodoList"] = Relationship(back_populates="team")

    def get_member_ids(self) -> List[int]:
        return [membership.user_id for membership in self.memberships]

    def __str__(self) -> str:
        return f"Team: {self.name} (ID: {self.id})"

    def __repr__(self) -> str:
        return f"Team(id={self.id!r}, name={self.name!r}, description={self.description!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Team):
            return NotImplemented
        return self.id == other.id
