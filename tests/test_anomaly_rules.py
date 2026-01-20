import pytest
from pydantic import ValidationError
from googleAdsDummy.types import Anomaly_rules


def test_accepts_list_and_tuple():
    a = Anomaly_rules.model_validate([True, 0.5, (0.5, 0.2)])
    assert a.enabled is True
    assert a.probability == 0.5
    assert a.efects.spike_conversions == 0.5


def test_probability_out_of_range():
    with pytest.raises(ValidationError):
        Anomaly_rules.model_validate([True, 1.5, (0.5, 0.2)])


def test_effect_out_of_range():
    with pytest.raises(ValidationError):
        Anomaly_rules.model_validate([True, 0.5, (1.5, 0.2)])
