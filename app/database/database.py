from sqlmodel import SQLModel, create_engine
from sqlalchemy import event
from sqlalchemy.engine import Engine
from app.models import User, TodoList, Todo

# Erstellung der SQLite-Datenbank und Aktivierung von Foreign Key Constraints
engine = create_engine("sqlite:///database.db", echo=False)

# Aktivieren von Foreign Key Constraints für SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Funktion zum Initialisieren der Datenbank und Erstellen der Tabellen
def init_db():
    SQLModel.metadata.create_all(engine)