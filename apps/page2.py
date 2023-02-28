import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
df = pd.read_csv(DATA_PATH.joinpath('Zemljišta za prodaju Pula cleaned 20.02.2023.csv'))

df['Price_€/m²'] = df['Price'] / df['Area_m²']
loc = pd.DataFrame(df['Location'].value_counts())
loc.index.name = 'Location'
loc.columns = ['count']
loc = loc.reset_index()
df1 = df.groupby('Location')['Price_€/m²'].mean().round(2).reset_index(name='Location_Avg_price/m²')
df1.sort_values(by=['Location_Avg_price/m²'], ascending=False)
df2 = df.groupby('Type')['Price_€/m²'].mean().round(2).reset_index(name='Avg_price/m²_agr_vs_build')
dic2 = {0: 'Agr.', 1: 'Build.'}
df2['Agr_vs_Build'] = df2['Type'].map(dic2)
df2 = df2.sort_index(ascending=False)
df3 = pd.DataFrame(df.groupby(['Location', 'Type'])['Price_€/m²'].apply(np.median).round(2)).reset_index()
dic = {0: 'Agr_avg_price', 1: 'Build_avg_price'}
df3['Agr. vs Build.'] = df3['Type'].map(dic)
del df3['Type']
df3 = df3.reset_index().pivot(columns='Agr. vs Build.', index='Location', values='Price_€/m²').fillna(0).reset_index()
df3 = df3.replace({0: np.nan})
agr_build = pd.DataFrame(df.Type.value_counts(normalize=True).mul(100)).round(2)
agr_build.index.name = 'Agr. vs Build.'
agr_build.columns = ['Percentage']
agr_build = agr_build.reset_index()
dic1 = {0: 'Agr.', 1: 'Build.'}
agr_build['Agr_vs_Build'] = agr_build['Agr. vs Build.'].map(dic1)
bins = [0, 1000, 5000, 45000]
labels = ['<1000m²', '1000-5000m²', '5000m²>']
df['Bins_area'] = pd.cut(df['Area_m²'], bins=bins, labels=labels, right=False, include_lowest=True)
df_bins_nvo = pd.DataFrame(df.groupby(['Bins_area', 'Type'])['Price_€/m²'].apply(np.median).round(2)).reset_index()
dic3 = {0: 'Agr avg price', 1: 'Build avg price'}
df_bins_nvo['Agr vs Build'] = df_bins_nvo['Type'].map(dic3)
del df_bins_nvo['Type']
df_bins_nvo = df_bins_nvo.reset_index().pivot(columns='Agr vs Build', index='Bins_area',
                                              values='Price_€/m²').reset_index()
df_0 = df.loc[(df['Type'] == 0), ['Price_€/m²', 'Location', 'Bins_area', ]]
df_0_loc = pd.DataFrame(df_0.groupby(['Location', 'Bins_area'])['Price_€/m²'].apply(np.median).round(2)).reset_index()
df_0_loc = df_0_loc.reset_index().pivot(columns='Bins_area', index='Location', values='Price_€/m²').reset_index()
df_1 = df.loc[(df['Type'] == 1), ['Price_€/m²', 'Location', 'Bins_area', ]]
df_1_loc = pd.DataFrame(df_1.groupby(['Location', 'Bins_area'])['Price_€/m²'].apply(np.median).round(2)).reset_index()
df_1_loc = df_1_loc.reset_index().pivot(columns='Bins_area', index='Location', values='Price_€/m²').reset_index()
df_B = df.loc[(df['Type'] == 1)]
df_A = df.loc[(df['Type'] == 0)]

fig1 = px.pie(loc, names='Location', values='count', title='Number of land for sale by Location (%)',
              color_discrete_sequence=px.colors.sequential.RdBu, width=1000,
              height=600)
fig3 = go.Figure()
fig3.add_trace(go.Bar(
    x=df3['Location'],
    y=df3['Build_avg_price'],
    name='Building land',
    marker={'color': 'indianred'},
    text=df3['Build_avg_price'],
    textposition="outside"
))
fig3.add_trace(go.Bar(
    x=df3['Location'],
    y=df3['Agr_avg_price'],
    name='Agricultural land',
    marker={'color': 'lightsalmon'},
    text=df3['Agr_avg_price'],
    textposition="outside"
))
fig3.update_layout(barmode='group', xaxis_tickangle=-45, title='Building vs Agricultural land '
                                                               'average price €/m² by Location',
                   xaxis_title="Location",
                   yaxis_title="Price_€",
                   legend_title="Agr. vs Build.")
fig4 = px.bar(agr_build, x='Agr_vs_Build', y=['Percentage', 'Agr_vs_Build'], title='Agricultural vs Building land (%) ',
              color='Agr_vs_Build',
              text_auto=True,
              width=800, height=400,
              color_discrete_sequence=px.colors.sequential.RdBu,
              labels={"value": 'Percentage', "Agr_vs_Build": "Agr vs Build"})
fig4.update_layout(legend_title_text='Agr. vs Build.')
fig5 = px.bar(df2, x='Agr_vs_Build', y=['Avg_price/m²_agr_vs_build', 'Agr_vs_Build'],
              title='Agricultural vs Building land average price € ',
              color='Agr_vs_Build',
              text_auto=True,
              width=800, height=400,
              color_discrete_sequence=px.colors.sequential.RdBu,
              labels={"value": 'Average price €', "Agr_vs_Build": "Agr vs Build"})
fig5.update_layout(legend_title_text='Agr. vs Build.')
fig6 = go.Figure()
fig6.add_trace(go.Scatter(
    x=df_bins_nvo['Bins_area'],
    y=df_bins_nvo['Build avg price'],
    mode='lines+markers+text',
    name="Building price €/m²",
    text=df_bins_nvo['Build avg price'],
    textposition='top center'
))

