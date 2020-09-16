"""
Author: Aaron Ho
Python Version: 3.7
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from pathlib import Path
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd

from scripts.stat_finder import *
from scripts.visual import *
from scripts.path_finder import mma_math

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.14.0/css/all.css"

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.DARKLY, FONT_AWESOME],
                suppress_callback_exceptions=True)
# Data

path = Path(__file__).parent
name_db = pd.read_csv((path / "data/urls/name_url.tsv"),
                      sep='\t', header=None, names=['name', 'link'])

"""-----------------------------------------------
Helpers for Updating stats and visuals


-----------------------------------------------"""


def fighter_data(db, f_name):
    link = name_to_url(db, f_name)
    header = get_header_img(link)
    records = scrape_ratio(link)
    stats = scrape_stats(link)

    return header, records, stats


def challenger_visuals(records, stats):
    totals_graph = plot_totals_reverse(stats)
    striking_graph = plot_targets_reverse(stats)
    ratio_graph = plot_ratios(records)

    return totals_graph, ratio_graph, striking_graph


def opponent_visuals(records, stats):
    totals_graph = plot_totals(stats)
    striking_graph = plot_targets(stats)
    ratio_graph = plot_ratios(records)

    return totals_graph, ratio_graph, striking_graph


"""-----------------------------------------------
Html Content Wrappers

-----------------------------------------------"""
def empty_card():
    return dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H2("Text"),
                ], style={'textAlign': 'center'})
            ])
    )


def challenger_img(link, f_name, l_name):
    return [html.Img(className="ch-img", src=link, alt=f"No Image"),
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
def get_wins(wins):
    wld = f"{wins['WLD'][0]}-{wins['WLD'][1]}-{wins['WLD'][2]}"
    ko = f"{wins['KO'][0]}-{wins['KO'][1]}"
    sub = f"{wins['SUB'][0]}-{wins['SUB'][1]}"
    return dbc.CardGroup(className='win-holder', children=[
        dbc.Card(className='win-card', children=[
            dbc.CardHeader(className='win-head', children=[
                html.H5("W-L-D", className='win-head-text')]
                           ),
            dbc.CardBody(className='win-body', children=[
                html.H4(f"{wld}", className='win-body-text')]
                         )]
                 ),
        dbc.Card(className='win-card', children=[
            dbc.CardHeader(className='win-head', children=[
                html.H5("(T)KO", className='win-head-text')]
                           ),
            dbc.CardBody(className='win-body', children=[
                html.H4(f"{ko}", className='win-body-text')]
                         )]
                 ),
        dbc.Card(className='win-card', children=[
            dbc.CardHeader(className='win-head', children=[
                html.H5("Sub", className='win-head-text')]
                           ),
            dbc.CardBody(className='win-body', children=[
                html.H4(f"{sub}", className='win-body-text')]
                         )]
                 )]
                         )


# Row Three Helpers

def insert_fig(fig):
    return dcc.Graph(className='fig', figure=fig, responsive='auto')


# Path Finder

def find_path(challenger, opponent):
    fight_path = mma_math(name_db, challenger, opponent)
    print(fight_path)
    print(len(fight_path))
    return [
        dbc.Button(challenger, id='ch-button', className='ch-button'),

        html.Div(id='path-holder', className='path-holder', children=[
            html.I(className='fas fa-arrow-right fa-lg arrow')

        ]),
        dbc.Button(opponent, id='op-button', className='op-button')
    ]


def initial_path(challenger, opponent):
    return [
        dbc.Button(challenger, id='ch-button', className='ch-button'),

        dcc.Loading(id='path-loader', children=[
            html.Div(id='path-holder', className='path-holder', children=[
                # html.I(className='fas fa-arrow-right fa-lg arrow')
            ])]
                    ),

        dbc.Button(opponent, id='op-button', className='op-button')
    ]


# def initial_path(challenger, opponent):
#     return [
#         dbc.Button(challenger, id='ch-button', className='ch-button'),
#
#         html.Div(id='path-holder', className='path-holder', children=[
#             html.I(className='fas fa-arrow-right fa-lg arrow')
#
#         ]),
#         dbc.Button(opponent, id='op-button', className='op-button')
#     ]


"""-----------------------------------------------
Layout Functions

