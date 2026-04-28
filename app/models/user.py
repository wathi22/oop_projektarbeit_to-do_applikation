from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
import bcrypt

if TYPE_CHECKING:
    from .todo_list import TodoList


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    firstname: str
    lastname: str
    email: str = Field(index=True, unique=True)
    password_hash: str

    todo_lists: List["TodoList"] = Relationship(back_populates="owner")

    @staticmethod
    def hash_password(plain_password: str) -> str:
        password_bytes = plain_password.encode("utf-8")
        hash_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hash_bytes.decode("utf-8")

    def check_password(self, plain_password: str) -> bool:
        password_bytes = plain_password.encode("utf-8")
        hash_bytes = self.password_hash.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hash_bytes)

    def full_name(self) -> str:
        return f"{self.firstname} {self.lastname}"
    
    # Magic-Method Happy Path __str__ gibt Vor- und Nachname zurück
    def __str__(self) -> str:
        return f"{self.firstname} {self.lastname}"
    
    # Magic-Method Happy Path __repr__ gibt alle wichtigen Felder zurück
    def __repr__(self):
        return (
            f"User(id={self.id!r}, "
            f"firstname={self.firstname!r}, "
            f"lastname={self.lastname!r}, "
            f"email={self.email!r})"
            f"password_hash={'***' if self.password_hash else None!r})"
        )
    
    # Magic-Method Happy Path __eq__ gleiche ID => gleich
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return self.id == other.id