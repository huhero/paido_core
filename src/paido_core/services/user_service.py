from sqlalchemy import select
from sqlalchemy.orm import Session

from paido_core.core.security import get_password_hash
from paido_core.models.user import User
from paido_core.schemas.user import UserList, UserSchema


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: UserSchema) -> User:
        db_user = User(
            username=user.username,
            email=user.email,
            password=get_password_hash(user.password),
        )
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def get_user_by_email_or_username(
        self, email: str | None = None, username: str | None = None
    ) -> User | None:
        return self.session.scalar(
            select(User).where(
                (User.email == email) | (User.username == username)
            )
        )

    def get_list_of_users(self, skip: int = 0, limit: int = 10) -> UserList:
        users = self.session.scalars(
            select(User).where(User.active).offset(skip).limit(limit)
        ).all()

        return {'users': users}

    def update_user(self, user: User) -> User:
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete_user(self, user: User) -> User:
        user.active = False
        self.session.commit()
        self.session.refresh(user)
        return user
