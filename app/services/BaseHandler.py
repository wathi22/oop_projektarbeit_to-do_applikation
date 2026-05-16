from abc import ABC, abstractmethod
from typing import Optional

from sqlmodel import Session, SQLModel, select


# by Matthias
class BaseHandler(ABC):
    # Gemeinsame Basisfunktionen fuer alle Handler
    # Jede Unterklasse setzt hier ihr eigenes SQLModel ein
    model: type[SQLModel]

    def __init__(self, session: Session) -> None:
        # Die Session wird fuer alle Datenbankzugriffe wiederverwendet
        self.session = session

    # Speichert ein Objekt und macht die Aenderung in der Datenbank dauerhaft
    def save(self, obj: SQLModel) -> SQLModel:
        try:
            self.session.add(obj)
            self.session.commit()
            self.session.refresh(obj)
            return obj
        except Exception:
            # Bei Fehlern wird die offene Transaktion zurueckgesetzt
            self.session.rollback()
            raise

    # Loescht ein Objekt anhand seiner ID
    def delete(self, obj_id: int) -> bool:
        obj = self.session.get(self.model, obj_id)
        if obj is None:
            # False bedeutet: Es wurde kein passendes Objekt gefunden
            return False

        try:
            self.session.delete(obj)
            self.session.commit()
            return True
        except Exception:
            # Auch beim Loeschen bleibt die Datenbank so konsistent
            self.session.rollback()
            raise

    # Gibt ein einzelnes Objekt zurueck oder None, falls die ID nicht existiert
    def get_by_id(self, obj_id: int) -> Optional[SQLModel]:
        return self.session.get(self.model, obj_id)

    # Gibt alle Eintraege des jeweiligen Modells zurueck
    def get_all(self) -> list[SQLModel]:
        return self.session.exec(select(self.model)).all()

    # Muss im jeweiligen Handler passend zum Modell umgesetzt werden
    @abstractmethod
    def update(self, obj_id: int, **fields: object) -> Optional[SQLModel]:
        pass
