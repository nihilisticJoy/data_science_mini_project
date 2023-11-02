import dash
from dash import html

dash.register_page(__name__, path="/")

layout = html.Div(
    [
        html.H1("Gamesaver"),
        html.P(
            """Welcome to Gamesaver!
            Explore the dataset freely and create your own machine learning models to predict insights related to the games on Stream!"""
        ),
    ],
    className="content",
)
