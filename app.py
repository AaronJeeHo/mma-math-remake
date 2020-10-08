"""
Author: Aaron Ho
Python Version: 3.7
"""

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
from pathlib import Path

from scripts.path_finder import mma_math
from scripts.stat_finder import *
from scripts.visual import *

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.14.0/css/all.css"

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.DARKLY, FONT_AWESOME],
                suppress_callback_exceptions=True)
# Data

path = Path(__file__).parent
name_db = pd.read_csv((path / "data/urls/name_url.tsv"),
                      sep='\t', header=None, names=['name', 'link'])

name_list = list(name_db['name'].map(lambda x: html.Option(value=x)))

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


def format_time(n):
    minutes = int(n / 60)
    seconds = int(n % 60)

    if seconds < 10:
        time_val = f"{minutes}:0{seconds}"
    else:
        time_val = f"{minutes}:{seconds}"

    return time_val


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
            html.Div(id='path-holder', className='path-holder')

        ]
                    ),

        dbc.Button(opponent, id='op-button',
                   className='op-button'),
        html.Div(challenger, id='current-figure', style={'display': 'none'}),
    ]


def find_path(fight_path):
    path_list = [html.I(className='fas fa-arrow-right fa-lg arrow')]

    if len(fight_path) > 2:
        win_list = fight_path[1:-1]

        for fighter in win_list:
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

        input_suggestion(),
        control_tabs(),

        html.Div(id='current-challenger', style={'display': 'none'}),
        html.Div(id='current-opponent', style={'display': 'none'}),
        html.Div(id='current-path', style={'display': 'none'}),
        html.Div(id='timer-status', style={'display': 'none'}),
        dcc.Store(id='fig-storage'),
        dcc.Store(id='path-found'),
    ]
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


def path_controller():
    return html.Div(id='path-controls', children=[
        html.P('Elapsed Time', className='side-text'),
        html.Div(id='timer-container', children=[
            daq.LEDDisplay(id='timer-display', size=64,
                           color='#4ACFAC', backgroundColor='#111111',
                           value='0:00'),
            dcc.Interval(id='timer-interval', disabled=True)
        ]),
        html.Br(),
        dbc.Button('Cancel Search', id='abort', size='lg', color='danger')
    ])


def control_tabs():
    return html.Div(id='tab-container', children=[
        dbc.Tabs(id='tabs', children=[
            dbc.Tab(tab_id='input', children=[fighter_input()]),
            dbc.Tab(tab_id='timer', children=[path_controller()])
        ],
                 active_tab='input',
                 style={'display': 'none'}
                 )
    ]
                    )


def initial_layout():
    no_data = fighter_data(name_db, None)
    no_records = no_data[1]
    no_stats = no_data[2]

    ch_head = (None, 'Challenger', 'Fighter A')
    op_head = (None, 'Opponent', 'Fighter B')

    ch_plots = challenger_visuals(no_records, no_stats)
    op_plots = opponent_visuals(no_records, no_stats)

    op_totals = insert_fig('op-totals', op_plots[0])
    ch_totals = insert_fig('ch-totals', ch_plots[0])

    op_totals.figure['data'][0].pop('textposition', None)
    ch_totals.figure['data'][0].pop('textposition', None)

    op_targets = insert_fig('op-targets', op_plots[2])
    ch_targets = insert_fig('ch-targets', ch_plots[2])

    for i in range(3):
        op_targets.figure['data'][i].pop('textposition', None)
        ch_targets.figure['data'][i].pop('textposition', None)

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
                    dbc.Col(className='fig-col-three', width=8,
                            children=ch_totals)],
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
                    dbc.Col(className='fig-col-three', width=8,
                            children=op_totals),
                    dbc.Col(className='fig-col-three', width=4, children=[
                        insert_fig('op-wins', op_plots[1])
                    ])],
                        no_gutters=True, justify='between')]
                    )],
                justify='between'),

        dbc.Row(className="row-four", children=[
            dbc.Col(ch_targets, width=5, className='row-four-col'),
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

            dbc.Col(op_targets, width=5, className='row-four-col')],
                justify='between'
                ),

        dbc.Row(className="bot-row", children=[
            dbc.Col(id='bot-row-col', className='bot-row-col', width=12, children=[
                dbc.Row(className='path-title', children=[
                    html.H4('MMA-MATH Path', className='path-title-text')
                ]),
                dbc.Row(id='path-row', className='path-row',
                        children=initial_path('Fighter A', 'Fighter B')

                        ),
                html.Div(id='is-loading-container', children=[
                    dcc.RadioItems(id='is-loading',
                                   options=[{'label': 'True', 'value': 'True'},
                                            {'label': 'False', 'value': 'False'}],
                                   value='False',
                                   )
                ], style={'display': 'none'})
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
                        ),
                html.Div(id='is-loading-container', children=[
                    dcc.RadioItems(id='is-loading',
                                   options=[{'label': 'True', 'value': 'True'},
                                            {'label': 'False', 'value': 'False'}],
                                   value='True',
                                   )
                ], style={'display': 'none'})

            ])
        ])
    ])


