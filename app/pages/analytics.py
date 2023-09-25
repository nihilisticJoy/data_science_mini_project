import dash
from dash import html, dcc, Input, Output, callback

import plotly.express as px
import pandas as pd

dash.register_page(__name__, path="/analytics")

df = pd.read_csv("steam_game_analysis/result_3_tags.csv")
COLUMNS = [
    "Name",
    "Platforms",
    "Reviewers",
    "",
    "Positive percent",
    "Comment",
    "Released",
    "Price",
    "Discount",
    "Discounted price",
    "Type",
    "URL",
    "All_tags",
]

df.columns = COLUMNS

layout = (
    html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [dcc.Dropdown(df.columns, df.columns[0], id="x")],
                        style={"width": "48%", "display": "inline-block"},
                    ),
                    html.Div(
                        [dcc.Dropdown(df.columns, df.columns[1], id="y")],
                        style={"width": "48%", "display": "inline-block"},
                    ),
                ]
            ),
            html.Div([dcc.Graph(id="scatter")]),
        ],
        className="content",
    ),
)


@callback(Output("scatter", "figure"), Input("x", "value"), Input("y", "value"))
def update_graph(x, y):
    fig = px.scatter(df, x, y, hover_name="Name")
    return fig
