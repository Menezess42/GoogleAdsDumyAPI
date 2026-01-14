from SeedSystem import seedSystem


class Gad:
    def __init__(self):
        self.seed = 42
        self.num_campaigns = 3
        self.enable_anomalies: bool = True
        self.weekend_factor: float = 0.7
        self._configSeedSystem()

    def clientConfig(self) -> None:
        """
        Client configuration used for campaign generation.

        Args:
            ...
        """
        ...

    def _configSeedSystem(self) -> None:
        """
        Wraper for configuration the reproducibility of the gadAPI
        """
        self.randomValueGenerator = seedSystem(self.seed)
