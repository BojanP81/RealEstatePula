import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

df_a = pd.read_excel(DATA_PATH.joinpath('Apartments_overall.xlsx'))
df_l = pd.read_excel(DATA_PATH.joinpath('Land_overall.xlsx'))

fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=df_a['Date'],
        y=df_a['Num_old_ap'],
        name="Num_old_ap",
        # marker_color='#64d916',
        marker={'color': '#64d916'},
        hovertext=df_a['Num_old_ap'],
        #         width=0.2,
    ),
)
fig.add_trace(
    go.Bar(
        x=df_a['Date'],
        y=df_a['Num_new_ap'],
        name="Num_new_ap",
        # marker_color='#b2d916',
        marker={'color': '#b2d916'},
        hovertext=df_a['Num_new_ap'],
        #         width=0.2,
    ),
)

fig.add_trace(
    go.Scatter(
        x=df_a['Date'],
        y=df_a['Price_€/m²_mean_old'],
        name="Price_€/m²_mean_old_ap",
        #     mode='lines',
        text=df_a['Price_€/m²_mean_old'],
        hoverinfo='text',
        line=dict(color='#0fb9f7', width=3),
        yaxis="y2")
)

fig.add_trace(
    go.Scatter(
        x=df_a['Date'],
        y=df_a['Price_€/m²_mean_new'],
        name="Price_€/m²_mean_new_ap",
        #     mode='lines',
        text=df_a['Price_€/m²_mean_new'],
        hoverinfo='text',
        line=dict(color='#0ff7cc', width=3),
        yaxis="y2"),
)

fig.add_trace(
    go.Scatter(
        x=df_a['Date'],
        y=df_a['HICP - Cro'],
        name="HICP -Cro",
        #     mode='lines',
        text=df_a['HICP - Cro'],
        hoverinfo='text',
        line=dict(color='#ff0090', width=2),
        yaxis="y3"),
)
fig.add_trace(
    go.Scatter(
        x=df_a['Date'],
        y=df_a['HICP - EU'],
        name="HICP -EU",
        #     mode='lines',
        text=df_a['HICP - EU'],
        hoverinfo='text',
        line=dict(color='#ff00f7', width=2),
        yaxis="y3"),
)

fig.add_annotation(text="HICP source:https://ec.europa.eu/eurostat/en/",
                   x=0,
                   y=-0.2,
                   showarrow=False,
                   textangle=0,
                   xanchor='left',
                   xref="paper",
                   yref="paper")
fig.update_layout(
    xaxis=dict(
        domain=[0.25, 1]
    ),
    yaxis=dict(
        title="Number of apartments",
        titlefont=dict(
            color="#b2d916"
        ),
        tickfont=dict(
            color="#b2d916"
        )
    ),
    yaxis2=dict(
        title="Price",
        titlefont=dict(
            color="#0fe8f7"
        ),
        tickfont=dict(
            color="#0fe8f7"
        ),
        anchor="free",
        overlaying="y",
        side="left",
        position=0.1
    ),
    yaxis3=dict(
        title="HICP",
        titlefont=dict(
            color="#ff0090"
        ),
        tickfont=dict(
            color="#ff0090"
        ),
        anchor="x",
        overlaying="y",
        side="right"
    ),

    title="Apartments overall",
    title_font_color="green",
    title_font_size=30,
    xaxis_title="Date",
    legend_title="Price and number vs inflation",

    legend=dict(orientation='h', xanchor="center", x=0.62, y=1.11),
)
fig1 = go.Figure()

fig1.add_trace(
    go.Bar(
        x=df_l['Date'],
        y=df_l['Num_Agr'],
        name="Num_Agr",
        # marker_color='#64d916',
        marker={'color': '#64d916'},
        hovertext=df_l['Num_Agr'],
        #         width=0.2,
    ),
)
fig1.add_trace(
    go.Bar(
        x=df_l['Date'],
        y=df_l['Num_Build'],
        name="Num_Build",
        # marker_color='#b2d916',
        marker={'color': '#b2d916'},
        hovertext=df_l['Num_Build'],
        #         width=0.2,
    ),
)

fig1.add_trace(
    go.Scatter(
        x=df_l['Date'],
        y=df_l['Price_€/m²_mean_Agr'],
        name="Price_€/m²_mean_Agr",
        #     mode='lines',
        text=df_l['Price_€/m²_mean_Agr'],
        hoverinfo='text',
        line=dict(color='#0fb9f7', width=3),
        yaxis="y2")
)

