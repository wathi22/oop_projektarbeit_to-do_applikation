from typing import Optional
from sqlmodel import Session, select
from app.models.user import User


class UserHandler:

    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.session.get(User, user_id)
        if not user:
            return False

        self.session.delete(user)
        self.session.commit()
        return True

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.get(User, user_id)

    def get_all(self) -> list[User]:
        return self.session.exec(select(User)).all()

    def update(
        self,
        user_id: int,
        firstname: Optional[str] = None,
        lastname: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Optional[User]:
        user = self.session.get(User, user_id)
        if not user:
            return None

        if firstname is not None:
            user.firstname = firstname
        if lastname is not None:
            user.lastname = lastname
        if email is not None:
            user.email = email

        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()