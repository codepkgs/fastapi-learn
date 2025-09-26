from typing import Optional

from app.core.database import get_db_session
from app.models.user import User


class UserRepository:
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        with get_db_session() as db:
            return db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        with get_db_session() as db:
            return db.query(User).filter(User.username == username).first()

    def create_user(self, user: User) -> User:
        with get_db_session() as db:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
