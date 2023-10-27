import dash
from dash import html, dcc, Input, Output, State, callback, ALL

import plotly.express as px
import pandas as pd

from layouts.singe_plot import Scatterplot
from layouts.heatmap import Overview
from layouts.linear_regression import Linear_Regression, get_result_layout
from layouts.prediction import Prediction

from utils.linear_regression import (
    evaluate_linear_regression,
    predict_linear_regression,
)

EXPLORATION_TYPE = {
    "Overview": Overview,
    "Scatterplot": Scatterplot,
    "Linear regression": Linear_Regression,
    "Prediction": Prediction,
}
FILE_PATH = "steam_game_analysis/src_data/clean_data.csv"

dash.register_page(__name__, path="/analytics")

df = pd.read_csv(FILE_PATH)
NUMERICAL_COLS = [i for i in df.columns if df[i].dtype != "object"][1:]


layout = (
    html.Div(
        [
            html.H1("Analytics"),
            "On this page, you can explore the games' data by using machine learning methods.",
            html.H3("Choose exploration type"),
            html.Div(
                dcc.Dropdown(
                    ["Overview", "Scatterplot", "Linear regression", "Prediction"],
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
    State("data_subset", "value"),
)
def update_lm_results(n_clicks, features, target, subset_conditions):
    if n_clicks == 0:
        return dash.no_update
    dff = df.copy()
    if len(subset_conditions) > 0:
        for i in subset_conditions:
            if i == "Non-free":
                dff = dff[dff["Price"] > 0]
            elif i == "Non-zero Discount":
                dff = dff[dff["Discount"] > 0]
            elif i == "Under 100% Discount":
                dff = dff[dff["Discount"] < 100]
            elif i == "Non-zero Positives":
                dff = dff[dff["Positives"] > 0]
    lm = evaluate_linear_regression(dff, features, target)

    layout = get_result_layout(lm)

    if len(features) == 1:
        fig = px.scatter(dff, features[0], target, hover_name="Title")
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


@callback(
    Output("prediction_features_div", "children"), Input("prediction_target", "value")
)
def update_features_input(target):
    if target is None:
        return dash.no_update
    numerical_cols = [i for i in df.columns if df[i].dtype != "object"][1:]
    numerical_cols.remove(target)

    # Create the grid with the features
    feature_layout = html.Div(
        className="grid-container",
        children=[
            html.Div(
                className="grid-item",
                children=[
                    html.H5(i, className="header-class"),
                    dcc.Input(
                        id={"index": i, "type": "feature_input"},
                        className="input-class",
                        style={"width": "100%"},
                    ),
                ],
            )
            for i in numerical_cols
        ],
    )

    # Button div
    button_layout = html.Div(
        [
            html.Button("Run", id="prediction_btn", n_clicks=0),
        ],
        style={"textAlign": "center", "marginTop": "20px", "width": "100%"},
    )

    # Return combined layout
    return [feature_layout, button_layout]


@callback(
    Output("prediction_result", "children"),
    Input("prediction_btn", "n_clicks"),
    State({"index": ALL, "type": "feature_input"}, "value"),
    State({"index": ALL, "type": "feature_input"}, "id"),
    State("prediction_target", "value"),
    State("data_subset", "value"),
)
def predict(n_clicks, feature_vals, feature_ids, target, subset_conditions):
    if n_clicks == 0:
        return dash.no_update

    dff = df.copy()
    if len(subset_conditions) > 0:
        for i in subset_conditions:
            if i == "Non-free":
                dff = dff[dff["Price"] > 0]
            elif i == "Non-zero Discount":
                dff = dff[dff["Discount"] > 0]
            elif i == "Under 100% Discount":
                dff = dff[dff["Discount"] < 100]

    ids = [i["index"] for i in feature_ids]
    data_dict = {id_: val for id_, val in zip(ids, feature_vals)}

    try:
        filtered_dict = {
            k: float(v) for k, v in data_dict.items() if v is not None and v != ""
        }
    except ValueError:
        return "Input values must be numerical!"

    X_predict = pd.DataFrame([filtered_dict])
    y_pred = predict_linear_regression(
        dff, list(filtered_dict.keys()), target, X_predict
    )

    formatted_pred = round(y_pred[0], 2)  # assuming y_pred is a 1D array or list
    display_result = html.Div(
        [
            html.H4("Predicted Value:"),
            html.Div(
                str(formatted_pred),
                className="predicted-value",  # Reference the CSS class
            ),
        ],
        className="result-container",  # Reference the CSS class
    )
    return display_result
