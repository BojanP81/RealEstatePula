from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from app import app
from apps import page1, page2, page3

page1.init_callbacks(app)
page2.init_callbacks1(app)
page3.init_callbacks2(app)
app.title = 'RealEstatePulaApp.'
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return page1.layout
    elif pathname == '/page2':
        return page2.layout
    elif pathname == '/page1':
        return page1.layout
    elif pathname == '/page3':
        return page3.layout
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=False)
