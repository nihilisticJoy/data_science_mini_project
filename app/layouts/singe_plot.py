from dash import html, dcc
import plotly.express as px


class Scatterplot:
    @classmethod
    def get_layout(self, df):
        layout = [
            html.Div(
                [
                    html.Div(
                        [
                            html.H3("x"),
                            dcc.Dropdown(
                                df.columns,
                                df.columns[0],
                                id="x",
                                clearable=False,
                            ),
                        ],
                        style={
                            "width": "48%",
                            "display": "inline-block",
                        },
                    ),
                    html.Div(
                        [
                            html.H3("y"),
                            dcc.Dropdown(
                                df.columns,
                                df.columns[1],
                                id="y",
                                clearable=False,
                            ),
                        ],
                        style={
                            "width": "48%",
                            "display": "inline-block",
                            "padding-left": "4%",
                        },
                    ),
                ]
            ),
            html.Div(
                [
                    dcc.Graph(
                        id="scatter",
                        figure=px.scatter(
                            df, df.columns[0], df.columns[1], hover_name="Title"
                        ),
                    )
                ]
            ),
        ]
        return layout
