from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .team import Team
    from .user import User


class Role(str, Enum):
    OWNER = "owner"
    MEMBER = "member"


class Membership(SQLModel, table=True):
    __tablename__ = "memberships"

    id: Optional[int] = Field(default=None, primary_key=True)
    team_id: Optional[int] = Field(default=None, foreign_key="teams.id")
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    role: Role = Role.MEMBER
    joined_at: datetime = Field(default_factory=datetime.now)

    team: Optional["Team"] = Relationship(back_populates="memberships")
    user: Optional["User"] = Relationship(back_populates="memberships")

    def __repr__(self) -> str:
        return f"Membership(id={self.id!r}, user_id={self.user_id!r}, team_id={self.team_id!r}, role={self.role!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Membership):
            return NotImplemented
        return (self.id == other.id and self.user_id == other.user_id and
                self.team_id == other.team_id and self.role == other.role)
