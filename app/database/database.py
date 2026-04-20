from sqlmodel import SQLModel, create_engine
from app.models import *

engine = create_engine("sqlite:///database.db", echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)