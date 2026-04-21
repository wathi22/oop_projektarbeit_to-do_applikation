from sqlmodel import Session, select
from app.database.database import engine
from app.models.user import User


def seed_users():
    users_to_seed = [
        {"firstname": "Wathanak", "lastname": "Deng", "email": "wathanak.deng@example.com"},
        {"firstname": "Matthias", "lastname": "Heiniger", "email": "matthias.heiniger@example.com"},
        {"firstname": "Joel", "lastname": "Fehr", "email": "joel.fehr@example.com"},
    ]

    with Session(engine) as session:
        for data in users_to_seed:
            exists = session.exec(select(User).where(User.email == data["email"])).first()
            if not exists:
                session.add(User(
                    firstname=data["firstname"],
                    lastname=data["lastname"],
                    email=data["email"],
                    password_hash=User.hash_password("password123"),
                ))

        session.commit()
        print("Users erstellt")


def run_seed():
    seed_users()