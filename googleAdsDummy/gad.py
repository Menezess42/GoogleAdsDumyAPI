from .engine.generators import dataTableStrategy
from .engine.seed import seedSystem


class Gad:
    def __init__(self):
        self.seed = 42
        self.num_campaigns = 3
        self.enable_anomalies: bool = True
        self.weekend_factor: float = 0.7
        self.dataTableStrategies = dataTableStrategy
        self._configSeedSystem()

    def config(self): ...
    def create(self): ...
    def query(self): ...

    def _configSeedSystem(self) -> None:
        """
        Wraper for configuration the reproducibility of the gadAPI
        """
        self.randomValueGenerator = seedSystem(self.seed)
