"""
Author: Aaron Ho
Python Version: 3.7
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from pathlib import Path
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
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

# name_list = list(name_db['name'])
name_list = list(name_db['name'].map(lambda x: html.Option(value=x)))

# lowercase = name_db['name'].str.lower()
# lowercase_db = pd.concat([lowercase, name_db['name']],
#                          axis=1, keys=['lower', 'name'])

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


def query_fighters():
    pass





"""-----------------------------------------------
Html Content Wrappers

-----------------------------------------------"""
def input_suggestion():
    return html.Datalist(id='suggestion', children=name_list)


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

def insert_fig(fig_id, fig):
    return dcc.Graph(id=fig_id, className='fig', figure=fig, responsive='auto')


# Path Finder

def initial_path(challenger, opponent):
    return [
        dbc.Button(challenger, id='ch-button', className='ch-button'),

        dbc.Spinner(id='path-loader', children=[
            html.Div(id='path-holder', className='path-holder')]
                    ),

        dbc.Button(opponent, id='op-button',
                   className='op-button')
    ]


def find_path(fight_path):
    path_list = [html.I(className='fas fa-arrow-right fa-lg arrow')]

    if len(fight_path) > 2:
        win_list = fight_path[1:-1]

        for fighter in win_list:
            #f_id = fighter.replace(' ', '')
            path_list.append(
                dbc.Button(fighter,
                           id={
                               'type': 'path-button',
                               'name': fighter

                           },
                           className='win-button',
                           style={'margin-left': '0.5em',
                                  'margin-right': '0.5em'})
            )

            path_list.append(
                html.I(className='fas fa-arrow-right fa-lg arrow')
            )

    return path_list


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
        fighter_input(),

        html.Div(id='current-challenger', style={'display': 'none'}),
        html.Div(id='current-opponent', style={'display': 'none'}),
        html.Div(id='current-path', style={'display': 'none'}),
        html.Div(id='temp', style={'display': 'none'}),
        dcc.Store(id='fig-storage')

    ]
                    )


def fighter_input():
    return html.Div(className='fighter-input', children=[
        html.P('Input two fighters to prove if...',
               className='side-text'),
        html.Br(),

        input_suggestion(),

        dbc.Form(className='input-form', children=[
            dbc.FormGroup(className='input-a', children=[
                dbc.Label('Fighter A', html_for='fighter-a'),
                dbc.Input(id='fighter-a', type='text',
                          valid=False, invalid=True,
                          placeholder='Input Challenger Name',
                          list='suggestion')]
                          ),

            html.P('Beats', className='side-text'),

            dbc.FormGroup(className='input-b', children=[
                dbc.Label('Fighter B', html_for='fighter-b'),
                dbc.Input(id='fighter-b', type='text',
                          valid=False, invalid=True,
                          placeholder='Input Opponent Name',
                          list='suggestion')]
                          ),
            dbc.Button('Confirm', id='submit', size='lg',
                       color='primary', disabled=True)]
                 )]
                    )


def initial_layout():
    no_data = fighter_data(name_db, None)
    no_records = no_data[1]
    no_stats = no_data[2]

    ch_head = (None, 'Challenger', 'Fighter A')
    op_head = (None, 'Opponent', 'Fighter B')

    ch_plots = challenger_visuals(no_records, no_stats)
    op_plots = opponent_visuals(no_records, no_stats)



    # no_records = {'WLD': (0, 0, 0), 'KO': (0, 0), 'SUB': (0, 0)}
    # print(no_data)

    return html.Div(className='content-area', children=[
        dbc.Row(className="top-row", children=[
            dbc.Col(challenger_img(*ch_head), width=5,
                    id='head-ch', className='head-ch'),
            dbc.Col(opponent_img(*op_head), width=5, className='head-op')],
                justify='between'),

        dbc.Row(className="row-two", children=[
            dbc.Col(get_wins(no_records), width=5, id='ch-recs',
                    className='wins'),
            dbc.Col(get_wins(no_records), width=5, className='wins')],
                justify='between'),

        dbc.Row(className="row-three", children=[
            dbc.Col(className='row-three-col', width=5, children=[
                dbc.Row(className='row-three-col-row', children=[
                    dbc.Col(className='fig-col-three', width=4, children=[
                        insert_fig('ch-wins', ch_plots[1])
                    ]),
                    dbc.Col(className='fig-col-three', width=8, children=[
                        insert_fig('ch-totals', ch_plots[0])
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
                        insert_fig('op-totals', op_plots[0])
                    ]),
                    dbc.Col(className='fig-col-three', width=4, children=[
                        insert_fig('op-wins', op_plots[1])
                    ])],
                        no_gutters=True, justify='between')]
                    )],
                justify='between'),

        dbc.Row(className="row-four", children=[
            dbc.Col(insert_fig('ch-targets', ch_plots[2]), width=5,
                    className='row-four-col'),

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

            dbc.Col(insert_fig('op-targets', op_plots[2]), width=5,
                    className='row-four-col')],
                justify='between'
                ),

        dbc.Row(className="bot-row", children=[
            dbc.Col(id='bot-row-col', className='bot-row-col', width=12, children=[
                dbc.Row(className='path-title', children=[
                    html.H4('MMA-MATH Path', className='path-title-text')
                ]),
                dbc.Row(id='path-row', className='path-row',
                        children=initial_path('Fighter A', 'Fighter B')
                        )
            ])
        ])
    ])


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
            dbc.Col(get_wins(ch_records), width=5, id='ch-recs',
                    className='wins'),
            dbc.Col(get_wins(op_records), width=5, className='wins')],
                justify='between'),


        dbc.Row(className="row-three", children=[
            dbc.Col(className='row-three-col', width=5, children=[
                dbc.Row(className='row-three-col-row', children=[
                    dbc.Col(className='fig-col-three', width=4, children=[
                        insert_fig('ch-wins', ch_plots[1])
                    ]),
                    dbc.Col(className='fig-col-three', width=8, children=[
                        insert_fig('ch-totals', ch_plots[0])
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
                        insert_fig('op-totals', op_plots[0])
                    ]),
                    dbc.Col(className='fig-col-three', width=4, children=[
                        insert_fig('op-wins', op_plots[1])
                    ])],
                        no_gutters=True, justify='between')]
                    )],
                justify='between'),


        dbc.Row(className="row-four", children=[
            dbc.Col(insert_fig('ch-targets', ch_plots[2]),
                    width=5, className='row-four-col'),

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


            dbc.Col(insert_fig('op-targets', op_plots[2]),
                    width=5, className='row-four-col')],
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


# App Layout
app.layout = html.Div(children=[
    side_bar(),
    html.Div(id='layout')
    # dbc.Spinner(id='load-layout', size='lg', children=[
    #     html.Div(id='layout')],
    #             spinner_style={'margin-left': '55vw',
    #                            'margin-top': '45vh',
    #                            'width': '5rem',
    #                            'height': '5rem'}
    #
    #             )

])


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
    [Output('layout', 'children'),
     Output('current-challenger', 'children'),
     Output('current-opponent', 'children')],
    [Input("submit", "n_clicks")],
    [State("fighter-a", "value"),
     State("fighter-b", "value")]
)
def update_dash(n, a_value, b_value):
    if n is None:
        # ch = 'Chan Sung Jung'
        # op = 'Conor McGregor'
        # return content_layout(ch, op), ch, op
        return initial_layout(), None, None
    else:
        # ch = a_value
        # op = b_value

        return content_layout(a_value, b_value), a_value, b_value


@app.callback(
    [Output('path-holder', 'children'),
     Output('current-path', 'children')],
    [Input("current-challenger", "children"),
     Input("current-opponent", "children")],
    [State("submit", "n_clicks")],
    prevent_initial_call=True
)
def update_path(ch_name, op_name, clicks):
    if clicks is None:
        return find_path([]), []

    win_path = mma_math(name_db, ch_name, op_name)

    if win_path is None:
        return html.H2('NO PATH FOUND'), None

    fight_path = find_path(win_path)

    if len(win_path) > 2:
        id_list = win_path[1:-1]
        # id_list = win_path[0:-1]
    else:
        id_list = []

    return fight_path, id_list


@app.callback(
    Output("fig-storage", "data"),
    [Input("current-path", "children")],
    [State("current-challenger", "children"),
     State('head-ch', 'children'),
     State('ch-recs', 'children'),
     State("ch-wins", "figure"),
     State("ch-totals", "figure"),
     State("ch-targets", "figure")],
    prevent_initial_call=True
)
def update_frames(win_path, ch_name, header, recs, wins, totals, targets):
    fig_dict = {}

    ch_data = {
        'header': header,
        'record': recs,
        'wins': wins,
        'totals': totals,
        'targets': targets
    }

    # ch_data = {
    #     'header': header,
    #     'record': recs,
    #     'wins': wins['data'],
    #     'totals': totals['data'],
    #     'targets': targets['data']
    # }

    fig_dict[ch_name] = ch_data

    for fighter in win_path:
        stats = fighter_data(name_db, fighter)
        plots = challenger_visuals(stats[1], stats[2])

        fig_dict[fighter] = {
            'header': challenger_img(*stats[0]),
            'record': get_wins(stats[1]),
            'wins': plots[1],
            'totals': plots[0],
            'targets': plots[2]
        }

        # fig_dict[fighter] = {
        #     'header': challenger_img(*stats[0]),
        #     'record': get_wins(stats[1]),
        #     'wins': plots[1]['data'],
        #     'totals': plots[0]['data'],
        #     'targets': plots[2]['data']
        # }

    return fig_dict


# @app.callback(
#     Output("temp", "children"),
#     [Input("fig-storage", "data")],
#     prevent_initial_call=True
# )
# def check_storage(storage):
#     print(storage)
#     return 'Done'


# @app.callback(
#     [Output("ch-totals", "figure")],
#     [Input("current-path", "children")],
#     [State("ch-wins", "figure"),
#      State("ch-totals", "figure"),
#      State("ch-targets", "figure")],
#     prevent_initial_call=True
# )
# def update_frames(win_path, wins, totals, targets):
#     wins['frames'] = []
#     totals['frames'] = []
#     totals['layout']['updatemenus'][0]['buttons'] = []
#     totals['layout']['updatemenus'][0]['visible'] = True
#     totals['layout']['updatemenus'][0]['type'] = 'buttons'
#     totals['layout']['updatemenus'][0]['active'] = 0
#     totals['layout']['updatemenus'][0]['showactive'] = True
#
#     targets['frames'] = []
#
#     # print(totals['layout'])
#     print(totals['layout']['updatemenus'])
#
#
#     for fighter in win_path:
#         stats = fighter_data(name_db, fighter)
#         plots = challenger_visuals(stats[1], stats[2])
#         button = {
#             'args': [
#                 [fighter],
#                 {'frame': {'duration': 100, 'redraw': True},
#                  'mode': 'immediate',
#                  'name': fighter,
#                  'fromcurrent': True,
#                  'transition': {'duration': 100, 'easing': 'linear'}
#                  }],
#             'label': fighter,
#             'method': 'animate'
#         }
#
#         totals['frames'].append({'data': plots[0]['data'], 'name': fighter})
#         totals['layout']['updatemenus'][0]['buttons'].append(button)
#
#     print(totals['layout']['updatemenus'])
#     print(totals['frames'])
#
#     return [totals]


@app.callback(
    [Output('head-ch', 'children'),
     Output('ch-recs', 'children'),
     Output('ch-wins', 'figure'),
     Output('ch-totals', 'figure'),
     Output('ch-targets', 'figure')],
    [Input('ch-button', 'n_clicks'),
     Input({'type': 'path-button', 'name': ALL}, 'n_clicks')],
    [State({'type': 'path-button', 'name': ALL}, 'children'),
     State('ch-button', 'children'),
     State('current-challenger', 'children'),
     State("fig-storage", "data")],
    prevent_initial_call=True
)
def click_path(nc, np, children, ch_name, curr_fighter, fig_dict):
    context = dash.callback_context

    # print(context.triggered)
    # print(context.states)

    if len(context.triggered) > 1 or context.triggered[0]['value'] is None:
        raise PreventUpdate

    clicked = (context.triggered[0]['prop_id']).split('.')[0]
    name = context.states[f"{clicked}.children"]

    print(name)

    data = fig_dict[name]

    return (data['header'], data['record'],
            data['wins'], data['totals'], data['targets'])


# @app.callback(
#     Output('head-ch', 'children'),
#     [Input({'type': 'path-button', 'name': ALL}, 'n_clicks')],
#     [State({'type': 'path-button', 'name': ALL}, 'children')],
#     prevent_initial_call=True
# )
# def click_path(n, children):
#     context = dash.callback_context
#
#     if len(context.triggered) > 1 or context.triggered[0]['value'] is None:
#         print('initial')
#         raise PreventUpdate
#
#     clicked = (context.triggered[0]['prop_id']).split('.')[0]
#     name = context.states[f"{clicked}.children"]
#
#     ch_data = fighter_data(name_db, name)
#     ch_head = ch_data[0]
#     ch_records = ch_data[1]
#     ch_stats = ch_data[2]
#     ch_plots = challenger_visuals(ch_records, ch_stats)
#
#     return challenger_img(*ch_head)



# Run App
if __name__ == '__main__':
    app.run_server(debug=True)
