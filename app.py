"""
Author: Aaron Ho
Python Version: 3.7
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
# Data


# Example Graph
def ex_bar():
    data = px.data.gapminder()

    data_canada = data[data.country == 'Canada']
    fig = px.bar(data_canada, x='year', y='pop',
                 hover_data=['lifeExp', 'gdpPercap'], color='lifeExp',
                 labels={'pop': 'population of Canada'}, height=400)
    return fig


def ex_pie():
    df = px.data.tips()
    fig = px.pie(df, values='tip', names='day')

    return fig


# HELPERS
def side_bar():
    return html.Div(className='side-bar', children=[
        html.H1('MMA Math Calculator', className='side-header'),
        html.Hr(className='title-line'),
        html.Div(className='side-text', children=[
            html.P(['If fighter A beat Fighter B, and Fighter B beat Fighter C...',
                    html.Br(), 'Clearly Fighter A can beat Fighter C.',
                    html.Br()]
                   ),
            html.P('This is the law of MMA Math', className='bold-y')
        ]),
        html.Hr(className='side-line'),
        fighter_input()]
                    )


def fighter_input():
    return html.Div(className='fighter-input', children=[
        html.P('Input two fighters to prove if...',
               className='side-text'),
        html.Br(),

        dbc.Form(className='input-form', children=[
            dbc.FormGroup(className='input-a', children=[
                dbc.Label('Fighter A', html_for='fighter-a'),
                dbc.Input(id='fighter-a', type='text',
                          placeholder='Input Challenger Name')]
                          ),
            html.P('Beats', className='side-text'),

            dbc.FormGroup(className='input-b', children=[
                dbc.Label('Fighter B', html_for='fighter-b'),
                dbc.Input(id='fighter-b', type='text',
                          placeholder='Input Opponent Name')]
                          ),
            dbc.Button('Confirm', size='lg', color='primary')]
                 )]
                    )


def content_layout():
    return html.Div(className='content-area', children=[
        dbc.Row(className="top-row", children=[
            dbc.Col(challenger_img(), width=5, className='head-ch'),
            dbc.Col(opponent_img(), width=5, className='head-op')],
                justify='between'),

        dbc.Row(className="row-two", children=[
            dbc.Col(get_wins(), width=5, className='wins'),
            dbc.Col(get_wins(), width=5, className='wins')],
                justify='between'),


        dbc.Row(className="row-three", children=[
            # dbc.Col(ch_fig_two(ex_pie(), ex_bar()), width=5, className='row-three-col')]
            dbc.Col(className='row-three-col', width=5, children=[
                dbc.Row(className='row-three-col-row', children=[
                    dbc.Col(className='fig-col-three', width=6,
                            children=[insert_fig(ex_pie())]),
                    dbc.Col(className='fig-col-three', width=6,
                            children=[insert_fig(ex_bar())])],
                        no_gutters=True)]
                    ),

            dbc.Col(className='row-three-col', width=5, children=[
                dbc.Row(className='row-three-col-row', children=[
                    dbc.Col(className='fig-col-three', width=6,
                            children=[insert_fig(ex_bar())]),
                    dbc.Col(className='fig-col-three', width=6,
                            children=[insert_fig(ex_pie())])],
                        no_gutters=True)]
                    )], justify='between'),

        dbc.Row(className="row-four", children=[
            dbc.Col(insert_fig(ex_bar()), width=5, className='row-four-col'),
            dbc.Col(insert_fig(ex_bar()), width=5, className='row-four-col')],
                justify='between'
                ),

        # dbc.Row(className="h-20", children=[
        #     dbc.Col(empty_card(), width=12)
        # ]
        #
        # )
    ])


def empty_card():
    return dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("Text"),
                ], style={'textAlign': 'center'})
            ])
    )


# TOP Row Helpers
# def challenger_img():
#     return [html.Img(className="ch-img", src="https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2611557.png&w=350&h=254"),
#             html.Div(className="ch-flex", children=[
#                 html.Div(className="ch-name", children=[
#                     html.H2("Khabib"), html.H2("Nurmagomedov")]
#                          )])]


def challenger_img():
    return [html.Img(className="ch-img", src="https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2611557.png&w=350&h=254"),
            html.Div(className="ch-name", children=[
                html.H2("Khabib"), html.H2("Nurmagomedov")])
            ]


def opponent_img():
    return [html.Div(className="op-name", children=[
                html.H2("Khabib"), html.H2("Nurmagomedov")]),
            html.Img(className="op-img",
                     src="https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2611557.png&w=350&h=254")
            ]


# Row Two Helpers
def get_wins():
    return dbc.CardGroup(className='win-holder', children=[
        dbc.Card(className='win-card', children=[
            dbc.CardHeader("W-L-D", className='win-head'),
            dbc.CardBody("empty", className='win-body')
        ]),
        dbc.Card(className='win-card', children=[
            dbc.CardHeader("(T)KO", className='win-head'),
            dbc.CardBody("empty", className='win-body')
        ]),
        dbc.Card(className='win-card', children=[
            dbc.CardHeader("Sub", className='win-head'),
            dbc.CardBody("empty", className='win-body')
        ])
    ])




# Row Three Helpers


# def ch_fig_two(bar, pie):
#     return [dcc.Graph(className='two-fig', figure=bar),
#             dcc.Graph(className='two-fig', figure=pie)]


def insert_fig(fig):
    return dcc.Graph(className='fig', figure=fig)



# Row 3 graph





# App Layout
app.layout = html.Div(children=[
    side_bar(),
    content_layout()


])

# Run App
if __name__ == '__main__':
    app.run_server(debug=True)
