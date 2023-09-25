import dash
from dash import html

dash.register_page(__name__, path="/games")

layout = html.Div(
    [
        html.H1("This is our Games page"),
        html.Div("This is our Games page content."),
    ],
    className="content",
)
