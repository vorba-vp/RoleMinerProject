from dash import dash_table, dcc, html

upa_matrix_layout = html.Div(
    children=[
        html.H2("UPA Table"),
        dcc.Loading(
            id="loading-left",
            type="default",
            children=[
                dash_table.DataTable(
                    id="upa-table",
                    columns=[],
                    data=[],
                    style_cell={
                        "textAlign": "center",
                        "minWidth": "50px",
                        "maxWidth": "50px",
                        "width": "50px",
                        "overflow": "hidden",
                        "textOverflow": "ellipsis",
                    },
                    style_cell_conditional=[
                        {
                            "if": {"column_id": "p_0"},
                            "minWidth": "85px",
                            "maxWidth": "85px",
                            "width": "85px",
                        }
                    ],
                ),
            ],
        ),
    ],
    style={
        "minWidth": "100%",
        "maxWidth": "100%",
        "width": "100%",
    },
)
