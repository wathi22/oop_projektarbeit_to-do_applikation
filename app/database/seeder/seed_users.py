from sqlmodel import Session, select
from app.database.database import engine
from app.models.user import User


def seed_users():
    with Session(engine) as session:

        # --- USER 1 ---
        user1_email = "wathanak.deng@example.com"
        existing_user1 = session.exec(
            select(User).where(User.email == user1_email)
        ).first()

        if not existing_user1:
            user1 = User(
                firstname="Wathanak",
                lastname="Deng",
                email=user1_email,
                password_hash=User.hash_password("password123"),
            )
            session.add(user1)
            print("User 1 erstellt")
        else:
            print("User 1 existiert bereits")

        # --- USER 2 ---
        user2_email = "matthias.heiniger@example.com"
        existing_user2 = session.exec(
            select(User).where(User.email == user2_email)
        ).first()

        if not existing_user2:
            user2 = User(
                firstname="Matthias",
                lastname="Heiniger",
                email=user2_email,
                password_hash=User.hash_password("password123"),
            )
            session.add(user2)
            print("User 2 erstellt")
        else:
            print("User 2 existiert bereits")

        # EIN commit am Ende (besser!)
        session.commit()


def run_seed():
    print("Starte Seeder...")
    seed_users()
    print("Seeder fertig")