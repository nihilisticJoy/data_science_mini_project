import dash
from dash import html

dash.register_page(__name__, path="/contact")

layout = html.Div(
    [
        html.H1("This is our Contact page"),
        html.Div("This is our Contact page."),
    ],
    className="content",
)
