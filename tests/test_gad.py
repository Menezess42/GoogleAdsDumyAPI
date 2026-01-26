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


def test_ensure_creation():
    gad = Gad()
    gad.config(
        seed=42,
        num_campaigns=3,
        weekend_factor=0.5,
        date_period=("2024-01-01", "2025-05-01"),
        anomaly_rules=[True, 0.5, (0.5, 0.2)],
        profile_rules=[["A", "B", "C"], ["A"], {"A": 0.25, "B": 0.50}],
    )
    gad.create()
    campaign_list = gad.world.list_campaigns()
    assert campaign_list[0].id == 'bdd640fb-0667-4ad1-9c80-317fa3b1799d'
    assert campaign_list[0].name == 'Sanchez-Taylor - Campaign 1'
    assert campaign_list[0].budget_amount == 859.81

    assert campaign_list[1].id == '07a0ca6e-0822-48f3-ac03-1199972a8469'
    assert campaign_list[1].name == 'Robinson PLC - Campaign 2'
    assert campaign_list[1].budget_amount == 4951.08

    assert campaign_list[2].id == 'b38a088c-a65e-4389-b74d-0fb132e70629'
    assert campaign_list[2].name == 'Barnes, Cole and Ramirez - Campaign 3'
    assert campaign_list[2].budget_amount == 73.26
