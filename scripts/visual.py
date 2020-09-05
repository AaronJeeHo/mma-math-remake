"""
Author: Aaron Ho
Python Version: 3.7
"""

import plotly.express as px
import pandas as pd
from scripts.path_finder import mma_math
from scripts.stat_finder import scrape_stats


def plot_targets(stats):
    striking = stats[0]
    ground = stats[2]
    target_data = {'Striking Accuracy': ['Head', 'Head', 'Head',
                                         'Body', 'Body', 'Body',
                                         'Leg', 'Leg', 'Leg'],
                   'Type': ['Overall', 'Standing', 'Ground',
                            'Overall', 'Standing', 'Ground',
                            'Overall', 'Standing', 'Ground'],
                   'Percent': [striking['Breakdown Head'],
                               striking['Head Strike Accuracy'],
                               ground['Ground Head Strike Accuracy'],
                               striking['Breakdown Body'],
                               striking['Body Strike Accuracy'],
                               ground['Ground Body Strike Accuracy'],
                               striking['Breakdown Leg'],
                               striking['Leg Strike Accuracy'],
                               ground['Ground Leg Strike Accuracy']]
                   }

    df = pd.DataFrame(target_data, columns=['Striking Accuracy', 'Type', 'Percent'])
    fig = px.bar(data_frame=df,
                 title='Striking Accuracy',
                 y='Striking Accuracy',
                 x='Percent',
                 range_x=[0, 110],
                 color='Type',
                 barmode='group',
                 category_orders={'Striking Accuracy': ['Head', 'Body', 'Leg'],
                                  'Type': ['Ground', 'Standing', 'Overall']},
                 orientation='h',
                 labels={'Type': 'Striking Position'},
                 text='Percent',
                 template='plotly_dark',
                 color_discrete_map={'Overall': '#4ACFAC', 'Standing': '#F9AA33', 'Ground': '#BB86FC'}
                 )

    fig.update_traces(
        legendgroup="position",
        textposition="outside",
        texttemplate='%{x}'
    )

    fig['data'][0]['name'] = 'Ground Strikes'
    fig['data'][1]['name'] = 'Standing Strikes'
    fig['data'][2]['name'] = 'Overall Accuracy'

    fig.update_layout(
        title={
            'x': 0.5, 'y': 0.97,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 25}
        },

        legend={
            'title': '',
            'itemsizing': 'trace',
            'traceorder': 'reversed',
            'tracegroupgap': 50,
            'orientation': 'h',
            'x': 0, 'y': 1,
            'xanchor': 'left',
            'yanchor': 'bottom',
            'font': {'size': 20}
        }

    )

    fig.update_yaxes(
        showgrid=False,
        title='',
        ticksuffix=" Strikes",
        tickfont={'size': 20}
    )

    fig.update_xaxes(
        title='',
        ticksuffix="%",
        tickfont={'size': 15}
    )

    fig.show()


def main():
    stat_list = scrape_stats('Khabib Nurmagomedov')
    plot_targets(stat_list)


if __name__ == '__main__':
    main()
