from .dataTableStategies import dataTableStrategy
from .searchQueryCompiler.astNodes_SearchQuery import FromNode, QueryNode
from .searchQueryCompiler.parser_SearchQuery import parse_query
from .SeedSystem import seedSystem


class Gad:
    def __init__(self):
        self.seed = 42
        self.num_campaigns = 3
        self.enable_anomalies: bool = True
        self.weekend_factor: float = 0.7
        self.dataTableStrategies = dataTableStrategy
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
            seed -- integer value used to configure a reproducible way of generating data;
            num_campaigns -- integer that determines how many campaigns this generator will produce;
            enable_anomalies -- boolean that determines whether anomalies may appear in the campaigns, such as during holiday periods;
            weekend_factor -- float in the range [0, 1] that determines the weight weekends have on the data.
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

    def gadAPI(self, searchQuery: str):
        searchQuery_node = parse_query(searchQuery)
        searchQuery_node_clean = searchQuery_node.model_dump(exclude_none=True)

        from_clause, *searchQuery_node_clean = searchQuery_node_clean.items()

        from_value = from_clause[1]['resource']

        campaign = self.dataTableStrategies[from_value.lower()]

        print(campaign)


