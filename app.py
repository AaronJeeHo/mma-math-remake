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
            dbc.Col(challenger_img(), width=5, className='row-col'),
            dbc.Col(opponent_img(), width=5, className='row-col')],
                justify='between'),
        #
        # dbc.Row(className="h-30", children=[
        #     dbc.Col(empty_card(), width=5),
        #     dbc.Col(empty_card(), width=2),
        #     dbc.Col(empty_card(), width=5)], justify='between'
        # ),
        #
        # dbc.Row(className="h-30", children=[
        #     dbc.Col(insert_graph(ex_bar()), width=5),
        #     dbc.Col(empty_card(), width=5)], justify='between'
        # ),
        #
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
    return [html.Img(className="op-img", src="https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2611557.png&w=350&h=254"),
            html.Div(className="op-name", children=[
                html.H2("Khabib"), html.H2("Nurmagomedov")])
            ]



# def img_card():
#     return dbc.Card(className='card-box', children=[
#         dbc.CardImg(src="https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2611557.png&w=350&h=254",
#                     top=True, className="fighter-img"),
#         dbc.CardBody(html.P('Khabib Nurmagomedov', className='card-name'))],
#                     outline=True)




def insert_graph(fig):
    return dcc.Graph(figure=fig)


def fighter_img():
    return html.Img(className="fighter-img", src="https://a.espncdn.com/combiner/i?img=/i/headshots/mma/players/full/2611557.png&w=350&h=254")



# App Layout
app.layout = html.Div(children=[
    side_bar(),
    content_layout()


])

# Run App
if __name__ == '__main__':
    app.run_server(debug=True)
