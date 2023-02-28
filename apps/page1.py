import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pathlib

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
df = pd.read_csv(DATA_PATH.joinpath('Stanovi Pula cleaned 20.02.2023.csv'))

df.drop(454, inplace=True)
df.drop(339, inplace=True)
fl = pd.DataFrame(df['Floor'].value_counts())
fl.index.name = 'floor'
fl.columns = ['count']
fl = fl.reset_index()
loc = pd.DataFrame(df['Location'].value_counts())
loc.index.name = 'Location'
loc.columns = ['count']
loc = loc.reset_index()
df['Price_€/m²'] = df['Price_€'] / df['Area_m²']
df1 = df.groupby('Location')['Price_€/m²'].mean().round(2).reset_index(name='Location_Avg_price/m²')
df1.sort_values(by=['Location_Avg_price/m²'], ascending=False)
df3 = pd.DataFrame(df.groupby(['Location', 'Newly_built'])['Price_€/m²'].apply(np.median).round(2)).reset_index()
dic = {0: 'Old_ap_price', 1: 'New_ap_price'}
df3['New vs old'] = df3['Newly_built'].map(dic)
del df3['Newly_built']
df3 = df3.reset_index().pivot(columns='New vs old', index='Location', values='Price_€/m²').fillna(0).reset_index()
df3 = df3.replace({0: np.nan})
new_old = pd.DataFrame(df.Newly_built.value_counts(normalize=True).mul(100)).round(2)
new_old.index.name = 'New vs old'
new_old.columns = ['Percentage']
new_old = new_old.reset_index()
dic1 = {0: 'Old', 1: 'New'}
new_old['New_vs_old'] = new_old['New vs old'].map(dic1)
df2 = df.groupby('Newly_built')['Price_€/m²'].mean().round(2).reset_index(name='Avg_price/m²_newly_vs_old')
dic2 = {0: 'Old', 1: 'New'}
df2['New vs old'] = df2['Newly_built'].map(dic2)
bins = [0, 50, 100, 505]
labels = ['<50m²', '50-100m²', '100m²>']
df['Bins_area'] = pd.cut(df['Area_m²'], bins=bins, labels=labels, right=False, include_lowest=True)
df_bins = df.groupby(df['Bins_area'], as_index=False)['Price_€/m²'].mean().round(2)
df_bins['Bins_area_count'] = df['Bins_area'].value_counts().values
new_old = pd.DataFrame(df.Newly_built.value_counts(normalize=True).mul(100)).round(2)
new_old.index.name = 'New vs old'
new_old.columns = ['Percentage']
new_old = new_old.reset_index()
dic1 = {0: 'Old', 1: 'New'}
new_old['New_vs_old'] = new_old['New vs old'].map(dic1)
df_bins_nvo = pd.DataFrame(df.groupby(['Bins_area', 'Newly_built'])['Price_€/m²']
                           .apply(np.median).round(2)).reset_index()
dic3 = {0: 'Old_ap_price', 1: 'New_ap_price'}
df_bins_nvo['New vs old'] = df_bins_nvo['Newly_built'].map(dic3)
del df_bins_nvo['Newly_built']
df_bins_nvo = \
    df_bins_nvo.reset_index().pivot(columns='New vs old', index='Bins_area', values='Price_€/m²').reset_index()
# df_bins_nvo = df_bins_nvo.loc[[2, 1, 0], :]
df_0 = df.loc[(df['Newly_built'] == 0), ['Price_€/m²', 'Location', 'Bins_area']]
df_0_loc = pd.DataFrame(df_0.groupby(['Location', 'Bins_area'])['Price_€/m²'].apply(np.median).round(2)).reset_index()
df_0_loc = df_0_loc.reset_index().pivot(columns='Bins_area', index='Location', values='Price_€/m²').reset_index()
df_1 = df.loc[(df['Newly_built'] == 1), ['Price_€/m²', 'Location', 'Bins_area']]
df_1_loc = pd.DataFrame(df_1.groupby(['Location', 'Bins_area'])['Price_€/m²'].apply(np.median).round(2)).reset_index()
df_1_loc = df_1_loc.reset_index().pivot(columns='Bins_area', index='Location', values='Price_€/m²').reset_index()

fig1 = px.pie(fl, names='floor', values='count', color='floor', title='Most commonly sold floor in the market',
              color_discrete_sequence=px.colors.sequential.RdBu, width=965, height=600)
fig2 = px.pie(loc, names='Location', values='count', title='Number of apartments by location (%)',
              color_discrete_sequence=px.colors.sequential.RdBu, width=965, height=600)
