from typing import List

from faker import Faker

from googleAdsDummy.engine.seed import seedSystem
from googleAdsDummy.models.campaign import Campaign
from googleAdsDummy.models.profiles import ProfileType
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
