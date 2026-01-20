import pytest
from pydantic import ValidationError
from googleAdsDummy.types import Profile_rules


def test_accepts_list_and_normalizes_upper():
    p = Profile_rules.model_validate([["a", "b", "a"], ["a"], {"a": 0.1}])

    assert p.allow_profiles == {"A", "B"}
    assert p.ensure_at_least_one == {"A"}
    assert p.distribution == {"A": 0.1}


def test_ensure_not_subset():
    with pytest.raises(ValueError, match="ensure_at_least_one contains values"):
        Profile_rules.model_validate([["A", "B"], ["C"], {"A": 0.1}])


def test_distribution_not_subset():
    with pytest.raises(ValueError, match="distribution contains keys"):
        Profile_rules.model_validate([["A", "B"], ["A"], {"C": 0.1}])


def test_empty_ensure_list_becomes_none():
    p = Profile_rules.model_validate([["A", "B"], [], {"A": 0.1}])
    assert p.ensure_at_least_one is None
