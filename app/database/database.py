#dummy files database.py

from sqlalchemy import create_engine
from app.models.models import Base

engine = create_engine("sqlite:///todos.db")


def init_db():
    Base.metadata.create_all(engine)