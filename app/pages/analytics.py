import dash
from dash import html, dcc, Input, Output, State, callback

import plotly.express as px
import pandas as pd

from layouts.singe_plot import Scatterplot
from layouts.heatmap import Overview
from layouts.linear_regression import Linear_Regression, get_result_layout

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
    if n_clicks == 0:
        return dash.no_update
    lm = evaluate_linear_regression(df, features, target)

    layout = get_result_layout(lm)

    if len(features) == 1:
        fig = px.scatter(df, features[0], target)
        line = px.line(
            x=lm["cleaned_df"][features[0]],
            y=lm["predictions"],
            color_discrete_sequence=["red"],
        )
        fig.add_traces(line.data)

        scatter_div = html.Div(
            [dcc.Graph(figure=fig)],
            id="lm_scatter",
            style={"width": "50%", "display": "inline-block"},
        )

        layout = html.Div([layout], style={"width": "50%", "display": "inline-block"})
        layout = html.Div([layout, scatter_div])

    return layout


@callback(Output("lm_features", "options"), Input("lm_target", "value"))
def update_features_dropdown(target):
    if not target:
        return dash.no_update
    numerical_cols = [i for i in df.columns if df[i].dtype != "object"][1:]
    numerical_cols.remove(target)

    return numerical_cols


@callback(Output("lm_target", "options"), Input("lm_features", "value"))
def update_target_dropdown(features):
    if not features:
        return dash.no_update
    numerical_cols = [i for i in df.columns if df[i].dtype != "object"][1:]
    for i in features:
        numerical_cols.remove(i)

    return numerical_cols
