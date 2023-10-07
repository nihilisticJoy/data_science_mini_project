import dash
from dash import html, dcc, Input, Output, State, callback

import plotly.express as px
import pandas as pd

from layouts.singe_plot import Scatterplot
from layouts.heatmap import Overview
from layouts.linear_regression import Linear_Regression

from utils.linear_regression import evaluate_linear_regression

EXPLORATION_TYPE = {
    "Overview": Overview,
    "Scatterplot": Scatterplot,
    "Linear regression": Linear_Regression,
}
FILE_PATH = "steam_game_analysis/src_data/clean_data.csv"

dash.register_page(__name__, path="/analytics")

df = pd.read_csv(FILE_PATH)

layout = (
    html.Div(
        [
            html.H1("Analytics"),
            "On this page, you can explore the games' data by using machine learning methods.",
            html.H3("Choose exploration type"),
            html.Div(
                dcc.Dropdown(
                    ["Overview", "Scatterplot", "Linear regression", "Classification"],
                    "Overview",
                    id="exploration",
                    clearable=False,
                ),
            ),
            html.Div(
                EXPLORATION_TYPE["Overview"].get_layout(df),
                id="analyze_layout",
            ),
        ],
        className="content",
    ),
)


@callback(Output("scatter", "figure"), Input("x", "value"), Input("y", "value"))
def update_scatter(x, y):
    fig = px.scatter(df, x, y, hover_name="Title")
    return fig


@callback(Output("analyze_layout", "children"), Input("exploration", "value"))
def update_layout(exploration):
    layout = EXPLORATION_TYPE[exploration].get_layout(df)
    return layout


@callback(
    Output("lm_results", "children"),
    Input("lm_btn", "n_clicks"),
    State("lm_features", "value"),
    State("lm_target", "value"),
)
def update_lm_results(n_clicks, features, target):
    lm = evaluate_linear_regression(df, features, target)
    return str(lm)
