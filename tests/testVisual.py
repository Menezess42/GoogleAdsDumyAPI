import os
import matplotlib.pyplot as plt
import pandas as pd
from googleAdsDummy.gad import Gad

os.makedirs("testeVisual", exist_ok=True)

QUERY = """SELECT campaign.name, metrics.impressions, metrics.clicks, metrics.cost, metrics.conversions FROM campaign WHERE metrics.date BETWEEN '2024-01-01' AND '2024-01-31'"""

simulations = [
    {
        "name": "sim1_seed42_weekend_low_profileA_heavy",
        "desc": "seed=42, weekend=0.2, perfil A pesado — alto volume, pouca queda no fim de semana",
        "config": dict(
            seed=42,
            num_campaigns=3,
            weekend_factor=0.2,
            date_period=("2024-01-01", "2025-05-01"),
            anomaly_rules=[False, 0.0, (0.0, 0.0)],
            profile_rules=[["A", "B", "C"], ["A"], {"A": 0.70}],
        ),
    },
    {
        "name": "sim2_seed7_weekend_high_profileC_heavy",
        "desc": "seed=7, weekend=0.8, perfil C pesado — baixo volume, queda suave no fim de semana",
        "config": dict(
            seed=7,
            num_campaigns=3,
            weekend_factor=0.8,
            date_period=("2024-01-01", "2025-05-01"),
            anomaly_rules=[False, 0.0, (0.0, 0.0)],
            profile_rules=[["B", "C"], ["C"], {"C": 0.70}],
        ),
    },
    {
        "name": "sim3_seed123_weekend_mid_balanced",
        "desc": "seed=123, weekend=0.5, perfis equilibrados — comportamento misto realista",
        "config": dict(
            seed=123,
            num_campaigns=3,
            weekend_factor=0.5,
            date_period=("2024-01-01", "2025-05-01"),
            anomaly_rules=[False, 0.0, (0.0, 0.0)],
            profile_rules=[["A", "B", "C"], ["A"], {"A": 0.33, "B": 0.33}],
        ),
    },
    {
        "name": "sim4_seed999_weekend_none_profileB_dominant",
        "desc": "seed=999, weekend=1.0 (sem queda), perfil B dominante — volume médio estável",
        "config": dict(
            seed=999,
            num_campaigns=3,
            weekend_factor=1.0,
            date_period=("2024-01-01", "2025-05-01"),
            anomaly_rules=[False, 0.0, (0.0, 0.0)],
            profile_rules=[["A", "B"], ["A"], {"B": 0.70}],
        ),
    },
]


def run_simulation(sim):
    gad = Gad()
    gad.config(**sim["config"])
    gad.create()

    r = gad.query(QUERY)
    df = pd.DataFrame(r["data"], columns=r["columns"])

    metrics = ["metrics.impressions", "metrics.clicks", "metrics.cost", "metrics.conversions"]
    titles = ["Impressions", "Clicks", "Cost", "Conversions"]

    fig, axes = plt.subplots(4, 1, figsize=(14, 14))
    fig.suptitle(f"{sim['name']}\n{sim['desc']}", fontsize=9)

    for campaign_name in df["campaign.name"].unique():
        subset = df[df["campaign.name"] == campaign_name].reset_index(drop=True)
        subset["day"] = pd.date_range(start="2024-01-01", periods=len(subset), freq="D")
        for ax, metric, title in zip(axes, metrics, titles):
            ax.plot(subset["day"], subset[metric], marker="o", markersize=2, label=campaign_name)

    for ax, title in zip(axes, titles):
        ax.set_title(title)
        ax.set_xlabel("Date")
        ax.legend(fontsize=6, loc="upper right")
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = f"testeVisual/{sim['name']}.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✓ {sim['name']}")


if __name__ == "__main__":
    for sim in simulations:
        run_simulation(sim)
    print(f"\n{len(simulations)} simulações salvas em testeVisual/")
