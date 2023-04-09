import pandas as pd
from ..types.datatype import City


def compute_traj_stat(city: City, traj_all: pd.DataFrame) -> pd.DataFrame:
    num_user = traj_all["userID"].unique().shape[0]
    num_poi = traj_all["poiID"].unique().shape[0]
    num_traj = traj_all["trajID"].unique().shape[0]
    df_stat = pd.DataFrame(
        {
            "#user": num_user,
            "#poi": num_poi,
            "#traj": num_traj,
            "#traj/user": num_traj / num_user,
        },
        index=[city.name],
    )
    return df_stat