fig3 = go.Figure()
fig3.add_trace(go.Bar(
    x=df3['Location'],
    y=df3['New_ap_price'],
    name='Newely build',
    marker={'color': 'rosybrown'},
    text=df3['New_ap_price'],
    textposition="outside"
))
fig3.add_trace(go.Bar(
    x=df3['Location'],
    y=df3['Old_ap_price'],
    name='Old',
    marker={'color': 'orangered'},
    text=df3['Old_ap_price'],
    textposition="outside"
))
fig3.update_layout(barmode='group', xaxis_tickangle=-45,
                   title='New vs old average price €/m² by location',
                   xaxis_title="Location",
                   yaxis_title="Price_€",
                   legend_title="New vs old",
                   width=900, height=650)
fig4 = px.bar(new_old, x='New_vs_old', y=['Percentage', 'New_vs_old'],
              title='Newly built vs old (%) ',
              color='New_vs_old',
              text_auto=True,
              width=800, height=400,
              color_discrete_sequence=px.colors.sequential.RdBu,
              labels={"value": 'Percentage', "New_vs_old": "New vs old"})
fig4.update_layout(legend_title_text='New vs old')
fig5 = px.bar(df2, x='New vs old', y=['Avg_price/m²_newly_vs_old', 'New vs old'],
              title='Newly built vs old average price € ',
              color='New vs old',
              text_auto=True,
              width=800, height=400,
              color_discrete_sequence=px.colors.sequential.RdBu,
              labels={"value": 'Average price €', "New_vs_old": "New vs old"})
fig5.update_layout(legend_title_text='New vs old')
fig6 = px.bar(df1, y='Location_Avg_price/m²', x='Location', text_auto=True,
              color_discrete_sequence=px.colors.sequential.RdBu,
              title="Average price €/m² by location",
              labels={"Location_Avg_price/m²": 'Average price/m²'},
              width=965, height=650)
fig6.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
fig7 = make_subplots(specs=[[{"secondary_y": True}]])
fig7.add_trace(
    go.Scatter(x=df_bins["Bins_area"], y=df_bins["Price_€/m²"], name="Price €/m²", mode='lines+markers+text',
               text=df_bins["Price_€/m²"],
               textposition='bottom center'),
    secondary_y=True
)
fig7.add_trace(
    go.Bar(x=df_bins["Bins_area"], y=df_bins["Bins_area_count"], name="Number of apartments",
           text=df_bins["Bins_area_count"]),
    secondary_y=False
)
fig7.update_xaxes(title_text="Apartment area")
fig7.update_yaxes(range=[0, 1100], title_text="Number of apartments", secondary_y=False)
fig7.update_yaxes(range=[0, 4000], title_text="Price €/m²", secondary_y=True)
fig7.update_layout(title_text='Avg price and count of small, medium and large apartments', width=965, height=600)
fig8 = go.Figure()
fig8.add_trace(go.Scatter(
    x=df_bins_nvo['Bins_area'],
    y=df_bins_nvo['New_ap_price'],
    mode='lines+markers+text',
    name="New ap. price €/m²",
    text=df_bins_nvo['New_ap_price'],
    textposition='top center'
))
fig8.add_trace(go.Scatter(
    x=df_bins_nvo['Bins_area'],
    y=df_bins_nvo['Old_ap_price'],
    name="Old ap. price €/m²",
    mode='lines+markers+text',
    text=df_bins_nvo['Old_ap_price'],
    textposition='bottom center'
))
fig8.update_layout(title_text='Average price €/m² of newly and old built per apartment size')
fig8.update_layout(legend_title_text='New vs old')
fig8.update_xaxes(title_text="Apartment area")
fig8.update_yaxes(title_text="Price €/m²")
fig9 = go.Figure()
fig9.add_trace(go.Bar(
    x=df_0_loc['Location'],
    y=df_0_loc['<50m²'],
    name='<50m²',
    marker={'color': 'rosybrown'},
    text=df_0_loc['<50m²'],
    textposition="outside"
))
fig9.add_trace(go.Bar(
    x=df_0_loc['Location'],
    y=df_0_loc['50-100m²'],
    name='50-100m²',
    marker={'color': 'darkred'},
    text=df_0_loc['50-100m²'],
    textposition="outside"
))
fig9.add_trace(go.Bar(
    x=df_0_loc['Location'],
    y=df_0_loc['100m²>'],
    name='100m²>',
    marker={'color': 'red'},
    text=df_0_loc['100m²>'],
    textposition="outside"
))
fig9.update_layout(barmode='group', xaxis_tickangle=-45, title='Old built apartments by location, average price €/m²'
                                                               'and size',
                   xaxis_title="Location",
                   yaxis_title="Price €/m2",
                   legend_title="Apartment area",
                   width=965, height=650)