fig1.add_trace(
    go.Scatter(
        x=df_l['Date'],
        y=df_l['Price_€/m²_mean_Build'],
        name="Price_€/m²_mean_Build",
        #     mode='lines',
        text=df_l['Price_€/m²_mean_Build'],
        hoverinfo='text',
        line=dict(color='#0ff7cc', width=3),
        yaxis="y2"),
)

fig1.add_trace(
    go.Scatter(
        x=df_l['Date'],
        y=df_l['HICP - Cro'],
        name="HICP -Cro",
        #     mode='lines',
        text=df_l['HICP - Cro'],
        hoverinfo='text',
        line=dict(color='#ff0090', width=2),
        yaxis="y3"),
)
fig1.add_trace(
    go.Scatter(
        x=df_l['Date'],
        y=df_l['HICP - EU'],
        name="HICP -EU",
        #     mode='lines',
        text=df_l['HICP - EU'],
        hoverinfo='text',
        line=dict(color='#ff00f7', width=2),
        yaxis="y3"),
)

fig1.add_annotation(text="HICP source:https://ec.europa.eu/eurostat/en/",
                    x=0,
                    y=-0.2,
                    showarrow=False,
                    textangle=0,
                    xanchor='left',
                    xref="paper",
                    yref="paper")
fig1.update_layout(
    xaxis=dict(
        domain=[0.25, 1]
    ),
    yaxis=dict(
        title="Number of land for sale",
        titlefont=dict(
            color="#b2d916"
        ),
        tickfont=dict(
            color="#b2d916"
        )
    ),
    yaxis2=dict(
        title="Price",
        titlefont=dict(
            color="#0fe8f7"
        ),
        tickfont=dict(
            color="#0fe8f7"
        ),
        anchor="free",
        overlaying="y",
        side="left",
        position=0.1
    ),
    yaxis3=dict(
        title="HICP",
        titlefont=dict(
            color="#ff0090"
        ),
        tickfont=dict(
            color="#ff0090"
        ),
        anchor="x",
        overlaying="y",
        side="right"
    ),

    title="Land overall",
    title_font_color="green",
    title_font_size=30,
    xaxis_title="Date",
    legend_title="Price and number vs inflation",

    legend=dict(orientation='h', xanchor="center", x=0.62, y=1.11),
)

card_content_input = [
    dbc.CardHeader("Welcome to my  Real Estate Pula analytical app ", style={'font-weight': 'bold',
                                                                             'text-align': 'center',
                                                                             }),

    dbc.Card(),
    dbc.CardBody(
        [

            dcc.Link(dbc.Button('Go to Apartments page', color="warning", className="me-1"), href='/page1'),
            dcc.Link(dbc.Button('Go to Land page', color="warning", className="me-1"), href='/page2'),
            html.Br(),
            html.Br(),
            html.H4('Overall', className='card-title'),
        ]
    ),

    dbc.CardBody(
        [
            html.H5('Select one of the options:', className='card-title'),
            dcc.Dropdown(id='dropdown2',

                         options=[
                             {'label': 'Apartments overall', 'value': 'AOa'},
                             {'label': 'Land overall', 'value': 'LOa'},

                         ],
                         value='AOa',
                         searchable=True,
                         style={'color': '#000000', "width": "60%", 'font-size': '12px'}),
            html.Div(id='output-data-upload'),

        ],

    ),
]
chart1_card_content = [
    dbc.CardBody(
        [
            dcc.Graph(id='my_bar3',
                      responsive=True,
                      style={"margin-left": "auto", "margin-right": "auto",
                             "height": "100%", "width": "100%"}
                      )
        ]
    ),
]

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Row(dbc.Card(card_content_input, color="primary", inverse=True)),
                dbc.Row(dbc.Card(chart1_card_content, color="primary", inverse=True)),

            ],
            className="mb-4", justify="center",
        ),
    ],
    fluid=True)


def init_callbacks2(app):
    @app.callback(
        Output('my_bar3', 'figure'),
        [Input(component_id='dropdown2', component_property='value')]
    )
    def select_graph(value):
        if value == 'AOa':
            return fig
        else:
            return fig1
