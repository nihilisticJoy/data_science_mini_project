import dash
from dash import html, dash_table, Output, Input, callback
import pandas as pd

dash.register_page(__name__, path="/games")

FILE_PATH = "steam_game_analysis/src_data/clean_data.csv"
df = pd.read_csv(FILE_PATH)

layout = html.Div(
    [
        html.H1("Games"),
        html.P("Explore our dataset!"),
        dash_table.DataTable(
            id="table",
            columns=[{"name": c, "id": c, "hideable": True} for c in df.columns[1:]],
            data=df.to_dict("records"),
            editable=False,
            page_action="native",
            page_size=20,
            sort_action="native",
            style_as_list_view=True,
        ),
    ],
    className="content",
)
