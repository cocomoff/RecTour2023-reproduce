from os.path import join
from typing import Dict, Tuple
import json


class City(object):
    """
    Target City (e.g., Osaka/Toronto in IJCAI'15/CIKM'16 datasets)
    """

    def __init__(
        self,
        name: str,
        config_fn: str = "./config/osak.json",
    ):
        self.name = name
        self.json = json.load(open(config_fn, "r"))
        self.dir = self.json.get("dir_data", "./data")
        self.dir_fig = self.json.get("dir_fig", "./output_figs")
        self.fn_poi = join(self.dir, self.json.get("fn_poi", f"poi-{self.name}.csv"))
        self.fn_traj = join(self.dir, self.json.get("fn_traj", f"traj-{self.name}.csv"))
        self.fn_cost = join(
            self.dir, self.json.get("fn_cost", f"costProfCat-{self.name}.csv")
        )
        self.fn_user_visit = join(
            self.dir, self.json.get("fn_user_vist", f"userVisits-{self.name}.csv")
        )
        self.fn_log = join(
            self.json.get("dir_log", "./output_logs"),
            self.json.get("fn_output", f"log-{self.name}.csv"),
        )

    def __str__(self) -> str:
        return f"City {self.name} (@{self.dir})"

    def get_fn_poi(self) -> str:
        return self.fn_poi

    def get_fn_traj(self) -> str:
        return self.fn_traj

    def get_fn_cost(self) -> str:
        return self.fn_cost

    def get_fn_user_visit(self) -> str:
        return self.fn_user_visit

    def get_fn_log(self) -> str:
        return self.fn_log


class PersToursInfo(object):
    """
    Computed Information in PersTour.

    - `average_poi_duration`: Def 3
    - `time_user_interest`: Def 4
    - `personalized_poi_visit_duration`: Def 5
    - `user_frequency_category`: Def 6
    """

    def __init__(
        self,
        average_poi_duration: Dict[int, float],
        time_user_interest: Dict[str, Dict[str, float]],
        personalized_poi_visit_duration: Dict[str, Dict[int, float]],
        user_frequency_category: Dict[str, Dict[str, float]],
        popularity: Dict[int, int],
        dict_cost: Dict[Tuple[int, int], float],
    ):
        # Def 3
        self.average_poi_duration = average_poi_duration

        # Def 4
        self.time_user_interest = time_user_interest

        # Def 5
        self.personalized_poi_visit_duration = personalized_poi_visit_duration

        # Def 6
        self.user_frequency_category = user_frequency_category

        # Popularity of POI
        self.popularity = popularity

        # Dict (i,j) -> cij
        self.dict_cost = dict_cost
