from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import SQLAlchemyError

from app.repositories.base_repository import BaseRepository


def test_commit_succeeds_without_rollback():
    db = MagicMock()
    repository = BaseRepository(db, object)

    repository._commit()

    db.commit.assert_called_once()
    db.rollback.assert_not_called()


def test_commit_rolls_back_when_database_error_occurs():
    db = MagicMock()
    repository = BaseRepository(db, object)

    error = SQLAlchemyError("database failure")
    db.commit.side_effect = error

    with pytest.raises(SQLAlchemyError, match="database failure"):
        repository._commit()

    db.rollback.assert_called_once()


def test_create_uses_commit():
    db = MagicMock()
    model = MagicMock()
    repository = BaseRepository(db, model)

    repository.create(name="Test")

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_update_uses_commit():
    db = MagicMock()
    model = MagicMock()
    repository = BaseRepository(db, model)

    obj = MagicMock()

    repository.update(obj)

    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(obj)


def test_delete_uses_commit():
    db = MagicMock()
    model = MagicMock()
    repository = BaseRepository(db, model)

    obj = MagicMock()

    repository.delete(obj)

    db.delete.assert_called_once_with(obj)
    db.commit.assert_called_once()