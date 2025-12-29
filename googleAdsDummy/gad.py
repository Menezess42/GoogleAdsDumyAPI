from _SeedSystem import seedSystem


class Gad:
    def __init__(self):
        self.seed = 42
        self.num_campaigns = 3
        self.enable_anomalies: bool = True
        self.weekend_factor: float = 0.7
        self._configSeedSystem()

    def clientConfig(
        self,
        seed: int,
        num_campaigns: int,
        enable_anomalies: bool,
        weekend_factor: float,
    ) -> None:
        """
        Client configuration used for campaign generation.

        Args:
            seed: Seed value used to ensure reproducible random behavior.
            num_campaigns: Number of campaigns to be generated.
            enable_anomalies: Whether anomalies should be injected into the data.
            weekend_factor: Adjustment factor applied to weekend behavior.
        """

        self.seed = seed
        self.num_campaigns = num_campaigns
        self.enable_anomalies = enable_anomalies
        self.weekend_factor = weekend_factor

        self._configSeedSystem()

    def _configSeedSystem(self) -> None:
        """
        Wraper for configuration the reproducibility of the gadAPI
        """
        self.randomValueGenerator = seedSystem(self.seed)

    def searchQuery(self, search_query: str) -> dict:
        return {}
        ...
        response = self._validateSearchQuery(search_query)