fig6.add_trace(go.Scatter(
    x=df_bins_nvo['Bins_area'],
    y=df_bins_nvo['Agr avg price'],
    name="Agicultural price €/m²",
    mode='lines+markers+text',
    text=df_bins_nvo['Agr avg price'],
    textposition='top center'
))

fig6.update_layout(title_text='Average price €/m² of Agricultural vs Building land size')
fig6.update_layout(legend_title_text='Buil. vs Agr. vs old')
fig6.update_xaxes(title_text="Land area")
fig6.update_yaxes(title_text="Price €/m²")
fig7 = go.Figure()
fig7.add_trace(go.Bar(
    x=df_0_loc['Location'],
    y=df_0_loc['<1000m²'],
    name='<1000m²',
    marker={'color': 'indianred'},
    text=df_0_loc['<1000m²'],
    textposition="outside"
))
fig7.add_trace(go.Bar(
    x=df_0_loc['Location'],
    y=df_0_loc['1000-5000m²'],
    name='1000-5000m²',
    marker={'color': 'lightsalmon'},
    text=df_0_loc['1000-5000m²'],
    textposition="outside"
))
fig7.add_trace(go.Bar(
    x=df_0_loc['Location'],
    y=df_0_loc['5000m²>'],
    name='5000m²>',
    marker={'color': 'red'},
    text=df_0_loc['5000m²>'],
    textposition="outside"
))

fig7.update_layout(barmode='group', xaxis_tickangle=-45, title='Agricultural land by location, '
                                                               'average price €/m² and size',
                   xaxis_title="Location",
                   yaxis_title="Price €/m2",
                   legend_title="Land area")
fig8 = go.Figure()
fig8.add_trace(go.Bar(
    x=df_1_loc['Location'],
    y=df_1_loc['<1000m²'],
    name='<1000m²',
    marker={'color': 'indianred'},
    text=df_1_loc['<1000m²'],
    textposition="outside"
))
fig8.add_trace(go.Bar(
    x=df_1_loc['Location'],
    y=df_1_loc['1000-5000m²'],
    name='1000-5000m²',
    marker={'color': 'lightsalmon'},
    text=df_1_loc['1000-5000m²'],
    textposition="outside"
))
fig8.add_trace(go.Bar(
    x=df_1_loc['Location'],
    y=df_1_loc['5000m²>'],
    name='5000m²>',
    marker={'color': 'red'},
    text=df_1_loc['5000m²>'],
    textposition="outside"
))

fig8.update_layout(barmode='group', xaxis_tickangle=-45, title='Building land by location, average price €/m² and size',
                   xaxis_title="Location",
                   yaxis_title="Price €/m2",
                   legend_title="Land area")
fig9 = px.scatter(df_B, x='Area_m²', y='Price_€', size='Price_€',
                  title='Building land relationship between area and price')
fig10 = px.scatter(df_A, x='Area_m²', y='Price_€', size='Price_€',
                   title='Agricultural land relationship between area and price')

card_content_input = [
    dbc.CardHeader("Welcome to my  Real Estate Pula analytical app ", style={'font-weight': 'bold',
                                                                             'text-align': 'center',
                                                                             }),

    dbc.Card(),
    dbc.CardBody(
        [

            dcc.Link(dbc.Button('Go to Apartments page', color="warning", className="me-1"), href='/page1'),
            dcc.Link(dbc.Button('Go to Overall page page', color="warning", className="me-1"), href='/page3'),
            html.Br(),
            html.Br(),
            html.H4('Land', className='card-title'),
        ]
    ),

    dbc.CardBody(
        [
            html.H5('Select one of the options:', className='card-title'),
            dcc.Dropdown(id='dropdown1',

                         options=[
                             {'label': 'Number of land for sale by Location (%)', 'value': 'LfS'},
                             {'label': 'Building land relationship between area and price', 'value': 'Blap'},
                             {'label': 'Agricultural land relationship between area and price', 'value': 'Alap'},
                             {'label': 'Building vs Agricultural land '
                                       'average price €/m² by Location', 'value': 'BvAl'},
                             {'label': 'Agricultural vs Building land (%)', 'value': 'AvBl'},
                             {'label': 'Agricultural vs Building land average price €', 'value': 'AvBap'},
                             {'label': 'Average price €/m² of Agricultural vs Building land size', 'value': 'AvBls'},
                             {'label': 'Agricultural land by location, '
                                       ' average price €/m² and size', 'value': 'Alps'},
                             {'label': 'Building land by location, '
                                       ' average price €/m² and size', 'value': 'Blps'},

                         ],
                         value='LfS',
                         searchable=True,
                         style={'color': '#000000', "width": "60%", 'font-size': '12px'}),
            html.Div(id='output-data-upload'),

        ],

    ),
]
chart1_card_content = [
    dbc.CardBody(
        [
            dcc.Graph(id='my_bar2',
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


def init_callbacks1(app):
    @app.callback(
        Output('my_bar2', 'figure'),
        [Input(component_id='dropdown1', component_property='value')]
    )
    def select_graph(value):
        if value == 'LfS':
            return fig1
        elif value == 'BvAl':
            return fig3
        elif value == 'AvBl':
            return fig4
        elif value == 'AvBap':
            return fig5
        elif value == 'AvBls':
            return fig6
        elif value == 'Alps':
            return fig7
        elif value == 'Blap':
            return fig9
        elif value == 'Alap':
            return fig10

        else:
            return fig8
