"""
Author: Aaron Ho
Python Version: 3.7
"""

import pandas as pd
import plotly.express as px

"""
Plot Target graphs
"""


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
        texttemplate='%{x}',
        hovertemplate=('<b>%{y}</b><br><br>'
                       'Fight Position: %{data.offsetgroup}<br><br>'
                       'Striking Accuracy: %{x}<extra></extra>')
    )

    fig['data'][0]['name'] = 'Ground Strikes'
    fig['data'][1]['name'] = 'Standing Strikes'
    fig['data'][2]['name'] = 'Overall Accuracy'
    fig.update_layout(
        autosize=True,
        margin={
            'pad': 0,
            'l': 0,
            'r': 0,
            'b': 0,
            't': 0,
        },

        legend={
            'title': '',
            'itemsizing': 'trace',
            'traceorder': 'reversed',
            'orientation': 'h',
            'x': 0.4, 'y': 1,
            'xanchor': 'center',
            'yanchor': 'bottom',
        },
        transition={
            'duration': 300,
            'easing': 'linear'
        }

    )

    fig.update_yaxes(
        showgrid=False,
        title={
            'text': '',
            'standoff': 0
        },
        ticksuffix=" Strikes",
        visible=False
    )

    fig.update_xaxes(
        title={
            'text': '',
            'standoff': 0
        },
        ticksuffix="%",
    )

    return fig


def plot_targets_reverse(stats):
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
                 y='Striking Accuracy',
                 x='Percent',
                 range_x=[110, 0],
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

        texttemplate='%{x}',
        hovertemplate=('<b>%{y}</b><br><br>'
                       'Fight Position: %{data.offsetgroup}<br><br>'
                       'Striking Accuracy: %{x}<extra></extra>')
    )

    fig['data'][0]['name'] = 'Ground Strikes'
    fig['data'][1]['name'] = 'Standing Strikes'
    fig['data'][2]['name'] = 'Overall Accuracy'

    fig.update_layout(
        autosize=True,
        margin={
            'pad': 0,
            'l': 0,
            'r': 0,
            'b': 0,
            't': 0,
        },

        legend={
            'title': '',
            'itemsizing': 'trace',
            'traceorder': 'normal',
            'orientation': 'h',
            'x': 0.6, 'y': 1,
            'xanchor': 'center',
            'yanchor': 'bottom',
        },
        transition={
            'duration': 300,
            'easing': 'linear'
        }

    )

    fig.update_yaxes(
        showgrid=False,
        title={
            'text': '',
            'standoff': 0
        },
        side="right",
        visible=False,
    )

    fig.update_xaxes(
        title={
            'text': '',
            'standoff': 0
        },
        ticksuffix="%",

    )

    return fig


"""
Plot Stat Total Graphs
"""


def plot_totals(stats):
    striking = stats[0]
    clinch = stats[1]

    total_data = {'Stats': ['Total Strike Accuracy',
                            'Significant Strike Accuracy',
                            'Takedown Accuracy'],

                  'Percent': [striking['Total Strike Accuracy'],
                              striking['Significant Strike Accuracy'],
                              clinch['Takedown Accuracy']
                              ]
                  }
    df = pd.DataFrame(total_data, columns=['Stats', 'Percent'])

    fig = px.bar(data_frame=df,
                 y='Stats',
                 x='Percent',
                 range_x=[0, 105],
                 text='Percent',
                 orientation='h',
                 template='plotly_dark',
                 color_discrete_sequence=['#e74c3c', '#e74c3c', '#e74c3c'],
                 )

    fig.update_traces(
        textposition="outside",
        texttemplate='%{x}',
        hovertemplate=('<b>%{label}</b><br><br>Percent: %{x}')
    )

    fig.update_layout(showlegend=False,
                      autosize=True,

                      margin={
                          'pad': 0,
                          'l': 0,
                          'r': 0,
                          'b': 0,
                          't': 0,
                      },
                      transition={
                          'duration': 300,
                          'easing': 'linear'
                      }

                      )

    fig.update_yaxes(
        showgrid=False,
        title={
            'text': '',
            'standoff': 0
        },
        visible=False
    )

    fig.update_xaxes(
        title={
            'text': '',
            'standoff': 0
        },
        ticksuffix="%",
    )

    return fig


def plot_totals_reverse(stats):
    striking = stats[0]
    clinch = stats[1]

    total_data = {'Stats': ['Total Strike Accuracy',
                            'Significant Strike Accuracy',
                            'Takedown Accuracy'],

                  'Percent': [striking['Total Strike Accuracy'],
                              striking['Significant Strike Accuracy'],
                              clinch['Takedown Accuracy']
                              ]
                  }
    df = pd.DataFrame(total_data, columns=['Stats', 'Percent'])

    fig = px.bar(data_frame=df,
                 y='Stats',
                 x='Percent',
                 range_x=[105, 0],
                 text='Percent',
                 orientation='h',
                 template='plotly_dark',
                 color_discrete_sequence=['#3498db', '#3498db', '#3498db']
                 )

    fig.update_traces(
        textposition="outside",
        texttemplate='%{x}',
        hovertemplate=('<b>%{label}</b><br><br>Percent: %{x}')
    )

    fig.update_layout(showlegend=False,
                      autosize=True,
                      hoverlabel={
                          'font': {
                              'color': '#ffffff'
                          }

                      },
                      margin={
                          'pad': 0,
                          'l': 0,
                          'r': 0,
                          'b': 0,
                          't': 0,
                      },
                      transition={
                          'duration': 300,
                          'easing': 'linear'
                      }

                      )

    fig.update_yaxes(
        showgrid=False,
        title={
            'text': '',
            'standoff': 0.5
        },
        side="right",
        visible=False
    )

    fig.update_xaxes(
        title={
            'text': '',
            'standoff': 0
        },
        ticksuffix="%",
    )

    return fig


"""
Plot Ratio Graphs
"""


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
                 template='plotly_dark',
                 color='Method',
                 color_discrete_map={'Decisions': '#4ACFAC',
                                     "(T)KO's": '#F9AA33',
                                     'Submissions': '#BB86FC'}
                 )

    fig.update_traces(textposition='inside',
                      textinfo='label+percent',
                      textfont={'size': 40},
                      hovertemplate=('<b>%{label}</b><br> Percent: %{percent}'
                                     '<br> Count: %{value}')
                      )
    fig.update_layout(showlegend=False,
                      autosize=True,
                      margin={
                          'pad': 0,
                          'l': 0,
                          'r': 0,
                          'b': 0,
                          't': 0,
                      },
                      transition={
                          'duration': 300,
                          'easing': 'linear'
                      }

                      )

    return fig


def main():
    pass


if __name__ == '__main__':
    main()
