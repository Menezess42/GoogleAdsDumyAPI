import pytest
from pydantic import BaseModel, Field, ValidationError


class User(BaseModel):
    id: int
    name: str
    age: int = Field(gt=0)
    email: str | None = None

def test_valid_user():
    user = User(id=1, name="Alice", age=30, email="a@a.com")
    assert user.id == 1
    assert user.age == 30


def test_valid_without_optional():
    user = User(id=2, name="Bob", age=25)
    assert user.email is None

def test_invalid_type():
    with pytest.raises(ValidationError):
        User(id="abc", name="Alice", age=30)


def test_invalid_age():
    with pytest.raises(ValidationError):
        User(id=1, name="Alice", age=0)


def test_missing_field():
    with pytest.raises(ValidationError):
        User(id=1, age=20)

def test_multiple_errors():
    with pytest.raises(ValidationError):
        User(id="x", name=123, age=-5)

