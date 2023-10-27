from dash import Dash, html, dcc, Input, Output, callback
import dash

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, use_pages=True, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.Div(
            [
                html.Img(
                    src="assets/console.png",
                    style={"width": "30px"},
                )
            ],
            id="banner",
            className="banner",
        ),
        html.Div(
            [
                html.Div(
                    [
                        dcc.Link(
                            f"{page['name']}",
                            href=page["relative_path"],
                            className="text",
                        )
                    ],
                    className="link",
                )
                for page in dash.page_registry.values()
            ],
            className="sidebar",
        ),
        dash.page_container,
    ],
    id="app-container",
)

if __name__ == "__main__":
    app.run(debug=True)
