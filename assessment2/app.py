"""
Basis Completion
Unit 4 Assessment

By Lucien Gaitskell
December 2020

"""
from ast import literal_eval
import random

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL

from based import basis, sp

external_stylesheets = ['assets/styles.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server  # For Gunicorn
app.title = "Luc's Linear Assessment 2"


content = [
    html.Header([
        html.H1("Basis Completion"),
        html.H3("Linear Assessment 2"),
        html.H5("Lucien Gaitskell"),
        html.Hr(),
    ], style={"textAlign": "center"}),

    html.H6(html.Strong("Vector Space")),

    html.Span([
        html.I('Dimension: '),
        dcc.Input(id='vspace-dim', min=0, type='number', placeholder="0", value=4, debounce=False, className='config-value'),
    ], className='config-container'),

    html.Span([
        html.I('Type: '),
        dcc.Dropdown(id="vspace-type", className='config-value',
                     options=[
                         {'label': 'Vector', 'value': 'vctr'},
                         {'label': 'Polynomial', 'value': 'poly'}
                     ],
                     value='vctr'
                     ),
    ], className='config-container'),

    html.Br(),
    html.H6(html.Strong('Points:')),
    html.Span([
        html.I('Set Size: '),
        dcc.Input(id='set-size', min=0, type='number', placeholder="0", value=2, debounce=False,
                  className='config-value'),
    ], className='config-container'),
    html.Br(),

    html.Div(id='set-container', children=[]),

    html.H4("Final Set:"),
    html.Div(id='output-container'),
]


app.layout = html.Div(content)


def sanitize(val, default=0, t=int):
    return t(val) if val is not None and val != "" else default


# https://dash.plotly.com/pattern-matching-callbacks
@app.callback(
    Output('set-container', 'children'),
    [Input('vspace-dim', 'value'), Input('set-size', 'value')],
    [State('set-container', 'children'), State({'type': 'vector-input', 'index': ALL}, 'id'), State({'type': 'vector-input', 'index': ALL}, 'value')],
)
def display_points(vdim, ssize, children, existvidx, vvalues):
    """

    :param vdim:
    :param ssize:
    :param children:
    :poram existvidx: Indexes of existing vector values
    :param vvalues: Matching values
    :return:
    """

    vdim = sanitize(vdim, 0)
    ssize = sanitize(ssize, 0)

    set_columns = []

    for v_idx in range(ssize):
        # Each element entry for this vector
        vector_elements = [html.H6("Vector {}".format(v_idx+1))]

        for c in range(vdim):
            existing_idx = next((index for (index, d) in enumerate(existvidx) if d["index"] == "{}-{}".format(v_idx, c)), None)

            if existing_idx is not None and vvalues[existing_idx] is not None:
                existing_value = vvalues[existing_idx]
            else:
                existing_value = 0

            # Each element in a vector
            vector_elements.append(dcc.Input(
                id={
                    'type': 'vector-input',
                    'index': "{}-{}".format(v_idx, c),
                }, type='number', placeholder="Element {}".format(v_idx+1, c+1), debounce=True,
                className="vector-element",
                value=existing_value
            ))
            vector_elements.append(html.Br())

        set_columns.append(html.Th(vector_elements, className="vector-column"))
    display_table = html.Table(html.Tr(set_columns))
    return display_table




@app.callback(
    Output('output-container', 'children'),
    [
        Input({'type': 'vector-input', 'index': ALL}, 'value'), Input('vspace-type', 'value')
    ],
    [State({'type': 'vector-input', 'index': ALL}, 'id'), State('vspace-dim', 'value'), State('set-size', 'value')],
)
def update_output(vecvals, vspacetype, vecids, vecdim, setsize):
    """

    :param vecvals: Vector element values
    :param vecids: Vector element IDs
    :return:
    """

    if vecdim is None or setsize is None:
        return ""

    input_set = [sp.zeros(vecdim, 1) for i in range(setsize)]

    for vid, vval in zip(vecids, vecvals):
        setidx, vecidx = map(int, vid['index'].split('-'))
        input_set[setidx][vecidx] = vval

    final_set = basis(input_set)

    set_columns = []
    for set_vec in final_set:
        vector_elements = []
        for deg, ele in enumerate(set_vec):
            ele = str(ele)
            if vspacetype == 'poly':
                ele += ' *t^{}'.format(deg)

            vector_elements.extend([
                html.P(str(ele)),
                html.Br(),
            ])

        set_columns.append(html.Th(vector_elements, className="output-column"))
    display_table = html.Table(html.Tr(set_columns), style={'margin': '0 auto'})
    return display_table


if __name__ == '__main__':
    app.run_server(debug=True)
