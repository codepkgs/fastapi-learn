from app.models.user import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_user_by_id(self, user_id: int):
        return self.user_repository.get_user_by_id(user_id)

    def get_user_by_username(self, username: str):
        return self.user_repository.get_user_by_username(username)

    def create_user(self, user: User):
        return self.user_repository.create_user(user)
