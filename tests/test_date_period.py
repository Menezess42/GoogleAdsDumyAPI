import pytest
from pydantic import ValidationError
from googleAdsDummy.types import Date_period


def test_accepts_tuple():
    d = Date_period.model_validate(("2024-01-01", "2025-01-01"))
    assert d.start_date < d.end_date


def test_invalid_order():
    with pytest.raises(ValueError, match="start_date should be less than end_date"):
        Date_period.model_validate(("2025-01-01", "2024-01-01"))
