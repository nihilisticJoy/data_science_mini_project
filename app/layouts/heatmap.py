from dash import html, dcc
import plotly.express as px


class Overview:
    @classmethod
    def get_layout(self, df):
        numerical_cols = [i for i in df.columns if df[i].dtype != "object"][1:]

        dff = df[numerical_cols]

        corr_matrix = dff.corr()
        fig = px.imshow(
            corr_matrix,
            color_continuous_scale="YlGnBu",
            zmin=-1,
            zmax=1,
            labels=dict(color="Correlation Coefficient"),
        )

        fig.update_xaxes(
            title_text="Columns",
            tickvals=list(range(len(corr_matrix.columns))),
            ticktext=corr_matrix.columns,
        )
        fig.update_yaxes(
            title_text="Columns",
            tickvals=list(range(len(corr_matrix.columns))),
            ticktext=corr_matrix.columns,
        )

        fig.update_layout(width=1300, height=700)

        for i in range(len(corr_matrix.columns)):
            for j in range(len(corr_matrix.columns)):
                fig.add_annotation(
                    dict(
                        x=j,
                        y=i,
                        xref="x",
                        yref="y",
                        text=str(round(corr_matrix.iloc[i, j], 2)),
                        showarrow=False,
                        font=dict(
                            color="black"
                            if abs(corr_matrix.iloc[i, j]) < 0.5
                            else "white",
                            size=12,
                        ),
                    )
                )

        layout = [
            html.Div(
                [
                    dcc.Graph(
                        id="heatmap",
                        figure=fig,
                    )
                ]
            ),
        ]
        return layout
