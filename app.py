import pandas as pd
import plotly.graph_objs as go
import dash
import dash_core_components as dcc
import dash_html_components as html

df = pd.read_csv("./data/topN.csv")

def generate_table(df, max_rows=15):
    cols = list(df.columns)
    cols.remove('year')
    n = min(len(df), max_rows)

    return html.Table(
        [html.Tr([html.Th(col) for col in cols])] + 
        [html.Tr([
            html.Td(df.iloc[i][col]) for col in cols
            ]) for i in range(n)]
    )


def generate_pie(labels, values, title):
    trace = go.Pie(labels = labels, values = values)
    layout = go.Layout(title = title)
    return {'data': [trace], 'layout': layout}


title = html.H4(children="Headquarter of Top 15 H-1B Sponsors")
    
drop_down = html.Div([
    dcc.Dropdown(
        id = 'year_dropdown',
        options = [
            {'label': '2013', 'value': 2013},
            {'label': '2014', 'value': 2014},
            {'label': '2015', 'value': 2015},
            {'label': '2016', 'value': 2016},
            {'label': '2017', 'value': 2017},
        ],
        value = 2017,
        )], 
    style={'width': '48%', 'display': 'inline-block'})


# ====================================
# Create a Dash object (called "app") with certain css style sheet
# ====================================
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)


# ====================================
# Define app layout
# ====================================
app.layout = html.Div(children=[
    title,
    drop_down,
    html.Div(id='my_table'),
    dcc.Graph(id='hq_pie')
    ])


# ====================================
# Define app callback
# ====================================
@app.callback(
    dash.dependencies.Output('my_table', 'children'),
    [dash.dependencies.Input('year_dropdown', 'value')]
    )
def update_table(year):
    df_year = df[df['year'] == year]
    return generate_table(df_year)

@app.callback(
    dash.dependencies.Output('hq_pie', 'figure'),
    [dash.dependencies.Input('year_dropdown', 'value')]
    )
def update_hq_pie(year):
    df_year = df[df['year'] == year]
    df_year_pie = df_year.groupby('head_quarter')['num_applications'].sum().reset_index(name="num_applications")
    labels = df_year_pie['head_quarter']
    values = df_year_pie['num_applications']
    title = "Headquarter Location of Top 15 H-1B Sponsors"
    return generate_pie(labels, values, title)


if __name__ == '__main__':
    app.run_server(debug=True)
