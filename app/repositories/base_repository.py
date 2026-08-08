from sqlalchemy import select
from sqlalchemy.orm import Session


class BaseRepository[T]:
    def __init__(
        self,
        db: Session,
        model: type[T],
    ):
        self.db = db
        self.model = model

    def create(self, **data) -> T:
        obj = self.model(**data)

        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)

        return obj

    def get_by_id(
        self,
        obj_id: int,
    ) -> T | None:
        statement = select(self.model).where(self.model.id == obj_id)

        return self.db.scalar(statement)

    def get_all(self) -> list[T]:
        statement = select(self.model)

        return list(self.db.scalars(statement).all())

    def update(
        self,
        obj: T,
    ) -> T:
        self.db.commit()
        self.db.refresh(obj)

        return obj

    def delete(
        self,
        obj: T,
    ) -> None:
        self.db.delete(obj)
        self.db.commit()