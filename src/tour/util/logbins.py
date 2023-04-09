import numpy as np
import pandas as pd
from typing import List, Tuple


def extract_logbins(
    poi_info: pd.DataFrame, indices: List[int], nbins: int, target: str
) -> Tuple[pd.Series, np.ndarray]:
    assert target in poi_info.columns
    poi_pops = poi_info.loc[indices, target]
    expo_pop1 = np.log10(max(1, min(poi_pops)))
    expo_pop2 = np.log10(max(poi_pops))

    logbins_pop = np.logspace(np.floor(expo_pop1), np.ceil(expo_pop2), nbins + 1)
    logbins_pop[0] = 0  # deal with underflow
    if logbins_pop[-1] < poi_info[target].max():
        logbins_pop[-1] = poi_info[target].max() + 1

    return poi_pops, logbins_pop
