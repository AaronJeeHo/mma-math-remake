"""
Author: Aaron Ho
Python Version: 3.7
"""

import plotly.express as px
import pandas as pd
from scripts.stat_finder import scrape_stats, scrape_ratio


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


def plot_totals(stats):
    striking = stats[0]
    clinch = stats[1]

    total_data = {'Stats': ['Takedown Accuracy',
                            'Significant Strike Accuracy',
                            'Total Strike Accuracy'],
                  'Percent': [clinch['Takedown Accuracy'],
                              striking['Significant Strike Accuracy'],
                              striking['Total Strike Accuracy']]
                  }
    df = pd.DataFrame(total_data, columns=['Stats', 'Percent'])

    fig = px.bar(data_frame=df,
                 x='Stats',
                 y='Percent',
                 title='Overall Stats',
                 range_y=[0, 105],
                 text='Percent',
                 orientation='v',
                 template='plotly_dark',
                 color_discrete_sequence=['#4ACFAC', '#4ACFAC', '#4ACFAC']
                 )

    fig.update_traces(
        textposition="outside",
        texttemplate='%{y}',
        textfont={'size': 15}
    )

    fig.update_layout(
        title={
            'x': 0.5, 'y': 0.97,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 25}
        }

    )

    fig.update_xaxes(
        showgrid=False,
        title='',
        tickfont={'size': 15}
    )

    fig.update_yaxes(
        title='',
        ticksuffix="%",
        tickfont={'size': 15}
    )

    fig.show()


def plot_ratios(stats):
    wins = stats['WLD'][0]
    ko = stats['KO'][0]
    sub = stats['SUB'][0]
    dec = wins - ko - sub

    ratio_data = {'Method': ['Decisions', "(T)KO's", 'Submissions'],
                  'Count': [dec, ko, sub]}

    df = pd.DataFrame(ratio_data, columns=['Method', 'Count'])
    fig = px.pie(data_frame=df,
                 values='Count',
                 names='Method',
                 title='Win Breakdown',
                 template='plotly_dark',
                 color='Method',
                 color_discrete_map={'Decisions': '#4ACFAC',
                                     "(T)KO's": '#F9AA33',
                                     'Submissions': '#BB86FC'}
                 )

    fig.update_layout(showlegend=False,

                      title={
                          'x': 0.5, 'y': 0.97,
                          'xanchor': 'center',
                          'yanchor': 'top',
                          'font': {'size': 25}}
                      )

    fig.update_traces(textposition='inside',
                      textinfo='label+value',
                      textfont={'size': 40},
                      hovertemplate='<b>%{label}</b><br> %{percent}'
                      )

    fig.show()


def main():
    # tat_list = scrape_stats('Khabib Nurmagomedov')
    # ratio = scrape_ratio('Khabib Nurmagomedov')
    # plot_targets(stat_list)
    # plot_totals(stat_list)
    # plot_ratios(ratio)
    pass


if __name__ == '__main__':
    main()
