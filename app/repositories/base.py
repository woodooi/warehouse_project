from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type, Optional, List
from app.models.base import Base

# T - певний об'єкт, який каслідує Base
T = TypeVar('T', bound=Base)
class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self._model = model

    def get_by_id(self, id: int) -> Optional[T]:
        return self.db.query(self._model).filter(self._model.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        return self.db.query(self._model).offset(skip).limit(limit).all()

    # obj_in - json, перевірений на валідність значень полів через pydantic
    def create(self, obj_in) -> T:
        obj_data = obj_in.model_dump()
        db_obj = self._model(**obj_data) 
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def update(self, db_obj: T, obj_in) -> T:
        obj_data = obj_in.model_dump(exclude_unset=True)
        for field, value in obj_data.items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> bool:
        obj = self.get_by_id(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
