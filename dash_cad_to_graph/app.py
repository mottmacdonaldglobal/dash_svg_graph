import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

import svg, dxf

app = dash.Dash(__name__)

fig = go.Figure()

dxf_filepath = os.path.join(os.getcwd(),'data','section.dxf')
my_dxf = dxf.DxfImporter(dxf_filepath)
my_dxf_shapes = my_dxf.process()
bounds = my_dxf.bounds()

# Update axes properties
fig.update_xaxes(
    range=[0, 400],
    zeroline=False,
)

fig.update_yaxes(
    range=[0, 400],
    zeroline=False,
)

fig.update_layout(shapes = my_dxf_shapes)

fig['layout'].update(
    autosize=False,
    yaxis=dict(scaleanchor="x", scaleratio=1),
    title='Extrusion DXF import',
    )


app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug= True)