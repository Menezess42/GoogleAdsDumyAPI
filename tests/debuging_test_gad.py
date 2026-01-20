from googleAdsDummy.gad import Gad


def valid_date():
    return ("2024-01-01", "2025-01-01")


def valid_anomaly():
    return [True, 0.5, (0.5, 0.2)]


def valid_profile():
    return [["A", "B", "C", "A"], ["A"], {"A": 0.1, "B": 0.3}]

def test_invalid_num_campaigns():
    g = Gad()
    g.config(
        seed=1,
        num_campaigns="3",
        weekend_factor=0.5,
        date_period=valid_date(),
        anomaly_rules=valid_anomaly(),
        profile_rules=valid_profile(),
    )

if __name__ == "__main__":
    test_invalid_num_campaigns()
