from typing import List

from faker import Faker

from googleAdsDummy.models.campaign import Campaign


def generate_campaign(seed: int, num_campaigns: int) -> List[Campaign]:
    
    Faker.seed(seed)
    faker = Faker()

    campaigns = []

    for i in range(1, num_campaigns+1):
        id = str(faker.unique.uuid4())
        name = f"{faker.company()} - Campaign {i}"
        budget_amount = faker.pydecimal(
            left_digits=4, right_digits=2, min_value=20.00, max_value=5000.00
        )
        campaigns.append(Campaign(id=id, name=name, budget_amount=budget_amount))

    return campaigns
