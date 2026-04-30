from typing import Optional
from abc import ABC, abstractmethod
from sqlmodel import Session, SQLModel, select

class BaseHandler(ABC):
    model: type[SQLModel]

    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, obj: SQLModel) -> SQLModel:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj
    
    def delete(self, obj_id: int) -> bool:
        obj = self.session.get(self.model, obj_id)
        if not obj:
            return False
        
        self.session.delete(obj)
        self.session.commit() 
        return True

    def get_by_id(self, obj_id: int) -> Optional[SQLModel]:
        return self.session.get(self.model, obj_id)
    
    def get_all(self) -> list[SQLModel]:
        return self.session.exec(select(self.model)).all()
    
    @abstractmethod
    def update(self, obj_id: int, **fields) -> Optional[SQLModel]:
        pass
