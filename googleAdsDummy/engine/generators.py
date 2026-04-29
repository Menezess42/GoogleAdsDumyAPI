import hashlib
import random
from datetime import date as date_type
from typing import List

from faker import Faker

from googleAdsDummy.engine.seed import seedSystem
from googleAdsDummy.models.campaign import Campaign
from googleAdsDummy.models.campaignMetrics import CampaignMetrics
from googleAdsDummy.models.profiles import PROFILE_BEHAVIOR, ProfileType
from googleAdsDummy.types import Profile_rules


def generate_campaign(seed: int, num_campaigns: int) -> List[Campaign]:

    Faker.seed(seed)
    faker = Faker()

    campaigns = []

    for i in range(1, num_campaigns + 1):
        id = str(faker.unique.uuid4())
        name = f"{faker.company()} - Campaign {i}"
        budget_amount = faker.pydecimal(
            left_digits=4, right_digits=2, min_value=20.00, max_value=5000.00
        )
        campaigns.append(Campaign(id=id, name=name, budget_amount=budget_amount))

    return campaigns


def generate_campaign_profiles(
    seed: int, campaign_ids: list[str], profile_rules: Profile_rules
) -> dict[str, ProfileType]:
    profiles_list, ensure_profiles, profiles_distribution = profile_rules
    seedGen = seedSystem(seed)

    campaign_profile: dict[str, ProfileType] = {}

    profiles_distribution = profiles_distribution or {}
    profiles_without_dist = profiles_list - profiles_distribution.keys()

    if profiles_without_dist:
        remaining_space = 1.0 - sum(profiles_distribution.values())
        equal_share = remaining_space / len(profiles_without_dist)
        for p in profiles_without_dist:
            profiles_distribution[p] = equal_share

    if ensure_profiles:
        for prof in sorted(ensure_profiles):
            r = seedGen()
            idx = int(r * len(campaign_ids))
            selected_id = campaign_ids.pop(idx)
            campaign_profile.update({selected_id: prof})

    if campaign_ids:
        ordered_profiles = sorted(profiles_distribution.keys())

        cumulative = []
        acc = 0.0
        for p in ordered_profiles:
            acc += profiles_distribution[p]
            cumulative.append((acc, p))

        for cid in campaign_ids:
            r = seedGen()
            for limit, prof in cumulative:
                if r <= limit:
                    campaign_profile.update({cid: prof})
                    break

    return campaign_profile


def generate_metrics(world, campaign_id: str, date_str: str) -> CampaignMetrics:
    raw = f"{world.seed}:{campaign_id}:{date_str}".encode()
    day_seed = int(hashlib.md5(raw).hexdigest(), 16)
    rng = random.Random(day_seed)

    profile = world.get_profile(campaign_id)
    behavior = PROFILE_BEHAVIOR[profile]

    d = date_type.fromisoformat(date_str)
    start = world.date_period.start_date
    end = world.date_period.end_date
    total_days = (end - start).days or 1
    progress = (d - start).days / total_days

    trend_multiplier = {
        "A": 1.0 + 0.3 * progress,
        "B": 1.0,
        "C": 1.0 - 0.2 * progress,
    }[profile]

    day_factor = world.weekend_factor if d.weekday() >= 5 else 1.0

    campaign = world.get_campaign(campaign_id)
    budget_scale = campaign.budget_amount * 2.5
    base_impressions = (
        budget_scale * behavior["volume_factor"] * trend_multiplier * day_factor
    )
    noise = rng.gauss(0, 0.1)
    impressions = max(0, int(base_impressions * (1 + noise)))

    ctr = max(0.0, rng.gauss(behavior["ctr_mean"], behavior["ctr_std"]))
    clicks = min(impressions, int(impressions * ctr))

    conv_rate = max(
        0.0, rng.gauss(behavior["conv_rate_mean"], behavior["conv_rate_std"])
    )
    conversions = min(clicks, int(clicks * conv_rate))

    cost_per_click = rng.uniform(0.5, 2.0) * (campaign.budget_amount / 1000)
    cost = round(clicks * cost_per_click, 2)

    cpa = round(cost / conversions, 2) if conversions > 0 else 0.0

    return CampaignMetrics(
        campaign_id=campaign_id,
        date=d,
        impressions=impressions,
        clicks=clicks,
        cost=cost,
        conversions=conversions,
        cpa=cpa,
    )
