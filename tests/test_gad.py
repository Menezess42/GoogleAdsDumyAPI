import pytest
from pydantic import ValidationError
from googleAdsDummy.gad import Gad


def valid_date():
    return ("2024-01-01", "2025-01-01")


def valid_anomaly():
    return [True, 0.5, (0.5, 0.2)]


def valid_profile():
    return [["A", "B", "C", "A"], ["A"], {"A": 0.1, "B": 0.3}]


def test_config_happy_path():
    g = Gad()
    g.config(
        seed=42,
        num_campaigns=3,
        weekend_factor=0.5,
        date_period=valid_date(),
        anomaly_rules=valid_anomaly(),
        profile_rules=valid_profile(),
    )

    assert g.seed == 42
    assert g.num_campaigns == 3
    assert g.weekend_factor == 0.5
    assert g.profile_rules.allow_profiles == {"A", "B", "C"}


def test_seed_none_defaults():
    g = Gad()
    g.config(
        seed=None,
        num_campaigns=3,
        weekend_factor=0.5,
        date_period=valid_date(),
        anomaly_rules=valid_anomaly(),
        profile_rules=valid_profile(),
    )

    assert g.seed == 42


@pytest.mark.parametrize("seed", [-1, "x", 1.5])
def test_invalid_seed(seed):
    g = Gad()
    with pytest.raises((ValueError, ValidationError)):
        g.config(
            seed=seed,
            num_campaigns=3,
            weekend_factor=0.5,
            date_period=valid_date(),
            anomaly_rules=valid_anomaly(),
            profile_rules=valid_profile(),
        )


@pytest.mark.parametrize("num", [0, -1, "3", 1.2])
def test_invalid_num_campaigns(num):
    g = Gad()
    with pytest.raises((ValueError, ValidationError)):
        g.config(
            seed=1,
            num_campaigns=num,
            weekend_factor=0.5,
            date_period=valid_date(),
            anomaly_rules=valid_anomaly(),
            profile_rules=valid_profile(),
        )


@pytest.mark.parametrize("wf", [-0.1, 1.1, "0.5"])
def test_invalid_weekend_factor(wf):
    g = Gad()
    with pytest.raises((ValueError, ValidationError)):
        g.config(
            seed=1,
            num_campaigns=3,
            weekend_factor=wf,
            date_period=valid_date(),
            anomaly_rules=valid_anomaly(),
            profile_rules=valid_profile(),
        )


def test_invalid_date_period_propagates():
    g = Gad()
    with pytest.raises(ValueError):
        g.config(
            seed=1,
            num_campaigns=3,
            weekend_factor=0.5,
            date_period=("2025-01-01", "2024-01-01"),
            anomaly_rules=valid_anomaly(),
            profile_rules=valid_profile(),
        )
