import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
import pandas as pd
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("data/movie.csv")
df = df[["movie_title", "title_year", "gross"]]

df.dropna(inplace=True)
df = df.astype({"title_year": "int32"})

app.layout = html.Div([

    dcc.Graph(id='indicator-graphic'),

    dcc.Slider(
        id='year--slider',
        min=df['title_year'].min(),
        max=df['title_year'].max(),
        value=df['title_year'].max(),

        marks={str(year): str(year) for year in df[df['title_year'] % 10 == 0]["title_year"].value_counts().index},

        step=None
    )
])


@app.callback(
    Output('indicator-graphic', 'figure'),
     Input('year--slider', 'value'))
def update_graph(year_value):
    dff = df[df['title_year'] <= year_value].sort_values(by="gross").head(10)

    fig = go.Figure(
            data=[go.Bar(x=dff["movie_title"],
                     y=dff["gross"])]
            )

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest', xaxis_title = "movie title", yaxis_title = "gross")


    return fig


if __name__ == '__main__':
    app.run_server(debug=True)