from dash import dash_table, dcc, html

right_part_layout = html.Div(
    children=[
        html.H2("FastMiner Result"),
        dcc.Loading(
            id="loading-right",
            type="default",
            children=[
                dash_table.DataTable(
                    id="fm-result-table",
                    columns=[],
                    data=[],
                    row_selectable="single",
                    style_cell={"textAlign": "left"},
                    sort_action="native",
                ),
                html.Div(id="calc-time", style={"marginTop": "20px"}),
            ],
        ),
    ],
    style={
        "minWidth": "100%",
        "maxWidth": "100%",
        "width": "100%",
    },
)
