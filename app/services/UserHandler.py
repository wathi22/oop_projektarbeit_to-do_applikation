from typing import Optional

from sqlmodel import select

from app.models.user import User
from app.services.BaseHandler import BaseHandler


# by Matthias
class UserHandler(BaseHandler):

    # Festlegen des Modells, das von diesem Handler verwaltet wird
    model = User

    # Aktualisieren eines Benutzers anhand seiner ID und optionaler Felder
    def update(
        self,
        user_id: int,
        firstname: Optional[str] = None,
        lastname: Optional[str] = None,
        email: Optional[str] = None,
    ) -> Optional[User]:
        # Zuerst wird der bestehende Benutzer aus der Datenbank geholt
        user = self.session.get(User, user_id)
        if user is None:
            # Wenn kein Benutzer gefunden wurde, gibt die Methode None zurueck
            return None

        # Nur Felder mit einem neuen Wert werden aktualisiert
        if firstname is not None:
            user.firstname = firstname
        if lastname is not None:
            user.lastname = lastname
        if email is not None:
            user.email = email

        # Speichern laeuft ueber die geerbte Methode aus BaseHandler
        self.save(user)
        return user

    # Abrufen eines Benutzers anhand seiner E-Mail-Adresse
    def get_by_email(self, email: str) -> Optional[User]:
        # SQLModel-Abfrage nach der eindeutigen E-Mail-Adresse
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()