fig10 = go.Figure()
fig10.add_trace(go.Bar(
    x=df_1_loc['Location'],
    y=df_1_loc['<50m²'],
    name='<50m²',
    marker={'color': 'rosybrown'},
    text=df_1_loc['<50m²'],
    textposition="outside"
))
fig10.add_trace(go.Bar(
    x=df_1_loc['Location'],
    y=df_1_loc['50-100m²'],
    name='50-100m²',
    marker={'color': 'darkred'},
    text=df_1_loc['50-100m²'],
    textposition="outside"
))
fig10.add_trace(go.Bar(
    x=df_1_loc['Location'],
    y=df_1_loc['100m²>'],
    name='100m²>',
    marker={'color': 'red'},
    text=df_1_loc['100m²>'],
    textposition="outside"
))
fig10.update_layout(barmode='group', xaxis_tickangle=-45, title='Newly built apartments by location,average price €/m² '
                                                                'and size',
                    xaxis_title="Location",
                    yaxis_title="Price €/m2",
                    legend_title="Apartment area",
                    width=965, height=650)
fig11 = px.scatter(df, x='Area_m²', y='Price_€', size='Price_€')
fig11.update_layout(title='Relationship of apartment area and price €')

card_content_input = [
    dbc.CardHeader("Welcome to my Real Estate Pula analytical app ", style={'font-weight': 'bold',
                                                                            'text-align': 'center',
                                                                            }),
    dbc.Card(),
    dbc.CardBody(
        [
            html.H4('Overview', className='card-title'),
            html.P(
                "This is an interactive web app build completely in Python using Plotly's Dash analytics "
                "application framework. "
                "The app visualizes data through 11 interactive charts in the Apartments page, 9 charts in the "
                "Land page and 2 in the Overall page. Due to the amount of data and the size of the charts this app "
                "is best used in the desktop view. "
                "The data was collected from the real estate advertiser's website and represents the latest available "
                "data from ads for the previous month. ",
                className="card-text",
            ),
            html.P(
                "DISCLAIMER: Note that the amounts reported in the analysis are those that customers ask for and not "
                "those that they receive after the transaction. There may also be a slight difference in the number of "
                "new and old apartments because it is very ungrateful to filter this type of data from ads text. "
                "Nevertheless, they provide a good insight into the real estate market in Pula. ",
                className="card-text",
            ),
            html.P("The ultimate goal of this project is to monitor price movements on a monthly basis and the impact "
                   "of inflation, interest rates and the introduction of the Euro on the real estate market in Pula.",

                   className="card-text",
                   ),
            html.P(
                "...so stay tuned for new updates. :)",
                className="card-text",
            ),
            dcc.Link(dbc.Button('Go to Land page', color="warning", className="me-1"), href='/page2'),
            dcc.Link(dbc.Button('Go to Overall page', color="warning", className="me-1"), href='/page3'),
            html.Br(),
            html.Br(),
            html.H4('Apartments', className='card-title'),
        ]
    ),

    dbc.CardBody(
        [
            html.H5('Select one of the options:', className='card-title'),
            dcc.Dropdown(id='dropdown',

                         options=[
                             {'label': 'Average price € by location', 'value': 'NvoPLoc'},
                             {'label': 'Relationship of apartment area and price €', 'value': 'AvP'},
                             {'label': 'Newly built vs old (%)', 'value': 'Nvo'},
                             {'label': 'Newly built vs old average price €', 'value': 'APL'},
                             {'label': 'Newly vs old avg price €/m² by location', 'value': 'NvoP'},
                             {'label': 'Number of apartments by location (%)', 'value': 'Loc'},
                             {'label': 'Avg price €/m² of newly & old built per apartment size',
                              'value': 'APNSize'},
                             {'label': 'Avg price and count of small, medium and large apartments',
                              'value': 'APsml'},
                             {'label': 'Old built apartments by location, area & avg price €/m²',
                              'value': 'OLocP'},
                             {'label': 'Newly built apartments by location, area & avg price €/m²',
                              'value': 'NLocP'},
                             {'label': 'Most commonly sold floor in market ', 'value': 'Floor'},
                         ],
                         value='NvoPLoc',
                         searchable=True,
                         style={'color': '#000000', "width": "60%", 'font-size': '12px'}),
            html.Div(id='output-data-upload'),

        ],

    ),
]
chart1_card_content = [
    dbc.CardBody(
        [
            dcc.Graph(id='my_bar1',
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


def init_callbacks(app):
    @app.callback(
        Output('my_bar1', 'figure'),
        [Input(component_id='dropdown', component_property='value')]
    )
    def select_graph(value):
        if value == 'Floor':
            return fig1
        elif value == 'Loc':
            return fig2
        elif value == 'NvoP':
            return fig3
        elif value == 'Nvo':
            return fig4
        elif value == 'APL':
            return fig5
        elif value == 'NvoPLoc':
            return fig6
        elif value == 'APsml':
            return fig7
        elif value == 'APNSize':
            return fig8
        elif value == 'OLocP':
            return fig9
        elif value == 'AvP':
            return fig11
        else:
            return fig10
