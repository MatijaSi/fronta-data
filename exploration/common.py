import pandas as pd
import matplotlib.pyplot as plt
from typing import List


def df_split_by_field(df: pd.DataFrame, field: str) -> List[pd.DataFrame]:
    distinct = df[field].unique()

    dfs = [df[df[field] == country] for country in distinct]

    return dfs


def plot_multiline(dfs: List[pd.DataFrame], x: str, y: str, label: str, title: str):
    fig, ax = plt.subplots()

    ax.set_title(title)

    for df in dfs:
        ax.plot(
            df[x],
            df[y],
            label=df[label].min(),
        )

    ax.legend()

    return fig
