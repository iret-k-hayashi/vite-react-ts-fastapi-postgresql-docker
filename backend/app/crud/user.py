from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    # 必要に応じて、以下のようにメソッドを加えたり、オーバーライドする。
    def get_by_email(self, db_session: Session, *, email: str) -> User | None:
        return db_session.query(User).filter(User.email == email).first()

    def create(self, db_session: Session, *, obj_in: UserCreate) -> User:
        try:
            db_obj = User(
                email=obj_in.email,
                name=obj_in.name,
                password=get_password_hash(obj_in.password),
            )
            db_session.add(db_obj)
            db_session.commit()
            db_session.refresh(db_obj)
            return db_obj
        except IntegrityError as sqlalchemy_error:
            db_session.rollback()
            raise sqlalchemy_error.orig

    def authenticate(
        self, db_session: Session, *, email: str, password: str
    ) -> User | None:
        user = self.get_by_email(db_session, email=email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user


user = CRUDUser(User)
