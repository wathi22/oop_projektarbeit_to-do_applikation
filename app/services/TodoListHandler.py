from typing import Optional

from sqlmodel import select

from app.models.todo_list import TodoList
from app.services.BaseHandler import BaseHandler


# by Matthias
class TodoListHandler(BaseHandler):

    # Festlegen des Modells, das von diesem Handler verwaltet wird
    model = TodoList

    # Aktualisieren einer To-Do-Liste anhand ihrer ID und optionaler Felder
    def update(
        self,
        todo_list_id: int,
        name: Optional[str] = None,
        owner_id: Optional[int] = None,
    ) -> Optional[TodoList]:
        # Zuerst wird die bestehende To-Do-Liste aus der Datenbank geholt
        todo_list = self.session.get(TodoList, todo_list_id)
        if todo_list is None:
            # Wenn keine Liste gefunden wurde, gibt die Methode None zurueck
            return None

        # Nur Felder mit einem neuen Wert werden aktualisiert
        if name is not None:
            if not name.strip():
                raise ValueError("TodoList name cannot be empty")
            todo_list.name = name

        if owner_id is not None:
            todo_list.owner_id = owner_id

        # Speichern laeuft ueber die geerbte Methode aus BaseHandler
        self.save(todo_list)
        return todo_list

    # Abrufen aller To-Do-Listen eines bestimmten Benutzers anhand seiner ID
    def get_lists_for_user(self, user_id: int) -> list[TodoList]:
        # SQLModel-Abfrage nach dem Besitzer der Liste
        statement = select(TodoList).where(TodoList.owner_id == user_id)
        return self.session.exec(statement).all()

    # Erstellen einer neuen To-Do-Liste für einen bestimmten Benutzer
    def create_list(self, user_id: int, name: str) -> TodoList:
        # Leere Listennamen werden nicht erlaubt
        if not name.strip():
            raise ValueError("TodoList name cannot be empty")

        new_todo_list = TodoList(name=name, owner_id=user_id)
        # Neue Liste wird ueber BaseHandler gespeichert
        return self.save(new_todo_list)
