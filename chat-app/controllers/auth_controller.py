from db import SessionLocal
from models import User

class AuthController:

    @staticmethod
    def get_db():
        return SessionLocal()

    @staticmethod
    def register(full_name, email, password):
        db = AuthController.get_db()

        if db.query(User).filter(User.email == email).first():
            db.close()
            return None

        user = User(email=email, full_name=full_name)
        user.set_password(password)

        db.add(user)
        db.commit()
        db.refresh(user)
        db.close()
        return user

    @staticmethod
    def login(email, password):
        db = AuthController.get_db()
        user = db.query(User).filter(User.email == email).first()
        db.close()

        if user and user.verify_password(password):
            return user
        return None
