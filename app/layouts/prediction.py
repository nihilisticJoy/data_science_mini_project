from dash import html, dcc


class Prediction:
    @classmethod
    def get_layout(self, df):
        numerical_cols = [i for i in df.columns if df[i].dtype != "object"][1:]
        layout = [
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H3("Target"),
                                    dcc.Dropdown(
                                        numerical_cols,
                                        id="prediction_target",
                                        clearable=False,
                                    ),
                                ],
                                className="flex-child target-div",
                            ),
                            html.Div(
                                [
                                    html.H3("Data subset"),
                                    dcc.Checklist(
                                        [
                                            "Non-free",
                                            "Non-zero Discount",
                                            "Under 100% Discount",
                                        ],
                                        [
                                            "Non-free",
                                            "Non-zero Discount",
                                            "Under 100% Discount",
                                        ],
                                        id="data_subset",
                                    ),
                                ],
                                className="flex-child data-subset-div",
                            ),
                        ],
                        className="flex-container",
                    ),
                    html.Div(id="prediction_features_div"),
                    html.Div(id="prediction_result"),
                ]
            )
        ]

        return layout
