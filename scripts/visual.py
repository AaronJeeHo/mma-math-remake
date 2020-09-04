"""
Author: Aaron Ho
Python Version: 3.7
"""

import plotly.express as px
import pandas as pd
from scripts.path_finder import mma_math
from scripts.stat_finder import scrape_stats


def plot_stats(stats):
    df = pd.DataFrame(list(stats.items()), columns=['Stat', 'Percentage'])
    fig = px.bar(
        data_frame=df,
        y='Stat',
        x='Percentage',
        orientation='h'
    )
    # fig.update_xaxes(autorange="reversed")
    # fig.show()


def main():
    stat_list = scrape_stats('Khabib Nurmagomedov')
    striking_stats = stat_list[0]
    plot_stats(striking_stats)


if __name__ == '__main__':
    main()
