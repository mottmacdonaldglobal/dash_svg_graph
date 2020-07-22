import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

import cad_to_shapely as c2s
from . import processor

app = dash.Dash(__name__)

fig = go.Figure()

dxf_filepath = os.path.join(os.getcwd(),'data','section_holes_complex.dxf')

my_cadfile = processor.CadGeometry(dxf_filepath)
my_cadfile.load()
my_cadfile.add_to_figure(fig, single_closed_polygon = True)
my_cadfile.set_figure_to_bounds(fig)


fig['layout'].update(
    autosize=False,
    yaxis=dict(scaleanchor="x", scaleratio=1),
    title='Extrusion DXF import',
    )

app.layout = html.Div([
    dcc.Graph(figure=fig, config=dict(staticPlot = True))
])

app.run_server(debug= True)