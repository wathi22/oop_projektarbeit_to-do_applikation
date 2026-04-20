from typing import Optional
from sqlmodel import Session, select
from app.models.user import User


class UserHandler:
    
    def __init__(self, session: Session):
        self.session = session

    # CRUD-Methoden für User
    def save(self, user: User) -> User: 
        self.session.add(user)          # Hinzufügen des User-Objekts zur Session
        self.session.commit()           # Speichern der Änderungen in der Datenbank
        self.session.refresh(user)      # Aktualisieren des User-Objekts mit den Daten aus der Datenbank (z.B. ID)
        return user                     # Rückgabe des gespeicherten User-Objekts mit aktualisierten Informationen (z.B. ID)
    
    # Löschen eines Benutzers anhand seiner ID
    def delete(self, user_id: int) -> bool:
        user = self.session.get(User, user_id)
        if not user:
            return False

        self.session.delete(user)
        self.session.commit()
        return True

    # Abrufen eines Benutzers anhand seiner ID
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.session.get(User, user_id)

    # Abrufen aller Benutzer aus der Datenbank
    def get_all(self) -> list[User]:
        return self.session.exec(select(User)).all()

    # Aktualisieren eines Benutzers anhand seiner ID und optionaler Felder
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

    # Abrufen eines Benutzers anhand seiner E-Mail-Adresse
    def get_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()