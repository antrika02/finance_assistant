from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):

    def __init__(
        self,
        db: Session,
        model: type[ModelType],
    ):
        self.db = db
        self.model = model

    def create(self, **data) -> ModelType:
        obj = self.model(**data)

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return obj

    def get_by_id(
        self,
        obj_id: int,
    ) -> ModelType | None:
        statement = select(self.model).where(
            self.model.id == obj_id
        )

        return self.db.scalar(statement)

    def get_all(self) -> list[ModelType]:
        statement = select(self.model)
        return list(self.db.scalars(statement).all())

    def update(
        self,
        obj: ModelType,
    ) -> ModelType:
        self.db.commit()
        self.db.refresh(obj)

        return obj

    def delete(
        self,
        obj: ModelType,
    ) -> None:
        self.db.delete(obj)
        self.db.commit()