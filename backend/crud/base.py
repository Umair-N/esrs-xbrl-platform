from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from database.base import CRUDBase
from psycopg2.extras import RealDictCursor

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class CRUDPostgreSQL(CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