# App Layout
app.layout = html.Div(children=[
    side_bar(),
    html.Div(id='layout')
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
     Output('current-opponent', 'children'),
     Output("timer-interval", "n_intervals")],
    [Input("submit", "n_clicks")],
    [State("fighter-a", "value"),
     State("fighter-b", "value")]
)
def update_dash(n, a_value, b_value):
    if n is None:
        return initial_layout(), None, None, dash.no_update
    else:
        return content_layout(a_value, b_value), a_value, b_value, 0


@app.callback(
    Output("timer-status", "children"),
    [Input('current-challenger', 'children')],
    prevent_initial_call=True
)
def update_interval(ch):
    return html.Div(id='timer-start')


@app.callback(
    [Output("timer-interval", "disabled"),
     Output("timer-display", "value"),
     Output("tabs", "active_tab")],
    [Input("timer-interval", "n_intervals")],
    [State("timer-interval", "disabled"),
     State("is-loading", "value"),
     State("tabs", "active_tab")],
    prevent_initial_call=True
)
def update_tabs(n, disabled, loading, tab):
    if disabled is True:
        return False, dash.no_update, dash.no_update

    if tab == 'input' and loading == 'True':
        return dash.no_update, format_time(n), 'timer'

    elif tab == 'timer' and loading == 'True':
        return dash.no_update, format_time(n), dash.no_update
    else:
        return True, format_time(0), 'input'


@app.callback(
    [Output('path-holder', 'children'),
     Output('current-path', 'children'),
     Output("fig-storage", "data"),
     Output("is-loading", "value")],
    [Input("timer-start", "children"),
     Input("abort", "n_clicks")],
    [State("current-challenger", "children"),
     State("current-opponent", "children"),
     State("submit", "n_clicks"),
     State('head-ch', 'children'),
     State('ch-recs', 'children'),
     State("ch-wins", "figure"),
     State("ch-totals", "figure"),
     State("ch-targets", "figure")],
    prevent_initial_call=True
)
def update_path(start, abort, ch_name, op_name, clicks, header, recs, wins, totals, targets):
    if clicks is None or ch_name is None:
        return find_path([]), dash.no_update, dash.no_update, dash.no_update

    context = dash.callback_context
    t_id = (context.triggered[0]['prop_id']).split('.')[0]
    print(t_id)

    if t_id == 'abort':
        print('ABORT SEARCH')
        return html.H2('NO PATH FOUND'), [], {}, 'False'

    fig_dict = {}

    ch_data = {
        'header': header,
        'record': recs,
        'wins': wins,
        'totals': totals,
        'targets': targets
    }

    fig_dict[ch_name] = ch_data

    win_path = mma_math(name_db, ch_name, op_name)

    if win_path is None:
        return html.H2('NO PATH FOUND'), [], {}, 'False'

    fight_path = find_path(win_path)

    if len(win_path) > 2:
        id_list = win_path[1:-1]

        for fighter in id_list:
            stats = fighter_data(name_db, fighter)
            plots = challenger_visuals(stats[1], stats[2])

            fig_dict[fighter] = {
                'header': challenger_img(*stats[0]),
                'record': get_wins(stats[1]),
                'wins': plots[1],
                'totals': plots[0],
                'targets': plots[2]
            }
    else:
        id_list = []

    return fight_path, id_list, fig_dict, 'False'


@app.callback(
    [Output('head-ch', 'children'),
     Output('ch-recs', 'children'),
     Output('ch-wins', 'figure'),
     Output('ch-totals', 'figure'),
     Output('ch-targets', 'figure'),
     Output('current-figure', 'children')],
    [Input('ch-button', 'n_clicks'),
     Input({'type': 'path-button', 'name': ALL}, 'n_clicks')],
    [State({'type': 'path-button', 'name': ALL}, 'children'),
     State('ch-button', 'children'),
     State('current-challenger', 'children'),
     State('current-figure', 'children'),
     State("fig-storage", "data")],
    prevent_initial_call=True
)
def click_path(nc, np, children, ch_name, ch_data, curr_figure, fig_dict):
    context = dash.callback_context

    if len(context.triggered) > 1 or context.triggered[0]['value'] is None:
        raise PreventUpdate
    else:

        clicked = (context.triggered[0]['prop_id']).split('.')[0]
        name = context.states[f"{clicked}.children"]

        if name == curr_figure:
            print('current fighter shown')
            raise PreventUpdate
        else:

            data = fig_dict[name]
            return (data['header'], data['record'],
                    data['wins'], data['totals'], data['targets'],
                    name)


# Run App
if __name__ == '__main__':
    app.run_server(debug=True)
