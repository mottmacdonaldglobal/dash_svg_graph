import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go

import svg, dxf



app = dash.Dash(__name__)

fig = go.Figure()



# Update axes properties
fig.update_xaxes(
    range=[0, 200000],
    zeroline=False,
)

fig.update_yaxes(
    range=[100000, 200000],
    zeroline=False,
)



filepath = os.path.join(os.getcwd(),'data','demo.svg')
my_svg = svg.GraphSvg(filepath)
fig.update_layout(shapes = my_svg.traces_from_svg_file(filepath, flip_x = False, flip_y = False))

fig['layout'].update(
    autosize=True,
    yaxis=dict(scaleanchor="x", scaleratio=1),
    title='Heat Map East Podium L3',
    xaxis_title='Wynyard Street',
    )


app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug= True)