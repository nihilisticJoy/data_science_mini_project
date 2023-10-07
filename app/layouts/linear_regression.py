from dash import html, dcc
import plotly.express as px

import numpy as np

from sklearn.model_selection import train_test_split, KFold
from sklearn.linear_model import LinearRegression, Ridge, LassoCV
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score

import pprint
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
                ]
            ),
            html.Div(id="lm_results"),
        ]

        return layout
