from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType], ABC):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        """
        self.model = model

    @abstractmethod
    def get(self, db: Any, id: int) -> Optional[ModelType]:
        pass

    @abstractmethod
    def get_multi(self, db: Any, *, skip: int = 0, limit: int = 100) -> List[ModelType]:
        pass

    @abstractmethod
    def create(self, db: Any, *, obj_in: CreateSchemaType) -> ModelType:
        pass

    @abstractmethod
    def update(
        self,
        db: Any,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        pass

    @abstractmethod
    def remove(self, db: Any, *, id: int) -> ModelType:
        pass
