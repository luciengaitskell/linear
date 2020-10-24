"""
Matrix Transformations
Unit 1 Assessment

By Lucien Gaitskell
October 2020

Math is more trouble than it's worth: https://chrisvoncsefalvay.com/2020/07/25/dash-latex/

"""
from ast import literal_eval

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go

import numpy as np


external_stylesheets = ['assets/styles.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Luc's Unit 1 Project"

# Default values
DEFAULT = [(1, 1), (5, 3), (2, 6)]


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
        ]),
        html.Tr([
            html.Th(dcc.Input(id='angle', type='text', placeholder='0', debounce=True)),
            html.Th(dcc.Input(id='shear', type='text', placeholder='0', debounce=True)),
        ])
    ]),

    # TODO: Implement shear

    html.Br(),
    html.I('Input three points'),

    html.Br(),
    html.H6('Points:'),
]

for i, dval in enumerate(DEFAULT):
    content.append(dcc.Input(id='pt{}'.format(i), type='text', placeholder=str(dval), debounce=True))


content.extend([
    html.Div(id='output'),
    dcc.Graph(id='graph'),
])

app.layout = html.Div(content)


inputs = [Input('angle', 'value')]
inputs.extend([Input('pt{}'.format(i), 'value') for i in range(len(DEFAULT))])


@app.callback(
    Output('output', 'children'), Output('graph', 'figure'),
    inputs,
)
def update_output(theta, *points):
    points = [literal_eval(p) if (p is not None and p != '') else DEFAULT[i] for i, p in enumerate(points)]

    vectors = []
    for p in points:
        vectors.append(np.array([[e] for e in p]))
    print(points)

    theta = int(theta) if theta is not None and theta != "" else 0
    theta *= np.pi / 180
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))


    for i, v in enumerate(vectors):
        vectors[i] = np.dot(R, v)
        #print("R * v: {} * {} = {}".format(R, v, vectors[i]))

    x = []
    y = []
    for v in vectors:
        x.append(v[0, 0])
        y.append(v[1, 0])

    x_o, y_o = zip(*points)
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y))
    fig.add_trace(go.Scatter(x=x_o, y=y_o))
    return "Points {}".format(points), fig


if __name__ == '__main__':
    app.run_server(debug=True)
