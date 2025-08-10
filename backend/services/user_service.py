from typing import List, Optional

from crud.user import user_crud
from models.user import User
from schemas.user import UserCreate, UserUpdate


class UserService:
    def create_user(self, user_data: UserCreate, db) -> Optional[User]:
        return user_crud.create_user(user_data, db)

    def get_user_by_email(self, email: str, db) -> Optional[User]:
        return user_crud.get_user_by_email(email, db)

    def get_user_by_id(self, user_id: int, db) -> Optional[User]:
        return user_crud.get_user_by_id(user_id, db)

    def get_all_users(
        self,
        db,
        skip: int = 0,
        limit: int = 10,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        search: Optional[str] = None
    ) -> List[User]:
        return user_crud.get_all_users(
            db=db,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
            search=search
        )

    def count_users(self, db, search: Optional[str] = None) -> int:
        return user_crud.count_users(db, search)

    def update_user(self, user_id: int, user_data: UserUpdate, db) -> Optional[User]:
        return user_crud.update_user(user_id, user_data, db)


user_service = UserService()
