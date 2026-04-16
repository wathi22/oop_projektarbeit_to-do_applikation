from datetime import datetime


class Todo:

    # Mögliche Status-Werte für ein To-Do-Item (Reihenfolge: Backlog → To-Do → In Progress → Done)
    STATUS_BACKLOG     = 'Backlog'
    STATUS_TODO        = 'To-Do'
    STATUS_IN_PROGRESS = 'In Progress'
    STATUS_DONE        = 'Done'

    # Mögliche Prioritäts-Werte (von niedrig bis kritisch)
    PRIORITY_LOW      = 'low'
    PRIORITY_MEDIUM   = 'medium'
    PRIORITY_HIGH     = 'high'
    PRIORITY_CRITICAL = 'critical'

    def __init__(
        self,
        id: int = None,
        title: str = "",
        description: str = "",
        priority: str = PRIORITY_LOW,
        status: str = STATUS_BACKLOG,
        progress: int = 0,
        start_date: str = "",
        due_date: str = "",
        labels: str = "",
        todo_list_id: int = None
    ):
        self.id = id                        # Von der DB vergeben (None bis gespeichert)
        self.title = title                  # Titel des To-Do-Items
        self.description = description      # Beschreibung / Details
        self.priority = priority            # Priorität: 'low' | 'medium' | 'high' | 'critical'
        self.status = status                # Aktueller Status (Standard: Backlog)
        self.progress = progress            # Fortschritt in Prozent (0–100)
        self.start_date = start_date        # Startdatum als String (Format: 'YYYY-MM-DD')
        self.due_date = due_date            # Fälligkeitsdatum als String (Format: 'YYYY-MM-DD')
        self.labels = labels                # Kommagetrennte Labels, z.B. 'Arbeit,Dringend'
        self.created_at = datetime.now()    # Erstellungszeitpunkt – automatisch beim Erstellen gesetzt
        self.todo_list_id = todo_list_id    # ID der übergeordneten TodoList (von DB vergeben)


    def toggle_status(self):
        # Setzt den Status einen Schritt weiter im Kreislauf:
        # Backlog → To-Do → In Progress → Done → Backlog
        if self.status == self.STATUS_BACKLOG:
            self.status = self.STATUS_TODO
        elif self.status == self.STATUS_TODO:
            self.status = self.STATUS_IN_PROGRESS
        elif self.status == self.STATUS_IN_PROGRESS:
            self.status = self.STATUS_DONE
        elif self.status == self.STATUS_DONE:
            self.status = self.STATUS_BACKLOG


    def is_overdue(self) -> bool:
        # Gibt True zurück wenn:
        # 1. Das To-Do noch nicht abgeschlossen ist (Status != Done)
        # 2. Ein Fälligkeitsdatum gesetzt ist
        # 3. Das Fälligkeitsdatum in der Vergangenheit liegt
        if not self.due_date:
            return False
        return self.status != self.STATUS_DONE and datetime.strptime(self.due_date, '%Y-%m-%d') < datetime.now()


    def update_progress(self, value: int):
        # Setzt den Fortschritt auf den angegebenen Wert (0–100)
        # Werte ausserhalb dieses Bereichs werden ignoriert
        if 0 <= value <= 100:
            self.progress = value