-----------------------------------------------"""


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
                          valid=False, invalid=True,
                          placeholder='Input Challenger Name')]),
            html.P('Beats', className='side-text'),

            dbc.FormGroup(className='input-b', children=[
                dbc.Label('Fighter B', html_for='fighter-b'),
                dbc.Input(id='fighter-b', type='text',
                          valid=False, invalid=True,
                          placeholder='Input Opponent Name')]
                          ),
            dbc.Button('Confirm', id='submit', size='lg',
                       color='primary', disabled=True)]
                 )]
                    )


def content_layout(ch_name, op_name):
    ch_data = fighter_data(name_db, ch_name)
    ch_head = ch_data[0]
    ch_records = ch_data[1]
    ch_stats = ch_data[2]
    ch_plots = challenger_visuals(ch_records, ch_stats)

    op_data = fighter_data(name_db, op_name)
    op_head = op_data[0]
    op_records = op_data[1]
    op_stats = op_data[2]
    op_plots = opponent_visuals(op_records, op_stats)

    return html.Div(className='content-area', children=[
        dbc.Row(className="top-row", children=[
            dbc.Col(challenger_img(*ch_head), width=5,
                    id='head-ch', className='head-ch'),
            dbc.Col(opponent_img(*op_head), width=5, className='head-op')],
                justify='between'),


        dbc.Row(className="row-two", children=[
            dbc.Col(get_wins(ch_records), width=5, className='wins'),
            dbc.Col(get_wins(op_records), width=5, className='wins')],
                justify='between'),


        dbc.Row(className="row-three", children=[
            dbc.Col(className='row-three-col', width=5, children=[
                dbc.Row(className='row-three-col-row', children=[
                    dbc.Col(className='fig-col-three', width=4, children=[
                        insert_fig(ch_plots[1])
                    ]),
                    dbc.Col(className='fig-col-three', width=8, children=[
                        insert_fig(ch_plots[0])
                    ])],
                        no_gutters=True, justify='between')]
                    ),

            dbc.Col(className='axis-col', width=2, children=[
                dbc.Row(className='axis-box', children=[
                    html.H4('Takedown Accuracy', className='axis-text')
                ]),

                dbc.Row(className='axis-box', children=[
                    html.H4('Sig. Strike Accuracy', className='axis-text')

                ], style={'border-top-style': 'none',
                          'border-bottom-style': 'none'}),
                dbc.Row(className='axis-box', children=[
                    html.H4('Total Strike Accuracy', className='axis-text')

                ]),
            ]),

            dbc.Col(className='row-three-col', width=5, children=[
                dbc.Row(className='row-three-col-row', children=[
                    dbc.Col(className='fig-col-three', width=8, children=[
                        insert_fig(op_plots[0])
                    ]),
                    dbc.Col(className='fig-col-three', width=4, children=[
                        insert_fig(op_plots[1])
                    ])],
                        no_gutters=True, justify='between')]
                    )],
                justify='between'),


        dbc.Row(className="row-four", children=[
            dbc.Col(insert_fig(ch_plots[2]), width=5, className='row-four-col'),

            dbc.Col(className='four-axis-col', width=2, children=[
                dbc.Row(className='four-axis-title-box', children=[
                    html.H4('Target Breakdown', className='axis-text')
                ], style={'color': '#F9AA33'}),

                dbc.Row(className='four-axis-box', children=[
                    html.H3('Head', className='axis-text')
                ]),

                dbc.Row(className='four-axis-box', children=[
                    html.H3('Body', className='axis-text')

                ], style={'border-top-style': 'none',
                          'border-bottom-style': 'none'}),
                dbc.Row(className='four-axis-box', children=[
                    html.H3('Leg', className='axis-text')

                ]),
            ]),


            dbc.Col(insert_fig(op_plots[2]), width=5, className='row-four-col')],
                justify='between'
                ),


        dbc.Row(className="bot-row", children=[
            dbc.Col(id='bot-row-col', className='bot-row-col', width=12, children=[
                dbc.Row(className='path-title', children=[
                    html.H4('MMA-MATH Path', className='path-title-text')
                ]),
                dbc.Row(id='path-row', className='path-row',
                        children=initial_path(ch_name, op_name)
                        )
            ])
        ])
    ])


# EMPTY PLACEHOLDER

# App Layout
app.layout = html.Div(children=[
    side_bar(),
    dbc.Spinner(id='load-layout', size='lg', children=[
        html.Div(id='layout')],
                spinner_style={'margin-left': '55vw',
                               'margin-top': '45vh',
                               'width': '5rem',
                               'height': '5rem'}

                )

])



# app.layout = html.Div(children=[
#     side_bar(),
#     html.Div(id='layout', children=[
#         ]
#              )])


# CALLBACKS
@app.callback(
    [Output("fighter-a", "valid"),
     Output("fighter-a", "invalid"),
     Output("fighter-b", "valid"),
     Output("fighter-b", "invalid"),
     Output("submit", "disabled")],
    [Input("fighter-a", "value"),
     Input("fighter-b", "value")],
    [State("fighter-a", "valid"),
     State("fighter-b", "valid"),
     State("fighter-a", "invalid"),
     State("fighter-b", "invalid"),
     State("submit", "disabled")],
    prevent_initial_call=True

)
def check_name(a_name, b_name,
               a_curr_val, b_curr_val, a_curr_inv, b_curr_inv, b_dis):
    a_link = name_to_url(name_db, a_name)
    b_link = name_to_url(name_db, b_name)

    a_valid = a_curr_val
    a_invalid = a_curr_inv
    b_valid = b_curr_val
    b_invalid = b_curr_inv
    is_disabled = b_dis

    # print(dash.callback_context)

    if (a_link is not None) and (a_name != b_name):
        a_valid = True
        a_invalid = False
    else:
        a_valid = False
        a_invalid = True

    if (b_link is not None) and (b_name != a_name):
        b_valid = True
        b_invalid = False
    else:
        b_valid = False
        b_invalid = True

    if (a_valid is True) and (b_valid is True):
        is_disabled = False
    else:
        is_disabled = True

    return a_valid, a_invalid, b_valid, b_invalid, is_disabled


@app.callback(
    Output('layout', 'children'),
    [Input("submit", "n_clicks")],
    [State("fighter-a", "value"),
     State("fighter-b", "value")]
)
def update_dash(n, a_value, b_value):
    if n is None:
        return content_layout('Khabib Nurmagomedov', 'Conor McGregor')
        # return html.H1('PLEASE INPUT FIGHTERS', className='content-area')
    else:
        ch = a_value
        op = b_value
        return content_layout(a_value, b_value)


@app.callback(
    Output('path-holder', 'children'),
    [Input("layout", "children")],
    [State("fighter-a", "value"),
     State("fighter-b", "value")],
    prevent_initial_call=True
)
def update_path(layout, ch_name, op_name):
    print('Layout updated...finding path')
    return f"{ch_name} -> {op_name}"


# @app.callback(
#     Output('path-holder', 'children'),
#     [Input('layout', 'children'),
#      Input('op-button', 'value')]
# )
# def test(ch_name, op_name):
#     print('oof')
#     return None


# Run App
if __name__ == '__main__':
    app.run_server(debug=True)
