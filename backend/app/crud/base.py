from typing import Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db_session: Session, id: int) -> ModelType:
        db_obj = db_session.query(self.model).filter(self.model.id == id).first()
        return db_obj

    def get_multi(self, db_session: Session, *, skip=0, limit=100) -> list[ModelType]:
        return db_session.query(self.model).offset(skip).limit(limit).all()

    def create(self, db_session: Session, *, obj_in: CreateSchemaType) -> ModelType:
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            db_session.add(db_obj)
            db_session.commit()
            db_session.refresh(db_obj)
            return db_obj
        except IntegrityError as sqlalchemy_error:
            db_session.rollback()
            raise sqlalchemy_error.orig

    def update(
        self, db_session: Session, *, id: int, obj_in: UpdateSchemaType
    ) -> ModelType:
        db_obj = db_session.query(self.model).filter(self.model.id == id).first()
        if not db_obj:
            return None
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_session.add(db_obj)
        try:
            db_session.commit()
            db_session.refresh(db_obj)
            return db_obj
        except IntegrityError as sqlalchemy_error:
            db_session.rollback()
            raise sqlalchemy_error.orig

    def remove(self, db_session: Session, *, id: int) -> ModelType:
        obj = db_session.query(self.model).get(id)
        if obj:  # objがNoneでないときのみ削除する。
            db_session.delete(obj)
            db_session.commit()
            return obj
        else:
            return None
