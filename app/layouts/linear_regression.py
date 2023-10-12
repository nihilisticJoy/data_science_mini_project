from dash import html, dcc
import plotly.express as px

from sklearn.model_selection import train_test_split, KFold
from sklearn.linear_model import LinearRegression, Ridge, LassoCV
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score

from math import sqrt


class Linear_Regression:
    @classmethod
    def get_layout(self, df):
        numerical_cols = [i for i in df.columns if df[i].dtype != "object"][1:]
        layout = [
            html.Div(
                [
                    html.Div(
                        [
                            html.H3("Features"),
                            dcc.Dropdown(
                                numerical_cols,
                                id="lm_features",
                                clearable=False,
                                multi=True,
                            ),
                        ],
                        style={
                            "width": "40%",
                            "display": "inline-block",
                        },
                    ),
                    html.Div(
                        [
                            html.H3("Target"),
                            dcc.Dropdown(
                                numerical_cols,
                                id="lm_target",
                                clearable=False,
                            ),
                        ],
                        style={
                            "width": "40%",
                            "display": "inline-block",
                            "padding-left": "4%",
                        },
                    ),
                    html.Div(
                        [
                            html.Button("Run", id="lm_btn", n_clicks=0),
                        ],
                        style={
                            "width": "16%",
                            "display": "inline-block",
                        },
                    ),
                    html.Div(
                        [
                            html.H3("Data subset"),
                            dcc.Checklist(
                                ["Non-free", "Only non-zero Discount"],
                                ["Non-free", "Only non-zero Discount"],
                                id="data_subset",
                            ),
                        ]
                    ),
                ]
            ),
            html.Div(id="lm_results"),
        ]

        return layout


def get_result_layout(lm):
    layout = html.Div(
        [
            html.H1("Linear Regression Model Results", className="header_style"),
            html.Div(
                [
                    html.Span("Coefficients:", className="label_style"),
                    html.Span(str(lm["coefficients"])),
                ],
                className="content_div_style",
            ),
            html.Div(
                [
                    html.Span("Training Score:", className="label_style"),
                    html.Span(str(lm["training_score"])),
                ],
                className="content_div_style",
            ),
            html.Div(
                [
                    html.Span("R-squared (R2):", className="label_style"),
                    html.Span(str(lm["r2"])),
                ],
                className="content_div_style",
            ),
            html.Div(
                [
                    html.Span("Mean Squared Error (MSE):", className="label_style"),
                    html.Span(str(lm["mse"])),
                ],
                className="content_div_style",
            ),
            html.Div(
                [
                    html.Span("Mean Absolute Error (MAE):", className="label_style"),
                    html.Span(str(lm["mae"])),
                ],
                className="content_div_style",
            ),
            html.Div(
                [
                    html.Span(
                        "Root Mean Squared Error (RMSE):", className="label_style"
                    ),
                    html.Span(str(lm["rmse"])),
                ],
                className="content_div_style",
            ),
        ],
        style={
            "width": "50%",
            "margin": "40px auto",
            "padding": "20px",
            "border": "1px solid #ddd",
            "borderRadius": "5px",
        },
    )
    return layout
