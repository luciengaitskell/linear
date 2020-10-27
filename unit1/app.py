"""
Matrix Transformations
Unit 1 Assessment

By Lucien Gaitskell
October 2020

Math is more trouble than it's worth: https://chrisvoncsefalvay.com/2020/07/25/dash-latex/

"""
from ast import literal_eval
import random

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL

import plotly.graph_objects as go

import numpy as np


external_stylesheets = ['assets/styles.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server  # For Gunicorn
app.title = "Luc's Unit 1 Project"

# Default values
DEFAULT = []
# TODO: GOING TO NEED TO ADDRESS THIS BAD HABIT


content = [
    html.Header([
        html.H1("Matrix Transformations"),
        html.H3("Unit 1 Assessment"),
        html.H5("Lucien Gaitskell"),
        html.Hr(),
    ], style={"textAlign": "center"}),

    html.Table([
        html.Tr([
            html.Th("Angle (deg)"),
            html.Th("Shear"),
            html.Th("Scale"),
        ]),
        html.Tr([
            html.Th(dcc.Input(id='angle', type='number', placeholder='0', debounce=True)),
            html.Th([
                dcc.Input(id='shearx', type='number', placeholder='x axis', debounce=True),
                html.Br(),
                dcc.Input(id='sheary', type='number', placeholder='y axis', debounce=True),
            ]),
            html.Th([
                dcc.Input(id='scalex', type='number', placeholder='x axis', debounce=True),
                html.Br(),
                dcc.Input(id='scaley', type='number', placeholder='y axis', debounce=True),
            ]),
        ])
    ]),

    html.Br(),
    html.I('Number of points:'),

    dcc.Input(id='numpts', type='number', placeholder="0", debounce=True),

    html.Br(),
    html.H6('Points:'),
    html.Div(id='point-container', children=[]),

    html.Div(id='output'),
    dcc.Graph(id='graph'),
]


app.layout = html.Div(content)


def sanitize(val, default=0, t=int):
    return t(val) if val is not None and val != "" else default


# https://dash.plotly.com/pattern-matching-callbacks
@app.callback(
    Output('point-container', 'children'),
    [Input('numpts', 'value')],
    [State('point-container', 'children')],
)
def display_points(numpts, children):
    numpts = sanitize(numpts, 0)
    children = []
    for c in range(numpts):
        if len(DEFAULT) <= c:
            default = (random.randint(0, 9), random.randint(0, 9))
            DEFAULT.append(default)

        new_input = dcc.Input(
            id={
                'type': 'point-input',
                'index': c,
            }, type='text', placeholder="Point {}".format(c+1), debounce=True)

        children.append(new_input)
    return children


inputs = []
inputs.extend([Input(name, 'value') for name in ['angle', 'shearx', 'sheary', 'scalex', 'scaley']])
inputs.append(Input({'type': 'point-input', 'index': ALL}, 'value'))
#inputs.extend([Input('pt{}'.format(i), 'value') for i in range(len(DEFAULT))])



@app.callback(
    Output('output', 'children'), Output('graph', 'figure'),
    inputs,
)
def update_output(theta, shearx, sheary, scalex, scaley, points):
    points = [literal_eval(p) if (p is not None and p != '') else DEFAULT[i] for i, p in enumerate(points)]

    vectors = []
    for p in points:
        vectors.append(np.array([[e] for e in p]))

    theta = sanitize(theta, 0, float)
    theta *= np.pi / 180
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))

    scalex = sanitize(scalex, 1, float)
    scaley = sanitize(scaley, 1, float)
    shearx = sanitize(shearx, 0, float)
    sheary = sanitize(sheary, 0, float)

    scale = np.array(((scalex, shearx), (sheary, scaley)), dtype=np.float)

    coeff = np.dot(R, scale)
    print(coeff)

    for i, v in enumerate(vectors):
        vectors[i] = np.dot(coeff, v)
        #print("R * v: {} * {} = {}".format(R, v, vectors[i]))

    x = []
    y = []
    for v in vectors:
        x.append(v[0, 0])
        y.append(v[1, 0])

    x_o, y_o = zip(*points) if len(points) > 0 else ([], [])
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y))
    fig.add_trace(go.Scatter(x=x_o, y=y_o))

    fig.update_layout(
        height=800,
        title="Display"
    )

    fig.update_xaxes(range=(-10, 10))
    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
        range=(-10, 10)
    )

    return "Points {}".format(points), fig


if __name__ == '__main__':
    app.run_server(debug=True)
