import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_renderer
import dash_table
import datetime
import pandas as pd
import plotly.graph_objs as go
import flask
import networkx as nx
import numpy as np
import plotly.express as px
import mysql.connector
import os
import plotly.express as px

bus_vol = pd.read_csv("bus_vol.csv")
bus_vol = bus_vol.query("Status in ['Normal','Alarm','Alert']")

## Connecting to database In local host##
SyncAED_db = mysql.connector.connect(host="localhost", user="root", passwd="Classmate123@#", database="Sync_AED")
mycursor = SyncAED_db.cursor()

### Acquistion of the Anomaly Data Table from database ##
anomaly_QUERY = 'SELECT * FROM Sync_AED.`anomaly_dect_data`'
df_anomaly = pd.read_sql_query(anomaly_QUERY, SyncAED_db)
##

### Acquistion of the event Data Table from database ##
event_QUERY = 'SELECT * FROM Sync_AED.`event detction flag`'
df_event = pd.read_sql_query(event_QUERY, SyncAED_db)
##

## Connection from database for Displaying Bus Map ##
bus_data_14 = 'SELECT * FROM Sync_AED.`bus-data`'
bus_data_14_map = pd.read_sql_query(bus_data_14, SyncAED_db)
lat_site = bus_vol.Latitude
lon_site = bus_vol.Longitude
nodes_df = bus_vol.Status

fig = go.Figure(go.Scattermapbox(
    mode="markers+lines",
    lat=lat_site,
    lon=lon_site,
    marker={'size': 12},
    text=nodes_df,
    hoverinfo='text'))

fig.update_layout(
    height=550,
    margin={'l': 0, 't': 0, 'b': 0, 'r': 0},
    mapbox={
        'style': "carto-positron",
        'center': {'lon': -120.222992, 'lat': 46.45826836},
        'zoom': 6})







# bus_data_14_map = bus_data_14_map.query("Status in ['Normal','Alarm','Alert']")
#fig = px.line_mapbox(bus_vol, lat="Latitude", lon="Longitude", color="Status", hover_data=["ID", "Vmin", "Vmax"],
                    # zoom=5.5, color_discrete_sequence=['green', 'red ', 'orange'], height=550)

# fig = px.scatter_mapbox(bus_data_14_map, lat="Latitude", lon="Longitude", hover_data=["ID", "Vmin", "Vmax"],
# color_discrete_sequence=["#19a0ff"], zoom=5, height=550))
#fig.update_layout(mapbox_style="")
#fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

####

G = nx.random_geometric_graph(50, 0.102)

edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        # colorscale options
        # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=36,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2))

node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append('# of connections: ' + str(len(adjacencies[1])))

node_trace.marker.color = node_adjacencies
node_trace.text = node_text

fig_1 = go.Figure(data=[edge_trace, node_trace],
                  layout=go.Layout(
                      titlefont_size=16,
                      showlegend=False,
                      hovermode='closest',
                      margin=dict(b=20, l=5, r=5, t=40),
                      xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)),

                  )

np.random.seed(1)

N = 100
N1 = 50
random_x = np.linspace(10, 100)
random_y1 = np.random.randn(N)
random_y2 = np.random.randn(N) + 5
random_y3 = np.random.randn(N1)

# Create traces
fig_2 = go.Figure()
fig_2.add_trace(go.Scatter(x=random_x, y=random_y1,
                           mode='lines+markers',
                           name='lines+markers'))
fig_3 = go.Figure()
fig_3.add_trace(go.Scatter(x=random_x, y=random_y2,
                           mode='lines+markers',
                           name='lines+markers'))
fig_4 = go.Figure()
fig_4.add_trace(go.Scatter(x=random_x, y=random_y3,
                           mode='lines+markers',
                           name='lines+markers'))

df = pd.read_csv("data copy.csv")
df = df[['id', 'diagnosis', 'radius_mean', "smoothness_mean"]]

