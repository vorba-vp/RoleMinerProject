from dash import dash_table, dcc, html

fast_miner_result_layout = html.Div(
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
                    page_size=20,
                    style_data_conditional=[
                        {
                            "if": {
                                "filter_query": '{label} = ""'
                            },  # Apply to empty rows
                            "backgroundColor": "#f9f9f9",
                            "color": "#f9f9f9",
                        }
                    ],
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
