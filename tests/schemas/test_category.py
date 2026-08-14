import pytest
from pydantic import ValidationError

from app.enums import CategoryType
from app.schemas.category import CategoryCreate, CategoryUpdate


def test_category_create_accepts_valid_data():
    category = CategoryCreate(
        name="Food",
        type=CategoryType.EXPENSE,
        icon="🍔",
        color="#FF5733",
    )

    assert category.name == "Food"
    assert category.type == CategoryType.EXPENSE
    assert category.icon == "🍔"
    assert category.color == "#FF5733"


@pytest.mark.parametrize(
    "field",
    ["name", "icon", "color"],
)
def test_category_create_rejects_empty_string(field):
    data = {
        "name": "Food",
        "type": CategoryType.EXPENSE,
        "icon": "🍔",
        "color": "#FF5733",
    }

    data[field] = ""

    with pytest.raises(ValidationError):
        CategoryCreate(**data)


def test_category_create_rejects_long_name():
    with pytest.raises(ValidationError):
        CategoryCreate(
            name="x" * 101,
            type=CategoryType.EXPENSE,
            icon="🍔",
            color="#FF5733",
        )


def test_category_create_rejects_long_icon():
    with pytest.raises(ValidationError):
        CategoryCreate(
            name="Food",
            type=CategoryType.EXPENSE,
            icon="x" * 51,
            color="#FF5733",
        )


def test_category_create_rejects_long_color():
    with pytest.raises(ValidationError):
        CategoryCreate(
            name="Food",
            type=CategoryType.EXPENSE,
            icon="🍔",
            color="x" * 21,
        )


def test_category_update_allows_partial_updates():
    category = CategoryUpdate(
        name="Dining",
    )

    assert category.name == "Dining"
    assert category.type is None
    assert category.icon is None
    assert category.color is None


@pytest.mark.parametrize(
    "field",
    ["name", "icon", "color"],
)
def test_category_update_rejects_empty_string(field):
    with pytest.raises(ValidationError):
        CategoryUpdate(**{field: ""})


def test_category_update_rejects_long_name():
    with pytest.raises(ValidationError):
        CategoryUpdate(
            name="x" * 101,
        )


def test_category_update_rejects_long_icon():
    with pytest.raises(ValidationError):
        CategoryUpdate(
            icon="x" * 51,
        )


def test_category_update_rejects_long_color():
    with pytest.raises(ValidationError):
        CategoryUpdate(
            color="x" * 21,
        )