"""
Author: Aaron Ho
Python Version: 3.7
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

from scripts.stat_finder import *
from scripts.visual import *


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
# Data

name_db = pd.read_csv('data/urls/name_url.tsv',
                      sep='\t', header=None, names=['name', 'link'])

init_ch = 'Khabib Nurmagomedov'
init_op = 'Conor McGregor'

init_ch_head = get_header_img(name_to_url(name_db, init_ch))
init_op_head = get_header_img(name_to_url(name_db, init_op))


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
            dbc.Button('Confirm', id='submit', size='lg', color='primary')]
                 )]
                    )


def content_layout():
    return html.Div(className='content-area', children=[
        dbc.Row(className="top-row", children=[
            dbc.Col(challenger_img(*init_ch_head), width=5,
                    id='head-ch', className='head-ch'),
            dbc.Col(opponent_img(*init_op_head), width=5, className='head-op')],
                justify='between'),

        dbc.Row(className="row-two", children=[
            dbc.Col(get_wins(), width=5, className='wins'),
            dbc.Col(get_wins(), width=5, className='wins')],
                justify='between'),


        dbc.Row(className="row-three", children=[
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

        dbc.Row(className="bot-row", children=[
            dbc.Col(id='path', width=12)]
        )
    ])


# EMPTY PLACEHOLDER
def empty_card():
    return dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("Text"),
                ], style={'textAlign': 'center'})
            ])
    )


def challenger_img(link, f_name, l_name):
    return [html.Img(className="ch-img", src=link),
            html.Div(className="ch-name", children=[
                html.H2(f_name), html.H2(l_name)])
            ]


def opponent_img(link, f_name, l_name):
    return [html.Div(className="op-name", children=[
                html.H2(f_name), html.H2(l_name)]),
            html.Img(className="op-img",
                     src=link)
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

def insert_fig(fig):
    return dcc.Graph(className='fig', figure=fig)


# App Layout
app.layout = html.Div(children=[
    side_bar(),
    content_layout()])


# CALLBACKS
@app.callback(
    Output('head-ch', 'children'),
    [Input("submit", "n_clicks")],
    [State("fighter-a", "value"),
     State("fighter-b", "value")]
)
def update_dash(n, a_value, b_value):
    if n is None:
        return "Please Enter Fighters"
    else:
        ch = get_header_img(name_to_url(name_db, a_value))
        return challenger_img(*ch)




# Run App
if __name__ == '__main__':
    app.run_server(debug=True)