app = dash.Dash(external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H1(className="syn_logo", children="SyncAED Tool"),
            html.H5(children="SynchroPhasor Anomaly And Event Detection")], className="six columns head-left "),
    ], className="main_syn_header"),

    html.Div([
        dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
            dcc.Tab(label='SyncAED Detection', value='tab-1-example'),
            dcc.Tab(label='Anomaly Detection', value='tab-2-example'),
            dcc.Tab(label='Event Detection', value="tab-3-example"),
            dcc.Tab(label='USER SETTINGS', value='user-sett', className="sync-user"),
        ]),
        html.Div(id='tabs-content-example')
    ]),
])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(screen_layout):
    if screen_layout == 'tab-1-example':
        return html.Div([
            html.Div([
                html.Div([
                    html.H5(children="Anomaly Detection data"),
                    dash_table.DataTable(id="anomaly-table",
                                         columns=[{"name": i, "id": i, "deletable": True, "selectable": True} for i in
                                                  df_anomaly.columns], row_selectable="multi",
                                         row_deletable=True,
                                         selected_rows=[],
                                         style_cell_conditional=[
                                             {
                                                 'if': {'column_id': c},
                                                 'text-align': 'left'
                                             } for c in ['Date', 'Region']
                                         ],

                                         style_data_conditional=[
                                             {
                                                 'if': {'row_index': 'odd'},
                                                 'backgroundColor': 'rgb(248, 248, 248)',

                                             }
                                         ],

                                         style_header={
                                             'backgroundColor': 'rgb(230, 230, 230)',
                                             'fontWeight': 'bold',
                                             'text-align': 'center'
                                         }, page_size=6, page_action="native", data=df_anomaly.to_dict('records'),
                                         selected_columns=["1", "2"]),
                ], className="anomaly-dec-con"),

                html.Div([
                    html.H5(children="Event Detection data"),
                    dash_table.DataTable(id="anomaly-table-2",
                                         columns=[{"name": i, "id": i, "selectable": True, "deletable": True} for i in
                                                  df_event.columns], row_selectable="multi",
                                         row_deletable=True,
                                         selected_rows=[],
                                         style_cell_conditional=[{
                                             'if': {'column_id': c}, 'textAlign': 'left'} for c in ['Date', 'Region']],
                                         style_data_conditional=[
                                             {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}],
                                         style_header={
                                             'backgroundColor': 'rgb(230, 230, 230)',
                                             'fontWeight': 'bold',
                                             'text-align': 'center'
                                         }, page_size=6, page_action="native", data=df_event.to_dict('records'),
                                         selected_columns=["1", "2"]),
                ], className="event-dec-con"),

            ], className="two-thirds column"),

            html.Div([
                html.H4("Network Graph of PMU Data"),
                dcc.Graph(id="Graph_close",
                          figure=fig),
            ], className="one-third column graph-netrk"),
        ], className="container", id="Syn-EAD")


    elif screen_layout == 'tab-2-example':
        return html.Div([
            html.Div([
                html.H5(children="Anomaly detection PMU Data Table"),
                dash_table.DataTable(id="anomaly-table-2",
                                     columns=[{"name": i, "id": i, "selectable": True} for i in df_anomaly.columns],
                                     row_selectable="multi",
                                     row_deletable=True,
                                     selected_rows=[],
                                     style_cell_conditional=[{
                                         'if': {'column_id': c}, 'textAlign': 'left'} for c in ['Date', 'Region']],
                                     style_data_conditional=[
                                         {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}],
                                     style_header={
                                         'backgroundColor': 'rgb(230, 230, 230)',
                                         'fontWeight': 'bold',
                                         'text-align': 'center'
                                     }, page_size=6, page_action="native", data=df_anomaly.to_dict('records'),
                                     selected_columns=["1", "2"]),
            ], className="anomaly-dect-anomaly-page"),

            html.Div([
                html.Div([
                    dcc.Graph(id="Graph_close", figure=fig_2),
                ], className="four columns"),
                html.Div([dcc.Graph(id="Graph_close",
                                    figure=fig_3)], className="four columns"),
                html.Div([dcc.Graph(id="Graph_close",
                                    figure=fig_4)], className="four columns"),
            ], className="container anomaly-graph-1"),

            html.Div([
                html.Div([
                    dcc.Graph(id="Graph_close", figure=fig_3),
                ], className="four columns"),
                html.Div([dcc.Graph(id="Graph_close",
                                    figure=fig_4)], className="four columns"),
                html.Div([html.Button(dcc.Link("Download/Export", href="/"), className="export_file")],
                         className="four columns export-button "),
            ], className="container anomaly-graph-2"),

        ])


    elif screen_layout == 'tab-3-example':
        return html.Div([
            html.Div([
                html.H5(children="Event detection PMU Data Table"),
                dash_table.DataTable(id="anomaly-table-2",
                                     columns=[{"name": i, "id": i, "selectable": True} for i in df_event.columns],
                                     row_selectable="multi",
                                     row_deletable=True,
                                     selected_rows=[],
                                     style_cell_conditional=[{
                                         'if': {'column_id': c}, 'textAlign': 'left'} for c in ['Date', 'Region']],
                                     style_data_conditional=[
                                         {'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(248, 248, 248)'}],
                                     style_header={
                                         'backgroundColor': 'rgb(230, 230, 230)',
                                         'fontWeight': 'bold',
                                         'text-align': 'center'
                                     }, page_size=6, page_action="native", data=df_event.to_dict('records'),
                                     selected_columns=["1", "2"]),
            ], className="anomaly-dect-anomaly-page"),

            html.Div([
                html.Div([
                    html.Div([
                        dcc.Graph(id="Graph_close", figure=fig_3),
                    ], className="six columns"),
                    html.Div([
                        dcc.Graph(id="Graph_close", figure=fig_2),
                    ], className="six columns"),
                ], className="six columns"),

                html.Div([
                    html.H4("Network Sub-Graph"),
                    dcc.Graph(id="Graph_close", figure=fig_4)], className="six columns"),
            ], className="container event-graph-2"),
        ])

    elif screen_layout == 'user-sett':
        return html.Div([
            html.Div([
                html.Div([
                    html.H3("Select Task")

                ], className='six columns'),

                html.Div([
                    dcc.Checklist(
                        options=[
                            {'label': 'Anomaly Detection', 'value': 'AD'},
                            {'label': 'Event Detection', 'value': 'ED'},
                            {'label': 'Anomaly & Event Detection', 'value': 'AED'}
                        ],
                        value=['AD']
                    ),
                ], className='six columns'),
            ], className="container sel-task"),

            html.Div([
                html.Div([
                    html.H3("Select Base Detector")

                ], className='six columns'),

                html.Div([
                    dcc.Checklist(
                        options=[
                            {'label': 'DBSCAN', 'value': 'AD'},
                            {'label': 'Linear Regression', 'value': 'ED'},
                            {'label': 'Chebyshev', 'value': 'AED'}
                        ],
                        value=['AD']
                    ),
                ], className='six columns'),
            ], className="container sel-task"),

            html.Div([
                html.Div([
                    html.H3("PMU Data Anomaly Option")

                ], className='six columns'),

                html.Div([
                    dcc.Checklist(
                        options=[
                            {'label': 'Detect and Flag', 'value': 'DF'},
                            {'label': 'Mitigate and Replace', 'value': 'MR'},
                        ],
                        value=['DF']
                    ),
                ], className='six columns'),
            ], className="container sel-task"),

            html.Div([
                html.Div(className="six columns"),
                html.Div([html.Button("OK")], className="six columns"),
            ], className="container")

        ], className="evn-click")


if __name__ == '__main__':
    app.run_server(debug=True)
